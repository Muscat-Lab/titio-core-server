import enum


class AuthPermission(str, enum.Enum):
    PerformanceCreate = "PerformanceCreate"
    PerformanceUpdate = "PerformanceUpdate"
    PerformanceDelete = "PerformanceDelete"
