class StatusCode(object):
    # Success codes
    SUCCESS = 0
    CONNECTION_FORMED = 1

    # Error codes
    UNSUPPORTED_COMMAND = -1
    UNSUPPORTED_OS = -2
    UNSPECIFIED_COMMAND = -3
    INVALID_JSON = -4
    PLUGIN_NOT_FOUND = -5
    PLUGIN_ERROR_UNKNOWN = -6

    success_messages = {
        SUCCESS: "Success",
        CONNECTION_FORMED: "Connection formed",
    }

    error_messages = {
        UNSUPPORTED_COMMAND: "The command supplied is unsupported.",
        UNSUPPORTED_OS: "This operating system is currently unsupported for the action you wish to take.",
        UNSPECIFIED_COMMAND: "No command was specified.",
        INVALID_JSON: "The JSON received by the server was invalid.",
        PLUGIN_NOT_FOUND: "The requested plugin was not found.",
        PLUGIN_ERROR_UNKNOWN: "An unknown error occurred within the plugin.",
    }

    @staticmethod
    def status_message(status_code):
        """
        Gets the corresponding status message for the supplied status code
        :param status_code: A status code
        :type status_code: int
        :return: A human readable status message
        :rtype: None
        """
        if status_code >= 0:
            return StatusCode.success_messages[status_code]
        else:
            return StatusCode.error_messages[status_code]

    @staticmethod
    def status_dict(status_code):
        """
        Creates a status dictionary for the supplied status code
        :param status_code: A status code
        :type status_code: int
        :return: A dictionary of information about the status
        :rtype: dict
        """
        return {
            "type": "error" if status_code < 0 else "info",
            "code": status_code,
            "message": StatusCode.status_message(status_code),
            "further_info": ""
        }
