"""Simple APM/OpenTelemetry initializer.

This initializes OpenTelemetry tracing and exports to OTLP if configured via
environment variables. It's designed to be optional and lightweight for demos.
"""
import os
from typing import Optional

from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
except Exception:
    # OpenTelemetry is optional — if deps aren't installed, APM init becomes a no-op.
    trace = None


def init_app(app: Optional[FastAPI] = None) -> None:
    otlp_endpoint = settings.otel_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if trace is None or not otlp_endpoint:
        return

    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
