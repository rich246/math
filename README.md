# rich246/math - 本地 AI 数学 起步实现

此分支添加了一个最小可运行的本地 AI 数学示例：后端使用 SymPy 提供符号计算 API，前端是一个简单的 HTML 页面，使用 KaTeX 渲染 LaTeX 结果。

主要内容：
- backend/app.py：Flask 后端，提供 /api/solve 接口（支持 simplify/solve/diff/integrate）。
- backend/requirements.txt：所需 Python 包列表（flask, sympy, flask-cors）。
- backend/run.ps1：Windows PowerShell 一键创建虚拟环境并运行服务器的脚本。
- web/index.html：简单前端示例，调用后端并用 KaTeX 渲染结果（使用 CDN）。
- web/README.md：前端使用说明。

注意：此实现离线（不使用付费云 API），但前端 KaTeX 通过 CDN 加载（免费）。如果需要完全脱网运行，我可以把 KaTeX 静态文件也加入仓库并更新前端来本地加载。

如何运行（Windows 快速开始）：
1. 克隆仓库并切到分支 feature/local-ai-math：
   git fetch origin
   git checkout -b feature/local-ai-math origin/feature/local-ai-math || git checkout -b feature/local-ai-math

2. 进入 backend 目录并运行 PowerShell 脚本（需要启用脚本执行或以管理员运行）：
   cd backend
   .\run.ps1

3. 打开 web/index.html（直接用浏览器打开文件），在页面中输入表达式并调用本地后端（确保后端在 http://localhost:5000 运行）。

如果你允许，我可以：
- 把 KaTeX 静态文件加入仓库以支持完全脱网运行；
- 增加 OCR、步骤更详细的推理或者把前端做成 React/Vite 项目；
- 将这个实现合并到主分支或发起 PR（需要你确认目标分支）。
