from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.base import Base

if TYPE_CHECKING:
    from contracts.models import Contract


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str]

    contracts: Mapped[list["Contract"]] = relationship(back_populates="project")
