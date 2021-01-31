class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBEmployeeExistsException(Exception):
    pass


class DBEmployeeNotExistsException(Exception):
    status_code = 403


class DBMessageNotExistsException(Exception):
    status_code = 403
