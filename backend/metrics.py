import time
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter("api_requests_total", "Total count of requests by method and path.", ["method", "path", "status_code"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency in seconds", ["method", "path"])

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path

        start_time = time.time()
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            raise e
        finally:
            process_time = time.time() - start_time
            REQUEST_COUNT.labels(method=method, path=path, status_code=status_code).inc()
            REQUEST_LATENCY.labels(method=method, path=path).observe(process_time)

        return response

def metrics_endpoint():
    return Response(generate_latest(), media_type="text/plain")
