from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException, \
    DBMessageNotExistsException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicMessageNotFound


class MessageEndpoint(BaseEndpoint):

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestPatchMessageDto(body)

        try:
            db_message = message_queries.patch_message(session, request_model, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if db_message.sender_id != token.get("eid"):
            return await self.make_response_json(status=403, message="Forbidden")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            db_message = message_queries.delete_message(session, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if db_message.sender_id != token.get("eid"):
            return await self.make_response_json(status=403, message="Forbidden")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        try:
            message = message_queries.get_message(session, message_id=message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        employee_id = token["eid"]
        if message.sender_id != employee_id and message.recipient_id != employee_id:
            return await self.make_response_json(status=403, message="Forbidden")

        response_message = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_message.dump())
