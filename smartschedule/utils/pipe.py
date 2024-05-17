from functools import reduce
from typing import Any, Callable, overload


@overload
def pipe[A, B](fn_1: Callable[[A], B], /) -> Callable[[A], B]: ...


@overload
def pipe[A, B, C](
    fn_1: Callable[[A], B], fn_2: Callable[[B], C], /
) -> Callable[[A], C]: ...


@overload
def pipe[A, B, C, D](
    fn_1: Callable[[A], B], fn_2: Callable[[B], C], fn_3: Callable[[C], D], /
) -> Callable[[A], D]: ...


def pipe(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def piped(arg: Any) -> Any:
        return reduce(lambda prev_fn, next_fn: next_fn(prev_fn), fns, arg)

    return piped
