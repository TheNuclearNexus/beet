from inspect import stack
from typing import ClassVar

from mecha.diagnostic import Diagnostic

from beet import Context
from pydantic import BaseModel, ValidationError

from beet.core.file import JsonFileBase
from beet.library.base import NamespaceFileScope, Pack


class FooModel(BaseModel):
    bar: int


class Foo(JsonFileBase[FooModel]):
    model = FooModel

    scope: ClassVar[NamespaceFileScope] = ("foo",)

    extension: ClassVar[str] = ".json"

    def bind(self, pack: Pack, path: str):
        try:
            self.data = FooModel.model_validate(self.data)
        except ValidationError as exc:
            raise Diagnostic("error", f"Failed to validate\n{'\n'.join(map(str, exc.errors()))}")


def beet_default(ctx: Context):
    ctx.data.extend_namespace.append(Foo)
