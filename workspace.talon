os: windows
-
show work [spaces]: key(win-tab)
new work [space]: key(win-ctrl-d)
close work space: key(win-ctrl-f4)
next work [space] [<number>]: user.workspace_next(number or 1)
previous work [space] [<number>]: user.workspace_previous(number or 1)

work [space] <number>: user.workspace_go(number)

send work [space] <number>: user.workspace_send(number)
move work [space] <number>: user.workspace_move(number)

window pin: user.window_pin()
window unpin: user.window_unpin()

window next [<number>]: user.window_next(number or 1)
(window | win) (folk | focus) (left | lease): user.window_focus_pos(400, 501)
(window | win) (folk | focus) (right | ross): user.window_focus_pos(1441, 551)