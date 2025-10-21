class EvidentlyError(Exception):
    def get_message(self):
        return f"{self.__class__.__name__}: {self}"

class NotSupportedError(Exception):
    """raised when function is supported in main Evidently version but not this slim version"""
    def get_message(self):
        return f"{self.__class__.__name__}: {self}"
