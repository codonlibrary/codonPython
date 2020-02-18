from requests.exceptions import ConnectionError


class MESHAuthenticationError(ConnectionError):
    """The MESH request authentication was invalid"""

    @property
    def msg(self):
        return "Invalid authentication"


class MESHMessageMissing(ConnectionError):
    """The message requested does not exist"""

    @property
    def msg(self):
        return "Message does not exist"


class MESHMessageAlreadyDownloaded(ConnectionError):
    """The MESH request has already been downloaded"""

    @property
    def msg(self):
        return "Message already downloaded"


class MESHDownloadErrors(Exception):
    """There were errors downloading MESH messages"""

    def __init__(self, exceptions):
        self.exceptions = exceptions


class MESHInvalidRecipient(ConnectionError):
    """The recipient is unknown or otherwise invalid"""

    @property
    def msg(self):
        return "Invalid recipient"


class MESHMultipleMatches(ConnectionError):
    """There are multiple messages with the provided local ID"""

    @property
    def msg(self):
        return "Multiple messages found"


class MESHUnknownError(ConnectionError):
    """There was an unknown error with the connection"""

    @property
    def msg(self):
        return "Unknown"
