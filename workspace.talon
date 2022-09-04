os: windows
-
work [space] show: key(win-tab)
work space new: key(win-ctrl-d)
work space close: key(win-ctrl-f4)

work <number>: user.workspace_go(number)
work next [<number>]: user.workspace_next(number or 1)
work previous [<number>]: user.workspace_previous(number or 1)
work send <number>: user.workspace_send(number)
work move <number>: user.workspace_move(number)

window pin: user.window_pin()
window unpin: user.window_unpin()

application pin: user.app_pin()
application unpin: user.app_unpin()

(window | win) (folk | focus) <number>: user.window_focus_grid_pos(number)
(window | win) (folk | focus) left: user.window_focus_grid_pos(4)
(window | win) (folk | focus) right: user.window_focus_grid_pos(6)

focus next [<number>]: user.window_next(number or 1)
