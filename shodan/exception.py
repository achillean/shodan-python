class APIError(Exception):
    """This exception gets raised whenever a non-200 status code was returned by the Shodan API."""

    def __init__(self, value, status_code=0):
        self.value = value
        self.status_code = status_code

    def __str__(self):
        return self.value


class APITimeout(APIError):
    pass
