from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=('GET', 'POST'),
        ),
        endpoints.CreateEmployeeEndpoint(
            config, context, uri='/user', methods=['POST'],
        ),
        endpoints.AuthEmployeeEndpoint(
            config, context, uri='/auth', methods=['POST'],
        ),
        endpoints.EmployeeEndpoint(
            config, context, uri='/user/<eid:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.AllEmployeeEndpoint(
            config, context, uri='/user/all', methods=['GET'], auth_required=True,
        ),
        endpoints.CreateMessageEndpoint(
            config, context, uri='/msg', methods=['POST'], auth_required=True,
        ),
        endpoints.MessageEndpoint(
            config, context, uri='/msg/<message_id:int>', methods=['GET', 'PATCH', 'DELETE'], auth_required=True,
        ),
        endpoints.AllMessageEndpoint(
            config, context, uri='/msg', methods=['GET'], auth_required=True,
        )
    )
