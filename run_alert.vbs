' Executa o script Python em segundo plano, sem abrir janela de terminal.
' Coloque um atalho deste arquivo em:
'   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

Dim scriptDir
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

Dim cmd
cmd = "pythonw """ & scriptDir & "\login_alert.py"""

CreateObject("WScript.Shell").Run cmd, 0, False
