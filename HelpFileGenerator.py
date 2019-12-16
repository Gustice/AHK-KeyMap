################################################################################
# Help-File generator for Autohotkey files 
# Collects Hotkey and Hotstring definitions ands prints them as helpfile table
# Usage: $py AHK-HelpFileGenerator.py <filename> [encoding]
# If encoding is not given the system default encoding will be used.
################################################################################

import sys
import os
import re # Regular expressions

# Decodes cryptic AHK hotkey definitions to string
HkCodes = []
HkNames = []

hkIngores = ['*', '~', '$']
hkCodeCommon = ['<#',       '>#',        '#',   '<^>!',  '<^',        '>^',         '^',    '<!',       '>!',        '!',   '<+',         '>+',          '+'    ]
hkNameCommon = ['Left-Win', 'Right-Win', 'Win', 'AltGr', 'Left-Ctrl', 'Right-Ctrl', 'Ctrl', 'Left-Alt', 'Right-Alt', 'Alt', 'Left-Shift', 'Right-Shift', 'Shift']
hkCodeModifier = ['LWin'    , 'RWin'     , 'Control', 'Ctrl', 'Alt' , 'Shift' , 'LControl',  'LCtrl',     'RControl',   'RCtrl',      'LShift'  ,    'RShift'  ,    'LAlt'    , 'RAlt' ]
hkNameModifier = ['Left-Win', 'Right-Win', 'Ctrl' ,   'Ctrl', 'Alt' , 'Shift' , 'Left-Ctrl', 'Left-Ctrl', 'Right-Ctrl', 'Right-Ctrl', 'Left-Shift' , 'Right-Shift', 'Left-Alt', 'Right-Alt' ]
hKCodeGeneral = ['CapsLock' , 'Space' , 'Tab' , 'Enter', 'Return', 'Escape', 'Esc',    'Backspace' 'BS'       ]
hKNameGeneral = ['CapsLock' , 'Space' , 'Tab' , 'Enter', 'Enter',  'Escape', 'Escape', 'Backspace' 'Backspace']
hKCodeCursor = ['ScrollLock', 'Delete', 'Del',    'Insert', 'Ins',    'Home', 'End', 'PgUp',   'PgDn',     'Up', 'Down', 'Left', 'Right']
hKNameCursor = ['ScrollLock', 'Delete', 'Delete', 'Insert', 'Insert', 'Home', 'End', 'PageUp', 'PageDown', '↑',  '↓',    '←',    '→',    ]
hKCodeNPNumMode = ['Numpad0'  , 'Numpad1'  , 'Numpad2'  , 'Numpad3'  , 'Numpad4'  , 'Numpad5'  , 'Numpad6'  , 'Numpad7'  , 'Numpad8'  , 'Numpad9'  , 'NumpadDot']
hKNameNPNumMode = ['NumPad-0' , 'NumPad-1' , 'NumPad-2' , 'NumPad-3' , 'NumPad-4' , 'NumPad-5' , 'NumPad-6' , 'NumPad-7' , 'NumPad-8' , 'NumPad-9' , 'NumPad-.' ]
hKCodeNPCursorMode = ['NumpadIns'  ,   'NumpadEnd'  , 'NumpadDown', 'NumpadPgDn' ,     'NumpadLeft', 'NumpadClear', 'NumpadRight', 'NumpadHome' , 'NumpadUp', 'NumpadPgUp' ,   'NumpadDel'    ]
hKNameNPCursorMode = ["NumPad-Insert", "NumPad-End",  "NumPad-↓",   "NumPad-PageDown", "NumPad-←",   "",            "NumPad-→",    "NumPad-Home", "NumPad-↑", "NumPad-PageUp", "NumPad-Delete"]
hKCodeNPGeneral = ['NumLock', 'NumpadDiv', 'NumpadMult', 'NumpadAdd', 'NumpadSub', 'NumpadEnter' ]
hKNameNPGeneral = ['NumLock', 'NumPad-/',  'NumPad-*',   'NumPad-+',  'NumPad--',  'NumPad-Enter']
hkCodeFKeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24']
hkNameFKeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24']

HkCodes = HkCodes + hkCodeCommon + hkCodeModifier + hKCodeGeneral + hKCodeCursor + hKCodeNPNumMode + hKCodeNPCursorMode + hKCodeNPGeneral + hkCodeFKeys
HkNames = HkNames + hkNameCommon + hkNameModifier + hKNameGeneral + hKNameCursor + hKNameNPNumMode + hKNameNPCursorMode + hKNameNPGeneral + hkNameFKeys

# Hotkey-Decoder for AutoHotkey Keys
# Interprets an AHK Hotkey like '#!W' as 'Win+Alt+W'
def HotkeyDecoder(keys):
    hotKeyCode = ""
    keys = str.lower(keys)
    
    # Delete all internal modifier
    for i in range(len(hkIngores)):
        keys = keys.replace(hkIngores[i],'')
    
    # Decode all Special functions like Control, Alt, ...
    for i in range(len(HkCodes)):
        key = str.lower(HkCodes[i])
        if ( keys.find(key) >= 0):
            hotKeyCode = hotKeyCode + HkNames[i] + '+'
            keys = keys.replace(key,'')
    
    # Append all ordinary characters like abc 123
    keys = str.upper(keys)
    for i in range(len(keys)):
        hotKeyCode = hotKeyCode + keys[i] + '+'
    
    return hotKeyCode.rstrip('+')


# Hotkey-Definition
# Syntax: "<EncodedHotkeyString>::[Command][;Comment]"
# Note: Hotkey-Definition isn't necessarily a single line command, however, 
#   only first line is parsed for documentation purpose.
# Note: If command is not shown in same line the comment is mandatory
# Note: Comment is optional if command is defined in same line as Hotkey
#   @todo implement sophisticated checks
class HotKey:
    maxHK = 0
    maxSend = 0

    def __init__(self, defString, command, description):
        if(not defString):
            return 

        self.defString = defString.strip()
        self.KeyDef = HotkeyDecoder(defString)
        HotKey.maxHK = max(len(self.KeyDef), HotKey.maxHK)
        
        self.command = ""
        if command:
            self.command = command.strip()
            HotKey.maxSend = max(len(self.command), HotKey.maxSend)
        self.description = ""
        if description:
            self.description = description.strip()
        return

    def PrintDefine(self):
        keyForm = '{' + ":{:d}s".format(HotKey.maxHK) + '}'
        cmdForm = '{' + ":{:d}s".format(HotKey.maxSend) + '}'
        formStr1 = "{} => {} | {}".format(keyForm,cmdForm,"{}")
        formStr2 = "{}    {} | {}".format(keyForm,cmdForm,"{}")

        output = ""
        if (self.command and self.description):
            output = formStr1.format(self.KeyDef, self.command, self.description)
        elif (self.command):
            output = formStr1.format(self.KeyDef, self.command, "")
        elif (self.description):
            output = formStr2.format(self.KeyDef, "", self.description)

        return output

# Hotstring-Definition
# Syntax: ""::<SensitiveString>::[Command][;Comment]"
# Note: Hotstring-Definition isn't necessarily a single line command, however, 
#   only first line is parsed for documentation purpose.
# Note: If command is not shown in same line the comment is mandatory
# Note: Comment is optional if command is defined in same line as Hotkey
#   @todo implement sophisticated checks
class HotString:

    maxHS = 0
    maxSend = 0

    def __init__(self, defString, command, description):
        if(not defString):
            return 

        self.defString = defString.strip()
        HotString.maxHS = max(len(self.defString), HotString.maxHS)
        
        self.command = ""
        if command:
            self.command = command.strip()
            HotString.maxSend = max(len(self.command), HotString.maxSend)
        
        self.description = ""
        if description:
            self.description = description.strip()
        return

    def PrintDefine(self):
        keyForm = '{' + ":{:d}s".format(HotString.maxHS) + '}'
        cmdForm = '{' + ":{:d}s".format(HotString.maxSend) + '}'
        formStr1 = "{} => {} | {}".format(keyForm,cmdForm,"{}")
        formStr2 = "{}    {} | {}".format(keyForm,cmdForm,"{}")

        output = ""
        if (self.command and self.description):
            output = formStr1.format(self.defString, self.command, self.description)
        elif (self.command):
            output = formStr1.format(self.defString, self.command, "")
        elif (self.description):
            output = formStr2.format(self.defString, "", self.description)

        return output


################################################################################
# Collects Hotkey and Hotstring definitions ands prints them as helpfile table
# 
# 
################################################################################
if (len(HkCodes) != len(HkNames)):
    print("Defined Hotkey-Description-Combination doesn't match")
    exit()

# Filename argument is mandatory
if (len(sys.argv) < 2):
    print("File argument is missing")
    exit()

file = sys.argv[1]
enc = sys.getdefaultencoding()

# Encoding argument is mandatory
if (len(sys.argv) == 3):
    enc = sys.argv[2]
print("Applied configuration: '{}'".format(enc))

name, extension = os.path.splitext(file)
if(extension != ".ahk"):
    print("Given argument is no Autohotkey file. Program exit")
    exit()

hotStringDefines = []
hotKeyDefines = []

print("Parsing given file: {}".format(file))
# Read given file and scan for Hotkey and Hotstring definitions
with open(file, 'r', encoding=enc) as fStream:
    
    line = fStream.readline()
    while line:
        line = fStream.readline()
        
        # Ignore Comment lines
        cStr = re.match("^\s*;", line)
        if (cStr):
            continue

        # Match Hotstrings like ::String::Action
        mHStr = re.match("^:\\*?:(?P<String>[^:]+)::(?P<Command>\\s*[^;]*\\s*)(?:;(?P<Comment>.*))?", line)
        if(mHStr):
            #print("matched line as hotstring: \n    {}".format(line))
            hS = HotString(mHStr.group('String'), mHStr.group('Command'), mHStr.group('Comment'))
            hotStringDefines.append(hS)

        # Match Hotkeys like Key::Action
        mHKey = re.match("^(?P<String>[^:]+)::(?P<Command>\\s*[^;]*\\s*)(?:;(?P<Comment>.*))?", line)
        if(mHKey):
            #print("matched line as hotkey: \n    {}".format(line))
            hS = HotKey(mHKey.group('String'), mHKey.group('Command'), mHKey.group('Comment'))
            hotKeyDefines.append(hS)

# Write found Objects to helpfile
print("Writing help output to file:")
nFile = name + ".help"
with open(nFile, 'w', encoding=enc) as oStream:
    oStream.write("Helpfile for {}\n".format(file))
    oStream.write("  Note: FileEncoding {}\n".format(enc))
    oStream.write("\n\n")

    oStream.write("Defined HotKeys:\n")
    for i in range(len(hotKeyDefines)):
        oStream.write(hotKeyDefines[i].PrintDefine() + '\n')
    
    oStream.write("\n\n")
    
    oStream.write("Defined HotStrings:\n")
    for i in range(len(hotStringDefines)):
        oStream.write(hotStringDefines[i].PrintDefine() + '\n')
