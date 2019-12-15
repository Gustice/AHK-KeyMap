;IMPORTANT, you must save this script as UTF-8 to make it work.

#Persistent  ; Keep the script running until the user exits it.
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Menu, Tray, Icon, shell32.dll, 75 ; Tray-Icon: Das Symbol in der Leiste. Symbole einehbar durch Iconwahl mit Quellpfad auf C:\Windows\System32\shell32.dll

Menu, Tray, Add  ; Seperator
Menu, Tray, Add, Show Help, HelpHandler

FileEncoding , UTF-8
FileInstall, KeyMap.txt, KeyMapOutput.txt, 1
return

HelpHandler:
Run  KeyMapOutput.txt
return

; Used Hotkeys:
  ; #    Win
  ; !    Alt
  ; ^    Control
  ; +    Shift
  ; <^>! AltGr
  ; * Allows extra modifiers
  ; ~ Doesn't block original hotkey

#C:: Run calc.exe ; Runs Calculator

OSD(text)
{
#Persistent
Progress, hide x1050 Y900 b1 w350 h27 zh0 FM10 cwEEEEEE ct111111,, %text%, AutoHotKeyProgressBar, Verdana BRK
WinSet, TransColor, 000000 120, AutoHotKeyProgressBar
Progress, show
SetTimer, RemoveToolTip, 2000
Return

RemoveToolTip:
SetTimer, RemoveToolTip, Off
Progress, Off
return
}


::#dt:: ; Prints current date in Format: dd.mm.yyyy
	FormatTime,Datum,,dd'.'MM'.'yyyy
	Send, %Datum% 
Return 

::#dtf:: ; Prints current date in Format: yyyy_mm_dd
	FormatTime,Datum,,yyyy_MM_dd
	Send, %Datum% 
Return

::#dts:: ; Prints current date in Format: dd.mm.yy
	FormatTime,Datum,,dd'.'MM'.'yy
	Send, %Datum% 
Return

~$NUMPADDOT:: ; Fast hits of Numpad-',' are replaced by .
IF (A_PRIORHOTKEY= "~$NUMPADDOT" AND A_TIMESINCEPRIORHOTKEY < 150)
  SEND, {BS 2}.
RETURN

^NumpadDot::send . ; prints '.' 

;Special characters
<^>!-::‒	; en - long hyphen / minus
<^>!+-::—	; em - dash
::#en::–
::#em::—
::#dia::Ø
; ::#euro::€
; <^>!+e::€

; Greek characters 'Key-combinations'
<^>!a::α
<^>!b::β
<^>!g::γ
<^>!d::δ
; <^>!e::ε
<^>!n::η
<^>!t::ϑ
<^>!l::λ
<^>!m::μ
<^>!p::π
<^>!r::ρ
<^>!s::σ
<^>!f::φ
<^>!w::ω

<^>!+d::Δ
<^>!+p::Π
<^>!+S::Σ
<^>!+w::Ω

; Greek characters 'Hotstrings'
::#alpha::α
::#beta::β
::#gamma::γ
::#delta::δ
::#deltavar::∂
::#epsilon::ε
::#zeta::ζ
::#eta::η
::#theta::θ
::#thetavar::ϑ
::#iota::ι
::#kappa::κ
::#lambda::λ
::#my::μ
::#ny::ν
::#xi::ξ
::#omikron::ο
::#pi::π
::#rho::ρ
::#sigma::σ
::#tau::τ
::#ypsilon::υ
::#phi::ϕ
::#phivar:: φ
::#chi::χ
::#psi::ψ
::#omega::ω

::#Alpha::Α
::#Beta::Β
::#Gamma::Γ
::#Delta::Δ
::#Epsilon::Ε
::#Zeta::Ζ
::#Eta::Η
::#Theta::Θ
::#Iota::Ι
::#Kappa::Κ
::#Lambda::Λ
::#My::Μ
::#Ny::Ν
::#Xi::Ξ
::#Omikron::Ο
::#Pi::Π
::#Rho::Ρ
::#Sigma::Σ
::#Tau::Τ
::#Ypsilon::Υ
::#Phi::Φ
::#Chi::Χ
::#Psi::Ψ
::#Omega::Ω
::#Ohm::Ω


; Mathematic Symbols
::#Prod::∏
::#Sum::∑

::#>=::≥
::#<=::≤
::#==::≡
::#uneq::≠
::#approx::≈
::#cdot::∙
::#not::⌐
::#avrg::Ø
::#pm::±
::#hdots::…
::#vdots::⁞
::#pmille::‰
::#inf::∞

::#->::→
::#<-::←
::#-^::↑
::#-v::↓
::#<->::↔

^+c:: ; copys floating number to clipboard and replaces dot by comma or vice versa
  clipboard = 	; emptys clipboard
  send ^c		; copy
  Sleep 50
  clipText := Clipboard	
  Sleep 50
  if ( RegExMatch(clipText, "\d+\.\d+") > 0) ; In case of dot separated value
  { ; Replace dot with comma
    clipText := RegExReplace(clipText,"\.",",")		
	Clipboard := clipText
	Sleep 50
  }
  else if ( RegExMatch(clipText, "\d+,\d+") > 0) ; In case of comma separated value
  { ; Replace comma with dot
    clipText := RegExReplace(clipText,",",".")		
	Clipboard := clipText
	Sleep 50
  }
return
