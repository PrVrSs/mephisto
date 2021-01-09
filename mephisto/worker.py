from typing import Any, NamedTuple

from .tracer import Tracer


class WorkerResult(NamedTuple):
    output: Any = None
    trace_data: Any = None
    exception: Any = None


def worker(*args, __callback__, **kwargs):
    with Tracer() as tracer:
        try:
            return WorkerResult(output=__callback__(*args, **kwargs), trace_data=tracer.data)
        except Exception as exc:
            return WorkerResult(exception=exc, trace_data=tracer.data)
