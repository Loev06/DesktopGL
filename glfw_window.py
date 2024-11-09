import glfw
import ctypes
from ctypes import wintypes
import screeninfo

from logging_format import logger

user32 = ctypes.windll.user32

class GLFWWindow:
    def __init__(self, monitor: screeninfo.Monitor, offset_monitor: screeninfo.Monitor):
        self.window = self.create_window()
        self.bind_to_desktop()
        self.show_window(monitor, offset_monitor)
    
    def create_window(self) -> glfw._GLFWwindow:
        logger.info("Initializing GLFW")
        if not glfw.init():
            logger.error("Failed to initialize GLFW")
            raise RuntimeError("Failed to initialize GLFW")

        glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.FOCUSED, False)
        glfw.window_hint(glfw.DECORATED, False)
        # glfw.window_hint(glfw.AUTO_ICONIFY, False)
        # glfw.window_hint(glfw.VISIBLE, False)

        window = glfw.create_window(640, 480, "DesktopGL", None, None)
        if not window:
            glfw.terminate()
            raise RuntimeError("Failed to create window")
        
        logger.info("Window created")
        
        glfw.make_context_current(window)
        return window
    
    def bind_to_desktop(self):
        # https://www.codeproject.com/Articles/856020/Draw-Behind-Desktop-Icons-in-Windows-8plus

        # handle to the program manager
        program_hwnd = user32.FindWindowW("Progman", None)

        # Send 0x052C to the program manager
        # This message directs the program manager to spawn a WorkerW behind the desktop icons.
        # If it is already there, nothing happens.
        user32.SendMessageTimeoutW(
            program_hwnd,
            0x052C,
            ctypes.c_ulong(0),
            None,
            0,
            1000,
            ctypes.byref(ctypes.c_ulong())
        )

        # Find the WorkerW
        
        # EnumWindowsProc callback function
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        # We enumerate all Windows, until we find one, that has the SHELLDLL_DefView as a child. 
        # If we found that window, we take its next sibling and assign it to workerw.
        self.workerw = None
        def callback(hwnd: int, lparam: int) -> bool:
            if user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None):
                self.workerw = user32.FindWindowExW(0, hwnd, "WorkerW", None)
            return True
        user32.EnumWindows(WNDENUMPROC(callback), 0)

        # Set created window to be a child of WorkerW
        hwnd = glfw.get_win32_window(self.window)
        user32.SetParent(hwnd, self.workerw)

    def show_window(self, monitor: screeninfo.Monitor, offset: screeninfo.Monitor):
        # glfw window pos is relative to monitors[0]
        # Windows window pos is relative to the primary monitor
        glfw.set_window_pos(
            self.window,
            monitor.x - offset.x,
            monitor.y - offset.y + monitor.height // 2
        )
        glfw.set_window_size(self.window, monitor.width, monitor.height)
        glfw.show_window(self.window)

    def render(self):
        pass
    
    def swap(self):
        glfw.poll_events()
        glfw.swap_buffers(self.window)

    def __del__(self):
        user32.SetParent(self.workerw, 0)
        glfw.terminate()
    
    def is_running(self) -> bool:
        return not glfw.window_should_close(self.window)
