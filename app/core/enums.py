from enum import Enum


class TaskStatus(str, Enum):
    open = 'open'
    close = 'close'


class TaskPriority(str, Enum):
    low = 'low'
    high = 'high'


class UserRole(str, Enum):
    admin = 'admin'
    user = 'user'