from talon import Module, ui, Context
import logging

# https://github.com/mrob95/py-VirtualDesktopAccessor
# talon/bin/pip.bat install pyvda
from pyvda import AppView, get_apps_by_z_order, VirtualDesktop

# Disable log spam
logging.getLogger("comtypes").setLevel(logging.INFO)

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def workspace_send(n: int):
        """Send the current window to a given workspace"""
        AppView.current().move(VirtualDesktop(n))

    def workspace_move(n: int):
        """Send the current window to a given workspace, and follow it"""
        target = VirtualDesktop(n)
        AppView.current().move(target)
        target.go()

    def workspace_go(n: int):
        """Go to a given workspace"""
        VirtualDesktop(n).go()

    def workspace_next(n: int):
        """Go to the next workspace (without animation)"""
        current = VirtualDesktop.current()
        VirtualDesktop(current.number + 1).go()

    def workspace_previous(n: int):
        """Go to the previous workspace (without animation)"""
        current = VirtualDesktop.current()
        VirtualDesktop(current.number - 1).go()

    def window_pin():
        """Pin the current window, making it active in all workspaces"""
        AppView.current().pin()

    def window_unpin():
        """Unpin the current window"""
        AppView.current().unpin()

    def window_next(n: int):
        """Switch to the window that is `n` windows beneath the active window"""
        windows = {w.id: w for w in ui.windows()}
        windows_by_z = get_apps_by_z_order()
        target = windows_by_z[n % len(windows_by_z)]
        windows[target.hwnd].focus()
        target.switch_to()

    def window_focus_pos(x: int, y: int):
        """Switch to the highest window that contains the point (x, y)"""
        windows = {w.id: w for w in ui.windows()}
        for a in get_apps_by_z_order():
            if windows[a.hwnd].rect.contains(x, y):
                windows[a.hwnd].focus()
                # This seems more robust
                a.switch_to()
                return

    def focus_window(hwnd: str):
        """"""
        window_map[hwnd].focus()

mod.list("windows")

APP_NAME_MAP = {
    "Visual Studio Code": "code",
    "cmd.exe": "command",
    "brave.exe": "brave",
    "WindowsTerminal.exe": "terminal",
    "explorer.exe": "explorer",
    "Windows Explorer": "explorer",
}

window_map = {}

def refresh_windows_in_workspace(window):
    global window_map
    relevant = [w.hwnd for w in get_apps_by_z_order()]
    if len(relevant) > 1:
        # Don't count current window
        relevant = relevant[1:]
    windows = [w for w in ui.windows() if w.id in set(relevant)]
    window_map = {str(w.id): w for w in windows}
    ctx.lists["user.windows"] = {
        APP_NAME_MAP.get(w.app.name, w.app.name): str(w.id)
        for w in windows
    }

# ui.register("win_title", refresh_windows_in_workspace)
ui.register("win_focus", refresh_windows_in_workspace)
