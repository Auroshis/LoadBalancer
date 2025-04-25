from fastapi import Request, APIRouter
from fastapi.responses import Response
import uuid
import httpx

def create_router(balancer, config, logger):
    router = APIRouter()

    @router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def handle(full_path: str, request: Request):
        trace_id = str(uuid.uuid4())
        target = balancer.get_server_round_robin()
        url = f"http://{target}/{full_path}"

        headers = dict(request.headers)
        headers["X-Trace-ID"] = trace_id

        body = await request.body()
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method=request.method,
                    url=url,
                    headers=headers,
                    content=body,
                    timeout=float(config.get("request_timeout", 5))
                )
            return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
            media_type=resp.headers.get("content-type")
        )
        except Exception as e:
            logger.error(f"[{trace_id}] Failed to route: {e}")
            return {"error": "backend unavailable"}, 503

    return router
