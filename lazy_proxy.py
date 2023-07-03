from collections import UserString
from typing import Any, Dict


class LazyProxy(UserString):
    key: str
    kwargs: Dict[str, Any]

    def __init__(  # noqa
        self, key: str, **kwargs: Any
    ) -> None:
        self.key = key
        self.kwargs = kwargs

    @property
    def data(self) -> str:  # type: ignore[override]
        from context import I18n

        context = I18n.get_current()
        if context:
            return context.get(key=self.key, **self.kwargs)
        return self.key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<'{self.key}'>"
