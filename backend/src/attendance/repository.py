"""
Attendance module — Repository layer.
"""

import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.attendance.models import AttendanceRecord, Shift, ShiftAssignment


class AttendanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_today(self, employee_id: uuid.UUID, today: date) -> AttendanceRecord | None:
        stmt = select(AttendanceRecord).where(
            AttendanceRecord.employee_id == employee_id,
            AttendanceRecord.date == today,
            AttendanceRecord.is_deleted == False,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, record: AttendanceRecord) -> AttendanceRecord:
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def get_by_employee_range(
        self, employee_id: uuid.UUID, from_date: date, to_date: date,
    ) -> list[AttendanceRecord]:
        stmt = (
            select(AttendanceRecord)
            .where(
                AttendanceRecord.employee_id == employee_id,
                AttendanceRecord.date >= from_date,
                AttendanceRecord.date <= to_date,
                AttendanceRecord.is_deleted == False,
            )
            .order_by(AttendanceRecord.date.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_all_today(self, today: date, page: int = 1, page_size: int = 50) -> tuple[list[AttendanceRecord], int]:
        stmt = (
            select(AttendanceRecord)
            .where(AttendanceRecord.date == today, AttendanceRecord.is_deleted == False)
            .order_by(AttendanceRecord.check_in.desc())
        )
        count_stmt = select(func.count(AttendanceRecord.id)).where(
            AttendanceRecord.date == today, AttendanceRecord.is_deleted == False,
        )
        total = (await self.db.execute(count_stmt)).scalar() or 0
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total

    async def count_present_today(self, today: date) -> int:
        stmt = select(func.count(AttendanceRecord.id)).where(
            AttendanceRecord.date == today,
            AttendanceRecord.status.in_(["present", "late"]),
            AttendanceRecord.is_deleted == False,
        )
        return (await self.db.execute(stmt)).scalar() or 0

    async def count_late_today(self, today: date) -> int:
        stmt = select(func.count(AttendanceRecord.id)).where(
            AttendanceRecord.date == today,
            AttendanceRecord.is_late == True,
            AttendanceRecord.is_deleted == False,
        )
        return (await self.db.execute(stmt)).scalar() or 0

    async def get_summary(self, employee_id: uuid.UUID, from_date: date, to_date: date) -> dict:
        records = await self.get_by_employee_range(employee_id, from_date, to_date)
        present = sum(1 for r in records if r.status in ["present", "late"])
        absent = sum(1 for r in records if r.status == "absent")
        late = sum(1 for r in records if r.is_late)
        wfh = sum(1 for r in records if r.is_remote)
        work_hours = [float(r.work_hours) for r in records if r.work_hours]
        overtime = sum(float(r.overtime_hours or 0) for r in records)
        avg_hours = sum(work_hours) / len(work_hours) if work_hours else 0.0

        total_working_days = (to_date - from_date).days + 1
        weekends = sum(1 for i in range(total_working_days) if (from_date.toordinal() + i) % 7 in [5, 6])
        actual_days = total_working_days - weekends

        return {
            "total_days": actual_days,
            "present_days": present,
            "absent_days": absent,
            "late_days": late,
            "leave_days": 0,
            "wfh_days": wfh,
            "avg_work_hours": round(avg_hours, 1),
            "total_overtime": round(overtime, 1),
            "attendance_percentage": round((present / actual_days) * 100, 1) if actual_days > 0 else 0,
        }


class ShiftRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Shift]:
        stmt = select(Shift).where(Shift.is_deleted == False).order_by(Shift.name)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, shift_id: uuid.UUID) -> Shift | None:
        stmt = select(Shift).where(Shift.id == shift_id, Shift.is_deleted == False)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
