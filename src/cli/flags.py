from utils import Singleton


class RefreshContractsFlag(metaclass=Singleton):
    def __init__(self):
        self.flag: bool = True

    @property
    def flag(self) -> bool:
        return self._refresh_contracts

    @flag.setter
    def flag(self, value: bool) -> None:
        self._refresh_contracts = value


class RefreshProjectsFlag(metaclass=Singleton):
    def __init__(self):
        self.flag: bool = True

    @property
    def flag(self) -> bool:
        return self._refresh_projects

    @flag.setter
    def flag(self, value: bool) -> None:
        self._refresh_projects = value
