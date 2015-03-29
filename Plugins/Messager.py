from Tkinter import *
import tkMessageBox
from Plugin import *
from SystemInfo import *
from StatusCode import *
from Utilities import *


class Messager(Plugin):
    """Allows messages to be received and displayed to the current user"""

    id = "messager"

    def __init__(self):
        Plugin.__init__(self)

    def run(self, callback, args):
        # TODO: Support linux
        # Arguments should have a 'type' key which can be any of:
        # 'abortretryignore','ok','okcancel','retrycancel','yesno','yesnocancel'
        if SystemInfo.get_os() in ["Windows", "Darwin"]:
            window = Tk()
            window.wm_withdraw()
            # center the window on the main screen
            window.geometry("1x1+" + str(window.winfo_screenwidth() / 2) + "+" + str(window.winfo_screenheight() / 2))
            # noinspection PyProtectedMember
            answer = tkMessageBox._show(type=args['type'], title=args['title'], message=args['message'], icon=None, )
            callback(self, StatusCode.SUCCESS, {"answer": answer})
        else:
            callback(self, StatusCode.UNSUPPORTED_OS, None)
            Logger().critical('Unsupported OS')