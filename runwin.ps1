# Перевірка наявності Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "I not see Python in system, please install Python for work with me :)" -ForegroundColor Red
    exit
}

# Перевірка наявності віртуального середовища
if (-not (Test-Path "./venv")) {
    Write-Host "Create virtual framework..." -ForegroundColor Green
    python -m venv venv
}

# Активація віртуального середовища
Write-Host "Activization virtual framework..." -ForegroundColor Green
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
./venv/Scripts/Activate.ps1

# Встановлення залежностей
Write-Host "Installing modules..." -ForegroundColor Green
python -m pip install --upgrade pip
pip install --upgrade pip
pip install -r requirements.txt

# Запуск Python-скрипта
Write-Host "Run script..." -ForegroundColor Green
python main.py
