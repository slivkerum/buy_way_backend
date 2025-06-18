import uuid
from http import HTTPStatus

from django.http import HttpRequest

from ninja import Router
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja import File, Form

from api.schemas import ApiResponse
from api.v1.organizations.schemas import OrganizationResponseSchema, OrganizationRequestSchema
from api.v1.users.handlers import AuthBearer
from apps.common.exceptions import ServiceException
from apps.users.entities.organizations import OrganizationEntity, OrganizationDocumentsEntity
from apps.users.entities.users import UserEntity
from apps.users.models import User, Organization
from apps.users.services.organizations import BaseOrganizationService
from apps.users.services.users import BaseUserService
from config.containers import get_container


router = Router(tags=['Организации'])


@router.post('create_organization', response={HTTPStatus.CREATED: OrganizationResponseSchema}, auth=AuthBearer())
def create_organization(
    request: HttpRequest,
    schema: OrganizationRequestSchema,
):
    container = get_container()
    organization_service: BaseOrganizationService = container.resolve(BaseOrganizationService)
    user_service: BaseUserService = container.resolve(BaseUserService)

    organization_entity = OrganizationEntity(
        id=None,
        name=schema.name,
        is_active=False,
        documents=[]
    )

    try:
        user_entity = user_service.get_user_by_id(request.user.id)
        user_model = User.objects.get(id=user_entity.id)

        organization = organization_service.create_organization(organization_entity)
        organization_model = Organization.from_entity(organization)
        organization_model.save()

        user_model.organization = organization_model
        user_model.save()

        user_entity.organization = organization
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return OrganizationResponseSchema.from_entity(organization)


@router.post('add_documents/', response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def add_documents(
    request: HttpRequest,
    name: str = Form(...),
    file: UploadedFile = File(...)
):
    container = get_container()
    organization_service: BaseOrganizationService = container.resolve(BaseOrganizationService)

    user = request.user
    if not user.organization:
        raise HttpError(HTTPStatus.BAD_REQUEST, "У пользователя нет организации")

    org_id = user.organization

    document_entity = OrganizationDocumentsEntity(
        id=None,
        name=name,
        path=file.name,
    )

    try:
        organization_service.add_documents(org_id=org_id.id, document=document_entity, file=file)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=None)


@router.delete('delete_document/{document_id}/', response={HTTPStatus.OK: ApiResponse}, auth=AuthBearer())
def delete_document(
    request: HttpRequest,
    document_id: int,
):
    container = get_container()
    organization_service: BaseOrganizationService = container.resolve(BaseOrganizationService)

    user = request.user
    if not user.organization:
        raise HttpError(HTTPStatus.BAD_REQUEST, "У пользователя нет организации")

    org_id = user.organization.id

    try:
        organization_service.remove_documents(org_id=org_id, document_id=document_id)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=None)