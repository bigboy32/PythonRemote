import platform


class SystemInfo(object):
    """A class for easily accessing all system information"""

    @staticmethod
    def get_os():
        return platform.system()

    @staticmethod
    def is_windows():
        return SystemInfo.get_os() == "Windows"

    @staticmethod
    def is_mac():
        return SystemInfo.get_os() == "Darwin"

    @staticmethod
    def is_linux():
        return SystemInfo.get_os() == "Linux"
