from talon import Module, ui
from ctypes import windll
import logging

# https://github.com/mrob95/py-VirtualDesktopAccessor
# talon/bin/pip.bat install pyvda
import pyvda

ASFW_ANY = -1

# Disable log spam
logging.getLogger("comtypes").setLevel(logging.INFO)

def go_to_n(n):
    windll.user32.AllowSetForegroundWindow(ASFW_ANY)
    pyvda.GoToDesktopNumber(n)

def get_windows_by_z():
    windows = {w.id: w for w in ui.windows()}
    windows_by_z = [windows[z] for z in pyvda.ViewGetByZOrder()]
    return windows_by_z

mod = Module()

@mod.action_class
class Actions:
    def workspace_send(n: int):
        """Send the current window to a given workspace"""
        wndh = ui.active_window().id
        pyvda.MoveWindowToDesktopNumber(wndh, n)

    def workspace_move(n: int):
        """Send the current window to a given workspace, and follow it"""
        wndh = ui.active_window().id
        pyvda.MoveWindowToDesktopNumber(wndh, n)
        go_to_n(n)

    def workspace_go(n: int):
        """Go to a given workspace"""
        go_to_n(n)

    def workspace_next(n: int):
        """Go to the next workspace (without animation)"""
        current = pyvda.GetCurrentDesktopNumber()
        go_to_n(current+n)

    def workspace_previous(n: int):
        """Go to the previous workspace (without animation)"""
        current = pyvda.GetCurrentDesktopNumber()
        go_to_n(current-n)

    def window_pin():
        """Pin the current window, making it active in all workspaces"""
        wndh = ui.active_window().id
        pyvda.PinWindow(wndh)

    def window_unpin():
        """Unpin the current window"""
        wndh = ui.active_window().id
        pyvda.UnPinWindow(wndh)

    def window_next(n: int):
        """Switch to the window that is `n` windows beneath the active window"""
        windows_by_z = get_windows_by_z()
        target = windows_by_z[n % len(windows_by_z)]
        target.app.focus()
        pyvda.ViewSwitchTo(target.id)

    def window_focus_pos(x: int, y: int):
        """Switch to the highest window that contains the point (x, y)"""
        windows = {w.id: w for w in ui.windows()}
        windows_by_z = [windows[hwnd] for hwnd in pyvda.ViewGetByZOrder()]
        for w in windows_by_z:
            if w.rect.contains(x, y):
                w.focus()
                pyvda.ViewSwitchTo(w.id)
                return