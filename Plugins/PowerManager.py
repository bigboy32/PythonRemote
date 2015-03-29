import os

from Plugin import *
from SystemInfo import *
from StatusCode import *
from Utilities import *


class PowerManager(Plugin):
    """The first example class for the python powered remote interface for my computer"""

    id = "power_manager"

    def __init__(self):
        Plugin.__init__(self)

    def run(self, callback, args):
        # args is a dictionary of commands and data

        if SystemInfo.is_mac():
            if args['option'] in ['sleep', 'hibernate']:
                callback(self, StatusCode.SUCCESS, None)
                os.system("osascript -e 'tell application \"System Events\" to sleep'")
            else:
                callback(self, StatusCode.UNSUPPORTED_COMMAND, {"error": "Unsupported command"})
                Logger().error("Unsupported command: " + args['option'])

        elif SystemInfo.is_windows():
            if args['option'] in ['sleep', 'hibernate']:
                callback(self, StatusCode.SUCCESS, None)
                os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
            elif args['option'] == 'shutdown':
                callback(self, StatusCode.SUCCESS, None)
                os.system(r'%windir%\system32\rundll32.exe shell32.dll,SHExitWindowsEx 4')
            elif args['option'] == 'restart':
                callback(self, StatusCode.SUCCESS, None)
                os.system(r'%windir%\system32\rundll32.exe shell32.dll,SHExitWindowsEx 2')
            elif args['option'] == 'logoff':
                callback(self, StatusCode.SUCCESS, None)
                os.system(r'%windir%\system32\rundll32.exe shell32.dll,SHExitWindowsEx 0')
            elif args['option'] == 'lock':
                callback(self, StatusCode.SUCCESS, None)
                os.system(r'%windir%\System32\rundll32.exe user32.dll,LockWorkStation')
            else:
                callback(self, StatusCode.UNSUPPORTED_COMMAND, {"error": "Unsupported command"})
                Logger().error("Unsupported command: " + args['option'])

        elif SystemInfo.is_linux():
            callback(self, StatusCode.UNSUPPORTED_OS, None)
            Logger().error("Unsupported OS for: '" + args['option'] + "'")

        else:
            callback(self, StatusCode.UNSUPPORTED_OS, None)
            Logger().error("Unsupported operating system")