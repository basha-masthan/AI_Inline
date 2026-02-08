$desktop = [System.Environment]::GetFolderPath('Desktop')
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$desktop\GitHub AI Assistant.lnk")

# Target python.exe directly to avoid Smart App Control blocking the .bat file
$Shortcut.TargetPath = "python.exe"
$Shortcut.Arguments = "d:\CodeX\FRD\AI_Inline\ai_assistant.py"
$Shortcut.WorkingDirectory = "d:\CodeX\FRD\AI_Inline"
$Shortcut.WindowStyle = 1
$Shortcut.IconLocation = "python.exe,0" # Uses Python icon
$Shortcut.Description = "Launch GitHub AI Assistant"
$Shortcut.Save()

Write-Host "Shortcut created on Desktop successfully!"
