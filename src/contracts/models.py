from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.base import Base

if TYPE_CHECKING:
    from projects.models import Project


class Status(str, Enum):
    DRAFT = "Черновик"
    ACTIVE = "Активен"
    COMPLETED = "Завершен"


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    signed_at: Mapped[datetime | None] = mapped_column(default=None)
    status: Mapped[Status] = mapped_column(default=Status.DRAFT)

    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id"), default=None)

    project: Mapped["Project"] = relationship(back_populates="contracts")
