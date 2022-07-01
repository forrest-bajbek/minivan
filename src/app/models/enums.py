from enum import Enum, unique


@unique
class TaskEnvEnum(str, Enum):
    PROD: str = "prod"
    STG: str = "stg"
    DEV: str = "dev"


@unique
class TaskStatusEnum(str, Enum):
    START: str = "start"
    COMPLETE: str = "complete"
    FAIL: str = "fail"


@unique
class ScopeEnum(str, Enum):
    READ: str = "read"
    WRITE: str = "write"

    @classmethod
    def allowed_values(cls):
        return [item.value for item in cls.__members__.values()]


@unique
class UserCategoryEnum(str, Enum):
    HUMAN: str = "human"
    ROBOT: str = "robot"
