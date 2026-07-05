# PowerShell 脚本：在 Windows 上创建 venv，安装依赖并运行 Flask

# 运行此脚本前，请在 PowerShell 中允许脚本执行：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 运行 Flask
$env:FLASK_APP = "app.py"
# 允许外部访问，如果需要仅本机访问可删去 --host
flask run --host=0.0.0.0 --port=5000
