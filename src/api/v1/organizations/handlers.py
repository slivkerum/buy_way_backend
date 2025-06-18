from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router

from api.schemas import ApiResponse
from api.v1.users.handlers import AuthBearer
from config.containers import get_container


router = Router(tags=['Организации'])