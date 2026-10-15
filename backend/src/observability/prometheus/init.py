from __future__ import annotations

from typing import TYPE_CHECKING

from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest, multiprocess
from starlette.responses import Response

if TYPE_CHECKING:
    from fastapi import FastAPI


def init_prometheus(app: FastAPI) -> None:
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)  # type: ignore[no-untyped-call]

    @app.get("/metrics", include_in_schema=False)
    @app.get("/metrics/", include_in_schema=False)
    def metrics_endpoint() -> Response:
        return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

