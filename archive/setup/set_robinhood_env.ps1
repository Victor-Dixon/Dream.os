# PowerShell script to set Robinhood environment variables
$env:ROBINHOOD_USERNAME = "DaDudeKC@gmail.com"
$env:ROBINHOOD_TOTP_SECRET = ""
Write-Host "Enter your Robinhood password:"
$password = Read-Host -AsSecureString
$env:ROBINHOOD_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
Write-Host "Environment variables set. Now run: python tools/robinhood_auth_test.py"