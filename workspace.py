from talon import Module, ui, Context, actions
import logging
from win32gui import GetWindowRect

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

    def app_pin():
        """Pin the current app, making all its windows active in all workspaces"""
        AppView.current().pin_app()

    def app_unpin():
        """Unpin the current app"""
        AppView.current().unpin_app()

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
            # talon caches Window.rect, so get the latest position from Windows
            left, top, right, bottom = GetWindowRect(a.hwnd)
            if (x >= left and x <= right) and (y >= top and y <= bottom):
                windows[a.hwnd].focus()
                # This seems more robust
                # a.switch_to()
                return

    def window_focus_grid_pos(n: int):
        """Switch to the highest window that contains the 1-9 grid position n"""
        s = ui.main_screen()
        x_max, y_max = s.width, s.height
        x_third, x_sixth = x_max // 3, x_max // 6
        y_third, y_sixth = y_max // 3, y_max // 6
        x_offset = (n-1) % 3
        y_offset = (n-1) // 3
        x_pos = x_offset * x_third + x_sixth
        y_pos = y_offset * y_third + y_sixth
        actions.user.window_focus_pos(x_pos, y_pos)
