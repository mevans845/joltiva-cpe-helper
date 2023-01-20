# Very Basic and Untested PowerShell Script to compress and backup archive

$Limit = (Get-Date).AddMonths('-12')  # This example will compress anything that is older than 12 Months
# $Limit = (Get-Date).AddDays(-30)  # Use this to compress things older than 30 days
$Path = "D:\InsertPAth"
$zipDir = "D:\InsertDest"
$ItemsToZip = (Get-ChildItem -Path $Path -Directory -Force).where{$_.LastWriteTime -le $Limit}.FullName

New-Item -Type Directory -Path $Path -Name 'zipDir' -Force

$ItemsToZip | ForEach-Object {

    $FullPath=$_

    Move-Item $FullPath -Destination $zipDir -Force
    Compress-Archive -Path $zipDir
}