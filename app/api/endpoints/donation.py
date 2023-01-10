from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import (AllDonationsDBSchema, DonationCreateSchema,
                         DonationDBSchema)
from app.services.investment import allocate_donation_funds

router = APIRouter()


@router.get(
    '/',
    response_model=List[AllDonationsDBSchema],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Список пожертвований'
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Просмотр списка всех пожертвований.
    """
    return await donation_crud.read_all(session=session)


@router.post(
    '/',
    response_model=DonationDBSchema,
    response_model_exclude_none=True,
    summary='Создать пожертвование'
)
async def create_donation(
    donation_in: DonationCreateSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Для авторизированного пользователя.
    Создать пожертвование.
      - **comment** - комментарий;
      - **full_amount** - сумма пожертвования.
    """
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user
    )
    await allocate_donation_funds(session=session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=List[DonationDBSchema],
    summary='Список пожертвований текущего пользователя'
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """
    Для авторизированного пользователя.
    Посмотреть список пожертвований текущего пользователя.
    """
    return await donation_crud.get_user_donations(user=user, session=session)
