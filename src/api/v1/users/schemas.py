from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from api.v1.organizations.schemas import OrganizationResponseSchema
from apps.users.entities.tokens import TokenPairEntity
from apps.users.entities.users import (
    UserEntity,
    UserRole,
)


class CredentialsRequestSchema(BaseModel):
    email: str
    password: str


class UserResponseSchema(BaseModel):
    id: UUID  # noqa
    email: str

    first_name: str
    last_name: str

    organization: Optional['OrganizationResponseSchema'] = Field(default=None)
    role: UserRole

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> 'UserResponseSchema':
        return cls(
            id=user_entity.id,
            email=user_entity.email,
            first_name=user_entity.first_name,
            last_name=user_entity.last_name,
            organization=OrganizationResponseSchema.from_entity(
                user_entity.organization
            ) if user_entity.organization else None,
            role=user_entity.role,
        )


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponseSchema

    @classmethod
    def from_entity(
            cls,
            token_pair: TokenPairEntity,
            user_entity: UserEntity,
    ) -> 'TokenResponseSchema':
        return cls(
            access_token=token_pair.access_token,
            refresh_token=token_pair.refresh_token,
            user=UserResponseSchema.from_entity(user_entity),
        )


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str
