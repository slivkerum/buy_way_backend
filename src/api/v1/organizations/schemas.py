from pydantic import BaseModel

from apps.users.entities.organizations import (
    OrganizationEntity,
)


class OrganizationResponseSchema(BaseModel):
    id: int  # noqa
    name: str

    @classmethod
    def from_entity(cls, organization_entity: OrganizationEntity) -> 'OrganizationResponseSchema':
        return cls(
            id=organization_entity.id,
            name=organization_entity.name,
        )
