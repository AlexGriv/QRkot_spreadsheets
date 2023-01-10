from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


def fully_invest(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def allocate_donation_funds(session: AsyncSession) -> None:
    non_allocated_donations = await donation_crud.read_not_closed(
        session=session
    )
    opened_charity_projects = await charity_project_crud.read_not_closed(
        session=session
    )
    if not all([non_allocated_donations, opened_charity_projects]):
        return
    for donation in non_allocated_donations:
        for project in opened_charity_projects:
            funds_requested = project.full_amount - project.invested_amount
            funds_available = donation.full_amount - donation.invested_amount
            funds_difference = funds_requested - funds_available

            if funds_difference == 0:
                fully_invest(donation)
                fully_invest(project)

            if funds_difference < 0:
                donation.invested_amount += abs(funds_difference)
                fully_invest(project)

            if funds_difference > 0:
                project.invested_amount += funds_available
                fully_invest(donation)
    await session.commit()
