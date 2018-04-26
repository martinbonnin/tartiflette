import sys
import asyncio
import logging
import time
import json
from aiohttp import web

from tests.examples.app.resolvers import TTFTT as tartiflette

logger = logging.getLogger(__name__)

async def _post_handler(req):
    start = time.time()

    try:
        req_content = await req.json(loads=json.loads)
        variables = req_content.get("variables", {})
        operation_name = req_content.get('operationName')

        print(variables)
        print(req_content["query"])

        data = await tartiflette.execute(req_content["query"], context={}, variables=variables)

        return web.Response(
            body=data,
            headers={
                "X-RESPONSE-TIME": "%s" % (time.time() - start)
            },
            content_type="application/json"
        )

    finally:
        logger.info(
            "It took %s",
            time.time() - start
        )

async def _options_handler(req):
    return web.Response(headers={
        "access-control-allow-credentials": "true",
        "access-control-allow-headers": "authorization,content-type,x-dm-davos",
        "access-control-allow-methods": "POST",
        "access-control-allow-origin": "http://hub.dm.gg",
        "access-control-expose-headers": "X-DM-API-Backend-Response-Time, X-DM-API-Edge, X-DM-API-Name, X-DM-API-Version, X-DM-API-Endpoint, X-DM-API-GraphQL-HasError, X-DM-To-Cache, X-DM-Log-URL, X-DM-Tracing-URL, X-DM-API-CDN-Name, authorization,content-type,x-dm-davos"
    })

def run():
    loop = asyncio.get_event_loop()

    # Init aiohttp
    app = web.Application()

    app.router.add_route('POST', '/', _post_handler)
    app.router.add_route('OPTIONS', '/', _options_handler)

    app_handler = app.make_handler()

    srv = loop.run_until_complete(
        loop.create_server(app_handler, '127.0.0.1', '8080')
    )

    try:
        loop.run_forever()
    except Exception as e:  # pylint: disable=broad-except
        logger.exception(e)
    except KeyboardInterrupt:  # CTRL+C (SIGINT) Here
        logger.info('Why did you CTRL+C me ?')
    finally:
        logger.info('Closing Server ...')
        srv.close()
        logger.info('Stopping Accepting Connections ...')
        loop.run_until_complete(srv.wait_closed())
        logger.info('Sending Application SHUTDOWN Event ...')
        loop.run_until_complete(app.shutdown())
        logger.info('Closing Accepted Connections (60s) ...')
        loop.run_until_complete(
            # 60 is the value recommended by aiohttp doc
            app_handler.shutdown(60.0)
        )
        logger.info('Calling Registered Application Finalizer ...')
        loop.run_until_complete(app.cleanup())
        logger.info('Seeya')

    loop.close()
    return 0


if __name__ == "__main__":
    sys.exit(run())
