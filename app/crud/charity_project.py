from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class CRUDCharityProject(BaseCRUD):

    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ):
        charity_project = await session.scalar(
            select(self.model).where(
                self.model.name == charity_project_name
            )
        )
        return charity_project


    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> List[Dict[str, str]]:
        """Получение отчета о времени закрытия проектов."""
        projects = await session.execute(
            select([CharityProject]).where(CharityProject.fully_invested == 1)
        )
        projects = projects.scalars().all()
        project_list = []
        for project in projects:
            project_list.append({
                'name': project.name,
                'duration': project.close_date - project.create_date,
                'description': project.description
            })
        project_list = sorted(project_list, key=lambda x: x['duration'])
        return project_list


charity_project_crud = CRUDCharityProject(CharityProject)
