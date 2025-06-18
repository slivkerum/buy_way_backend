from pydantic import BaseModel

from apps.users.entities.organizations import (
    OrganizationEntity
)



class OrganizationDocumentsResponseSchema(BaseModel):
    id: int
    name: str
    path: str


class OrganizationResponseSchema(BaseModel):
    id: int  # noqa
    name: str
    documents: list[OrganizationDocumentsResponseSchema]

    @classmethod
    def from_entity(cls, organization_entity: OrganizationEntity) -> 'OrganizationResponseSchema':
        return cls(
            id=organization_entity.id,
            name=organization_entity.name,
            documents=[
                OrganizationDocumentsResponseSchema(
                    id=doc.id,
                    name=doc.name,
                    path=doc.path
                )
                for doc in organization_entity.documents
            ]
        )


class OrganizationRequestSchema(BaseModel):
    name: str