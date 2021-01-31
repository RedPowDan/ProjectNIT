import datetime

from marshmallow import Schema, fields, pre_load, post_load


class Response(Schema):
    time = fields.DateTime(required=True)


if __name__ == '__main__':
    time = datetime.datetime.utcnow().isoformat()
    print(time)
    print(type(time))

    request = {
        'time': time
    }

    response = Response().load(request)
    print(response)
    print(response['time'])
    print(type(response['time']))
