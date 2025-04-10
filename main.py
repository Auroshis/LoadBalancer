import uuid
from aiohttp import web, ClientSession
from balancer import LoadBalancer
from health_checker import HealthChecker

SERVERS = ["localhost:8001", "localhost:8002"]

balancer = LoadBalancer(SERVERS)
checker = HealthChecker(SERVERS, balancer)
checker.start()

async def handle_request(request: web.Request):
    try:
        target = balancer.get_server_round_robin()
        trace_id = str(uuid.uuid4())
        path = request.rel_url
        url = f"http://{target}{path}"

        headers = dict(request.headers)
        headers["X-Trace-ID"] = trace_id

        body = await request.read()

        async with ClientSession() as session:
            async with session.request(
                method=request.method,
                url=url,
                headers=headers,
                data=body,
                allow_redirects=False,
                timeout=5
            ) as resp:
                response_body = await resp.read()

                # Build response
                return web.Response(
                    status=resp.status,
                    body=response_body,
                    headers=resp.headers
                )

    except Exception as e:
        return web.Response(status=503, text=f"Error: {e}")

app = web.Application()
app.router.add_route("*", "/{tail:.*}", handle_request)

if __name__ == "__main__":
    web.run_app(app, port=8080)
