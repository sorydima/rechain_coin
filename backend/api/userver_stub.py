"""Simple userver backend stub for future integration.

This module is a placeholder for a userver-based HTTP/gRPC service that will
serve node metadata and control endpoints.
"""

from aiohttp import web

async def handle_info(request):
    return web.json_response({'status': 'ok', 'node_id': 'stub'})

async def init_app():
    app = web.Application()
    app.router.add_get('/info', handle_info)
    return app

if __name__ == '__main__':
    web.run_app(init_app(), port=8080)
