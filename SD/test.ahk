
#If GetKeyState("ScrollLock", "T")

#z::Run cmd
;#c::MsgBox You pressed Win-C while Notepad is active.
RAlt::+AppsKey

#If

#c::
MouseClickDrag, Left, 0, 0, -100, 0, , R
MouseMove, 100,0,,R
Click
;winwaitactive
;SendInput ^F4
return





#v::
InputBox, OutputVar, Question 1, What is your first name?
if (OutputVar = "Bill")
    MsgBox, That's an awesome name`,, %OutputVar%.

InputBox, OutputVar2, Question 2, Do you like AutoHotkey?
if (OutputVar2 = "yes")
    MsgBox, Thank you for answering %OutputVar2%`, %OutputVar%! We will become great friends.
else
    MsgBox, %OutputVar%`, That makes me sad.
return

