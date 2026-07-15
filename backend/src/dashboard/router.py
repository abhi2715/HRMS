from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.employees.models import Employee, Department
from src.leaves.models import LeaveRequest
import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    # 1. Total Employees
    total_employees_query = await db.execute(select(func.count(Employee.id)).where(Employee.is_deleted == False))
    total_employees = total_employees_query.scalar() or 0

    # 2. Present Today (Placeholder for now, assuming 90% are present since we don't have attendance seed data easily available)
    present_today = int(total_employees * 0.90)

    # 3. Pending Leaves
    pending_leaves_query = await db.execute(select(func.count(LeaveRequest.id)).where(LeaveRequest.status == "pending"))
    pending_leaves = pending_leaves_query.scalar() or 0

    # 4. Open Positions (Hardcoded for now as recruitment module isn't fully integrated)
    open_positions = 5

    # 5. Department Distribution
    dept_query = await db.execute(
        select(Department.name, func.count(Employee.id))
        .join(Employee, Employee.department_id == Department.id)
        .where(Employee.is_deleted == False)
        .group_by(Department.name)
    )
    department_distribution = [{"name": row[0], "value": row[1]} for row in dept_query.all()]
    
    # 6. Recent Hires
    recent_hires_query = await db.execute(
        select(Employee.first_name, Employee.last_name, Employee.date_of_joining, Department.name, Employee.designation_id)
        .join(Department, Employee.department_id == Department.id)
        .where(Employee.is_deleted == False)
        .order_by(Employee.date_of_joining.desc())
        .limit(5)
    )
    
    # We ideally would join with Designation, but this is a quick fix to return a role
    # For now we will return a generic role if we don't join
    
    recent_hires = [
        {
            "name": f"{row[0]} {row[1]}",
            "date": row[2].strftime("%b %d, %Y") if row[2] else "N/A",
            "dept": row[3],
            "role": "Employee" # Adding a placeholder role, ideally join with Designation
        }
        for row in recent_hires_query.all()
    ]

    return {
        "kpis": {
            "totalEmployees": total_employees,
            "presentToday": present_today,
            "pendingLeaves": pending_leaves,
            "openPositions": open_positions,
        },
        "departmentDistribution": department_distribution,
        "recentHires": recent_hires
    }
