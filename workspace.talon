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

window next [<number>]: user.window_next(number or 1)
(window | win) (folk | focus) (left | lease): user.window_focus_pos(400, 501)
(window | win) (folk | focus) (right | ross): user.window_focus_pos(1441, 551)

focus {user.windows}: user.focus_window(windows)