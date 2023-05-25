from dataclasses import dataclass


@dataclass(slots=True)
class ErrorString:
    pyfile = "[ ! ]         Please Only Use Python '.py' files          [ ! ]"