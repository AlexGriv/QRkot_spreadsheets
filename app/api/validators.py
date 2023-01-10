from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdateSchema


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка наличия проекта в базе."""
    charity_project = await charity_project_crud.read_single(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с указанным id не существует!'
        )
    return charity_project


async def check_charity_project_name_duplilcate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """Проверка на уникальность."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверка внесения средств."""
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('В проект были внесены средства, не подлежит удалению!')
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    full_amount_update_value = charity_project_in.full_amount
    if (full_amount_update_value and
       charity_project.invested_amount > full_amount_update_value):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую cумму меньше уже вложенной'
        )
    name_update_value = charity_project_in.name
    await check_charity_project_name_duplilcate(
        charity_project_name=name_update_value, session=session
    )
    return charity_project
