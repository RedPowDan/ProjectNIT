from transport.sanic.endpoints import BaseEndpoint
from db.database import DBSession


def only_self(*, status_error: int = 403):
    def decorator(func):
        def wrapped(*args, **kwargs):
            if kwargs["token"].get('eid') != kwargs["eid"]:
                return BaseEndpoint.make_response_json(status=status_error)
            return func(*args, **kwargs)

        return wrapped

    return decorator


def only_received_messages(*, status_error: int = 403):
    def decorator(func):
        def wrapped(session: DBSession, *args, **kwargs):
            message = session.get_message_by_id(message_id=kwargs["message_id"])
            if kwargs["token"].get('eid') != message.recipient_id:
                return BaseEndpoint.make_response_json(status=status_error)
            return func(session, *args, **kwargs)

        return wrapped

    return decorator


def only_sent_messages(*, status_error: int = 403, message_status: str = ""):
    def decorator(func):
        def wrapped(*args, **kwargs):
            message = args.get_message_by_id(message_id=kwargs["message_id"])
            if kwargs["token"].get('eid') != message.sender_id:
                return BaseEndpoint.make_response_json(message=message_status, status=status_error)
            return func(*args, **kwargs)

        return wrapped

    return decorator
