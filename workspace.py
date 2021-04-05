from talon import Module, ui
from ctypes import windll
import logging

# https://github.com/mrob95/py-VirtualDesktopAccessor
# talon/bin/pip.bat install pyvda
from pyvda import AppView, get_apps_by_z_order, VirtualDesktop

# Disable log spam
logging.getLogger("comtypes").setLevel(logging.INFO)

mod = Module()

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