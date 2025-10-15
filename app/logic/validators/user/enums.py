import enum


class UserValidationStates(enum.Enum):
    EMAIL_UNIQUE = 'EMAIL_UNIQUE'
    USER_EXISTS = 'USER_EXISTS'