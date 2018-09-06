#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetTitleMatchMode, Regex


; is a comment
; ^ - CTRL , ! - ALT , + - SHIFT
; Hot string example
; ::flaot::float

	; HOUDINI
#IfWinActive, Houdini*
; Show reminder of all hotkeys
^F12::
txt11 =
(Ltrim Join`n
	no hotkeys currently
)
msgbox, 262208, Hotkeys,%txt11%
return



	; SUBSTANCE
#IfWinActive, Substance*
; Show reminder of all hotkeys
^F12::
txt11 =
(Ltrim Join`n
	alt + C : curvature
	alt + L : levels
	alt + B : blend
	alt + W : warp  
	alt + N : normal
	alt + T : transform
	alt + S : Slope BLur Grayscale
	alt + R : tile random
	alt + G : gradient
	alt + U : uniform color
	alt + P : polygon 2
	alt + V : bevel	
	alt + D : distance	
	shift + B : blur HQ grayscale
	shift + S : shape
	shift + H : histogram scan
	shift + E : edge detect
	shift + A : splatter
	shift + C : curve
	shift + D : directional warp
)
msgbox, 262208, Hotkeys,%txt11%
return

Tab::Space

!L:: 
Send, {Space}levels{Enter}
Return

!B:: 
Send, {Space}blend{Enter} 
Return

!W:: 
Send, {Space}warp{Enter} 
Return

!N:: 
Send, {Space}normal s{Enter} 
Return

!T:: 
Send, {Space}tr{Enter} 
Return

!S:: 
Send, {Space}Slope Blur G{Enter} 
Return

!C:: 
Send, {Space}curvature {Enter} 
Return

!R:: 
Send, {Space}tile ra{Enter} 
Return

!G:: 
Send, {Space}gra{Enter} 
Return

!P:: 
Send, {Space}polygon 2{Enter} 
Return

!U:: 
Send, {Space}uni{Enter} 
Return

!V:: 
Send, {Space}bevel{Enter} 
Return

!D:: 
Send, {Space}distance{Enter} 
Return

+B:: 
Send, {Space}blur HQ G{Enter} 
Return

+S:: 
Send, {Space}shape{Enter} 
Return

+H:: 
Send, {Space}histogram scan{Enter} 
Return

+E:: 
Send, {Space}edge{Enter} 
Return

+A:: 
Send, {Space}spla{Enter} 
Return

+C:: 
Send, {Space}c{Enter} 
Return

+D:: 
Send, {Space}directional warp{Enter} 
Return
