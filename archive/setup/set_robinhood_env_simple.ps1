# Simple PowerShell script to set Robinhood environment variables
# Run this first, then enter your password when prompted

$env:ROBINHOOD_USERNAME = "DaDudeKC@gmail.com"
$env:ROBINHOOD_TOTP_SECRET = ""

# Get password securely
$password = Read-Host "Enter your Robinhood password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$env:ROBINHOOD_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host "Environment variables set successfully!"
Write-Host "Now run: python tools/robinhood_auth_test.py"
Write-Host ""
Write-Host "When the script prompts for manual 2FA approval:"
Write-Host "1. Open your Robinhood app on your phone"
Write-Host "2. Look for 'Device Approval' or 'Login Request' notification"
Write-Host "3. Approve the request quickly (within 30 seconds)"