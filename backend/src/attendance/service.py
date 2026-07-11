"""
Attendance module — Business logic.
"""

import uuid
from datetime import date, datetime, time, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.attendance.models import AttendanceRecord
from src.attendance.repository import AttendanceRepository, ShiftRepository
from src.attendance.schemas import (
    AttendanceRecordResponse, AttendanceSummary, CheckInRequest,
    CheckOutRequest, ShiftResponse,
)
from src.core.exceptions import NotFoundException, ValidationException
from src.employees.repository import EmployeeRepository


class AttendanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.att_repo = AttendanceRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.employee_repo = EmployeeRepository(db)

    async def check_in(self, employee_id: uuid.UUID, data: CheckInRequest) -> AttendanceRecordResponse:
        today = date.today()
        existing = await self.att_repo.get_today(employee_id, today)
        if existing:
            raise ValidationException("Already checked in today")

        now = datetime.now(timezone.utc)
        grace_time = time(9, 15)
        current_time = now.time()
        is_late = current_time > grace_time
        late_minutes = 0
        if is_late:
            late_dt = datetime.combine(today, current_time) - datetime.combine(today, grace_time)
            late_minutes = int(late_dt.total_seconds() / 60)

        record = AttendanceRecord(
            employee_id=employee_id,
            date=today,
            check_in=now,
            status="late" if is_late else "present",
            is_late=is_late,
            late_minutes=late_minutes,
            is_remote=data.is_remote,
            location_lat=data.location_lat,
            location_lng=data.location_lng,
        )
        record = await self.att_repo.create(record)
        return self._to_response(record)

    async def check_out(self, employee_id: uuid.UUID, data: CheckOutRequest) -> AttendanceRecordResponse:
        today = date.today()
        record = await self.att_repo.get_today(employee_id, today)
        if not record:
            raise ValidationException("No check-in found for today")
        if record.check_out:
            raise ValidationException("Already checked out today")

        now = datetime.now(timezone.utc)
        record.check_out = now

        if record.check_in:
            diff = now - record.check_in
            hours = Decimal(str(round(diff.total_seconds() / 3600, 2)))
            record.work_hours = hours
            if hours > Decimal("9"):
                record.overtime_hours = hours - Decimal("9")
        if data.location_lat:
            record.location_lat = data.location_lat
        if data.location_lng:
            record.location_lng = data.location_lng

        await self.db.flush()
        await self.db.refresh(record)
        return self._to_response(record)

    async def get_my_attendance(
        self, employee_id: uuid.UUID, from_date: date, to_date: date,
    ) -> list[AttendanceRecordResponse]:
        records = await self.att_repo.get_by_employee_range(employee_id, from_date, to_date)
        return [self._to_response(r) for r in records]

    async def get_my_summary(
        self, employee_id: uuid.UUID, from_date: date, to_date: date,
    ) -> AttendanceSummary:
        summary = await self.att_repo.get_summary(employee_id, from_date, to_date)
        return AttendanceSummary(**summary)

    async def get_today_overview(self) -> dict:
        today = date.today()
        total_active = await self.employee_repo.count_active()
        present = await self.att_repo.count_present_today(today)
        late = await self.att_repo.count_late_today(today)

        records, total = await self.att_repo.get_all_today(today, page=1, page_size=50)
        items = []
        for r in records:
            emp = await self.employee_repo.get_by_id(r.employee_id)
            name = emp.user.full_name if emp and emp.user else "Unknown"
            resp = self._to_response(r)
            resp.employee_name = name
            items.append(resp)

        return {
            "total_employees": total_active,
            "present": present,
            "absent": total_active - present,
            "late": late,
            "attendance_rate": round((present / total_active * 100), 1) if total_active > 0 else 0,
            "records": items,
        }

    async def get_shifts(self) -> list[ShiftResponse]:
        shifts = await self.shift_repo.get_all()
        return [ShiftResponse.model_validate(s) for s in shifts]

    def _to_response(self, r: AttendanceRecord) -> AttendanceRecordResponse:
        return AttendanceRecordResponse(
            id=r.id,
            employee_id=r.employee_id,
            date=r.date,
            check_in=r.check_in,
            check_out=r.check_out,
            status=r.status,
            work_hours=r.work_hours,
            overtime_hours=r.overtime_hours,
            is_late=r.is_late,
            late_minutes=r.late_minutes,
            is_remote=r.is_remote,
            location_lat=r.location_lat,
            location_lng=r.location_lng,
        )
