from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity
from app.repos.activity import ActivityRepo
from app.resources.exceptions import ValidationError
from app.schemas import (
    ActivityResponseSchema,
    CreateActivityRequestSchema,
    UpdateActivityRequestSchema,
)
from app.services.base import SoftDeletableService

# Constants
MAX_ACTIVITY_DEPTH = 3
MAX_DEPTH_ERROR_MESSAGE = 'Maximum activity nesting level is 3 levels'
SELF_REFERENCE_ERROR_MESSAGE = 'Activity cannot be its own parent'


class ActivityService(SoftDeletableService[UUID, Activity, ActivityResponseSchema]):
    response_schema = ActivityResponseSchema

    def __init__(self, repo: ActivityRepo) -> None:
        super().__init__(repo)
        self.repo: ActivityRepo = repo

    async def _get_activity_depth(self, session: AsyncSession, activity_id: UUID) -> int:
        depth = 0
        current_activity_id: UUID | None = activity_id

        while current_activity_id is not None:
            query = self.repo.retrieve(current_activity_id)
            result = await session.execute(query)
            activity = result.scalar_one_or_none()

            if activity is None:
                break

            current_activity_id = activity.parent_id
            depth += 1

        return depth

    async def create_activity(
        self,
        session: AsyncSession,
        data: CreateActivityRequestSchema,
    ) -> ActivityResponseSchema:
        if data.parent_id is not None:
            parent_depth = await self._get_activity_depth(session, data.parent_id)
            if parent_depth >= MAX_ACTIVITY_DEPTH:
                raise ValidationError(MAX_DEPTH_ERROR_MESSAGE)

        return await self.create(session, data)

    async def update_activity(
        self,
        session: AsyncSession,
        activity_id: UUID,
        data: UpdateActivityRequestSchema,
    ) -> ActivityResponseSchema:
        if data.parent_id is not None:
            if data.parent_id == activity_id:
                raise ValidationError(SELF_REFERENCE_ERROR_MESSAGE)

            parent_depth = await self._get_activity_depth(session, data.parent_id)
            if parent_depth >= MAX_ACTIVITY_DEPTH:
                raise ValidationError(MAX_DEPTH_ERROR_MESSAGE)

        return await self.update(session, data, activity_id)
