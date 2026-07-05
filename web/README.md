简单的前端示例：用于输入表达式，调用后端并渲染 LaTeX 结果。

说明：此页面通过 KaTeX CDN 渲染数学公式，使用浏览器 fetch 调用本地后端 API (http://localhost:5000/api/solve)。

使用方法：在后端启动 Flask（参见 backend/run.ps1），然后用浏览器打开本文件（直接双击打开或通过本地静态服务器）。
