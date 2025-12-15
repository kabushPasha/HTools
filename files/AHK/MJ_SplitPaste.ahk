#Requires AutoHotkey v2.0

^+v:: {   ; Ctrl+Shift+V
    ClipWait(1)
    src_test := A_Clipboard

    ; Split on ---- (with optional newlines around it)
	text := StrReplace(src_test, "`r`n", "`n")
    text := StrReplace(text, "`r", "`n")  ; just in case
	
    parts := StrSplit(text, "`n----`n")

    for part in parts {
        cleaned := Trim(part)
        if cleaned != "" {
            ;SendText cleaned
			A_Clipboard := cleaned ;
			ClipWait		
			Send "{Ctrl Up}{Shift Up}"			
			Send "^v"
            Send "{Enter}"
            Sleep 500
        }
    }
	
	A_Clipboard := src_test ;
}