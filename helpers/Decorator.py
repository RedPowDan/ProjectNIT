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

