class ValidationException(Exception):
    details: list[str] | str

    def __init__(self, details: list[str]):
        super().__init__(details[0] if len(details) == 1 else details)


class BreakAllLoops(Exception):
    pass
