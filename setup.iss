[Setup]
AppName=PNG Tuber
AppVersion=1.0
DefaultDirName={pf}\PNG Tuber
DefaultGroupName=PNG Tuber
OutputBaseFilename=PNGTuber_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico

[Files]
Source: "dist\PNGTuber.exe"; DestDir: "{app}"
Source: "my_photos\*"; DestDir: "{app}\my_photos"; Flags: recursesubdirs

[Icons]
Name: "{group}\PNG Tuber"; Filename: "{app}\PNGTuber.exe"
Name: "{group}\Uninstall PNG Tuber"; Filename: "{uninstallexe}"
Name: "{commondesktop}\PNG Tuber"; Filename: "{app}\PNGTuber.exe"

[Run]
Filename: "{app}\PNGTuber.exe"; Description: "Запустить PNG Tuber"; Flags: postinstall nowait skipifsilent
