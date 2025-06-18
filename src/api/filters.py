from enum import Enum
from typing import Any

from ninja import Schema

from pydantic import Field


class PaginationOut(Schema):
    page: int
    page_size: int
    total: int
    total_pages: int = Field(default=0, alias='calculate_total_pages')
    has_next: bool = Field(default=None, alias='has_next_page')
    has_prev: bool = Field(default=None, alias='has_previous_page')

    @property
    def calculate_total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next_page(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous_page(self) -> bool:
        return self.page != 1


class PaginationIn(Schema):
    page: int = 1
    page_size: int = 15


class DefaultFilter(Enum):
    NOT_SET: Any
