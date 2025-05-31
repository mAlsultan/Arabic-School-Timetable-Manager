[Setup]
AppName=School Timetable Generator
AppVersion=1.0
AppPublisher=Your Name/Organization
DefaultDirName={autopf}\TimetableGenerator
DefaultGroupName=TimetableGenerator
OutputDir=output
OutputBaseFilename=TimetableGenerator_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\mushroom.ico
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Files]
; Main executable
Source: "dist\TimetableGenerator.exe"; DestDir: "{app}"; Flags: ignoreversion

; Data folder (for JSON files)
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

; Include Python DLLs and dependencies (if needed)
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Timetable Generator"; Filename: "{app}\TimetableGenerator.exe"
Name: "{commondesktop}\Timetable Generator"; Filename: "{app}\TimetableGenerator.exe"
Name: "{group}\Uninstall Timetable Generator"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\TimetableGenerator.exe"; Description: "Launch Application"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\data"