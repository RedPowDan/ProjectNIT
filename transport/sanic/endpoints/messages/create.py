from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicEmployeeNotFound

from db.queries import message as message_queries
from db.exceptions import DBDataException, DBIntegrityException, DBEmployeeNotExistsException


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            message = message_queries.create_message(session, request_model, token.get("eid"))
        except DBEmployeeNotExistsException:
            raise SanicEmployeeNotFound("Employee not found")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())
