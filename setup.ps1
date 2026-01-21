# SWE7301-API Setup Script for New Systems
# Run this script in PowerShell as Administrator

Write-Host "=== SWE7301-API: GeoScope Analytics Platform Setup ===" -ForegroundColor Green
Write-Host "Setting up complete development environment..." -ForegroundColor Yellow

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Set execution policy if needed
Write-Host "🔧 Setting PowerShell execution policy..." -ForegroundColor Blue
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✅ Execution policy updated" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not set execution policy. You may need to run as Administrator." -ForegroundColor Yellow
}

# Create virtual environment
Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Blue
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "⚡ Activating virtual environment..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

if ($?) {
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip

# Install backend dependencies
Write-Host "🔧 Installing Flask backend dependencies..." -ForegroundColor Blue
Set-Location "backend"
pip install flask flask-cors flask-jwt-extended flask-sqlalchemy sqlalchemy gunicorn flasgger
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
}
Set-Location ".."

# Install frontend dependencies  
Write-Host "🌐 Installing Django frontend dependencies..." -ForegroundColor Blue
Set-Location "frontend"
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
}

# Run Django migrations
Write-Host "🗄️  Running Django database migrations..." -ForegroundColor Blue
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database migrations completed" -ForegroundColor Green
} else {
    Write-Host "❌ Database migrations failed" -ForegroundColor Red
}
Set-Location ".."

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Start Backend Server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python run.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Frontend Server (in new terminal):" -ForegroundColor White  
Write-Host "   venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   python manage.py runserver 8001" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open browser to: http://127.0.0.1:8001" -ForegroundColor White
Write-Host "4. Login with: admin / password" -ForegroundColor White
Write-Host ""
Write-Host "=== Servers ===" -ForegroundColor Cyan
Write-Host "Backend (Flask + JWT): http://127.0.0.1:5000" -ForegroundColor White
Write-Host "Frontend (Django): http://127.0.0.1:8001" -ForegroundColor White
