class TaskException(Exception):
    pass


class NoTasksToProcess(TaskException):
    pass


class TaskFromJsonLoadingError(TaskException):
    pass


class TaskFromFileLoadingError(TaskException):
    pass


class UnknownTaskReceived(TaskException):
    pass


class ResultTaskContentMismatch(TaskException):
    pass


class SavingResultTaskError(TaskException):
    pass