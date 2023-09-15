from typing import TYPE_CHECKING

from utils.exceptions import ValidationException

if TYPE_CHECKING:
    from projects.schemas import ProjectBaseSchema


class ProjectValidator:
    def __init__(self, project_data: "ProjectBaseSchema"):
        self.project_data = project_data
        self.__errors = []

    def validate(self) -> None:
        self.validate_name()

        if self.__errors:
            raise ValidationException(self.__errors)

    def validate_name(self) -> None:
        if not isinstance(self.project_data.name, str):
            self.__errors.append(f"Имя должно быть строкой")
