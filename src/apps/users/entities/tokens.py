from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'


@dataclass
class TokenEntity:
    subject_id: str
    token_type: TokenType
    jti: str
    expires_at: datetime


@dataclass
class TokenPairEntity:
    access_token: str
    refresh_token: str
