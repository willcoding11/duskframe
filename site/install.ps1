<#
 Installer for Windows (no admin needed).
   irm <site>/install.ps1 | iex          # silent installer
   & ([scriptblock]::Create((irm <site>/install.ps1))) -Portable   # unzip only (also -Uninstall, -DryRun)
 Parameters: -Portable -Uninstall -DryRun -BaseUrl <url> -InstallDir <dir>
#>
param(
  [switch]$Portable, [switch]$Uninstall, [switch]$DryRun,
  [string]$BaseUrl = $env:BASE_URL,
  [string]$InstallDir = $env:INSTALL_DIR
)
$ErrorActionPreference = 'Stop'

# ---- brand config (single place; site/sync-installers.py rewrites these from branding/brand.env) ----
$BrandName = 'Duskframe'    # @brand
$Slug      = 'duskframe'    # @brand
$GhUser    = 'willcoding11' # @brand
$GhRepo    = 'duskframe'    # @brand
# -----------------------------------------------------------------------------------------------------

if (-not $BaseUrl)    { $BaseUrl = "https://github.com/$GhUser/$GhRepo/releases/latest/download" }
if (-not $InstallDir) { $InstallDir = Join-Path $env:LOCALAPPDATA $BrandName }
$ProgressPreference = 'SilentlyContinue'   # much faster Invoke-WebRequest

function Step($m) { Write-Host "==> $m" }
$lnk = Join-Path ([Environment]::GetFolderPath('Programs')) "$BrandName.lnk"

if ($Uninstall) {
  $unins = Join-Path $InstallDir 'Uninstall.exe'
  if ((Test-Path $unins) -and -not $Portable) {
    Step "Running $unins /S"
    if (-not $DryRun) { Start-Process $unins -ArgumentList '/S' -Wait }
  } else {
    Step "Removing $InstallDir"
    if (-not $DryRun) { Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue }
  }
  if (-not $DryRun) { Remove-Item -Force $lnk -ErrorAction SilentlyContinue }
  return
}

$file = if ($Portable) { "$Slug-windows-x64-portable.zip" } else { "$Slug-windows-x64-setup.exe" }
$tmp  = Join-Path ([IO.Path]::GetTempPath()) "$Slug-install-$([guid]::NewGuid().ToString('N'))"
$dest = Join-Path $tmp $file
Step "Downloading $BaseUrl/$file"
if ($DryRun) {
  if ($Portable) { Write-Host "[dry-run] unpack $file to $InstallDir + Start Menu shortcut" }
  else { Write-Host "[dry-run] run $file /S /D=$InstallDir" }
  return
}
New-Item -ItemType Directory -Force $tmp | Out-Null
try {
  Invoke-WebRequest -UseBasicParsing -Uri "$BaseUrl/$file" -OutFile $dest
  if ($Portable) {
    Step "Unpacking to $InstallDir"
    New-Item -ItemType Directory -Force $InstallDir | Out-Null
    Expand-Archive -Force -Path $dest -DestinationPath $InstallDir
    $exe = Get-ChildItem $InstallDir -Recurse -Filter "$Slug.exe" | Select-Object -First 1
    if ($exe) {
      $sc = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
      $sc.TargetPath = $exe.FullName; $sc.WorkingDirectory = $exe.DirectoryName; $sc.Save()
    }
  } else {
    Step "Running silent installer"
    Start-Process $dest -ArgumentList "/S /D=$InstallDir" -Wait   # NSIS: /D must be last
  }
  Step "Done. Find $BrandName in the Start Menu."
} finally {
  Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
}
