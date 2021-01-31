from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicEmployeeNotFound


class AllMessageEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        print(token.get("eid"))
        try:
            db_message = message_queries.get_messages(session, recipient_id=int(token.get("eid")))
        except DBEmployeeNotExistsException:
            raise SanicEmployeeNotFound("Employee not found")

        response_model = ResponseMessageDto(db_message, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
