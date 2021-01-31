import datetime
from typing import List

from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeExistsException, DBEmployeeNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, sender_id: int) -> DBMessage:
    recipient = session.get_employee_by_login(login=message.recipient)

    if recipient is None:
        raise DBEmployeeNotExistsException

    new_message = DBMessage(
        sender_id=sender_id,
        recipient_id=recipient.id,
        message=message.message
    )

    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, message_id: int) -> DBMessage:
    pass
    db_message = None

    if message_id is not None:
        db_message = session.get_message_by_id(message_id)

    if db_message is None:
        raise DBMessageNotExistsException

    return db_message


def get_messages(session: DBSession, recipient_id: int) -> List['DBMessage']:

    recipient = session.get_employee_by_id(eid=recipient_id)

    if recipient is None:
        raise DBEmployeeNotExistsException()

    return session.messages().filter(DBMessage.recipient_id == recipient_id)


def patch_message(session: DBSession, message, message_id: int) -> DBMessage:

    db_message = session.get_message_by_id(message_id)

    if db_message is None:
        raise DBMessageNotExistsException()

    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    db_message.update_at = datetime.datetime.utcnow()

    return db_message


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    pass
    db_message = session.get_message_by_id(message_id=message_id)

    if db_message is None:
        raise DBMessageNotExistsException()

    session.delete_model(db_message)

    return db_message

    # db_employee = session.get_employee_by_id(employee_id)
    # db_employee.is_delete = True
    # return db_employee



