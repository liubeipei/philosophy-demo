思有引力 · 可运行 HTML 产品原型
=================================

包含：人格测试（6/12/20轮）、人格匹配与报告、PNG卡片保存、12位哲学家对话、每日哲学困境、积分、人物图鉴、我的页面、响应式布局。

一、无需 API，直接体验
双击 index.html 在浏览器中打开；自动进入本地演示模式。测试和对话都可体验，但非真正 AI 动态推理。

二、连接 DeepSeek（推荐）
电脑已安装 Python 3 的情况下，在本目录运行：

macOS / Linux:
  export DEEPSEEK_API_KEY='你自己在控制台生成的新Key'
  python3 server.py

Windows PowerShell:
  $env:DEEPSEEK_API_KEY='你自己在控制台生成的新Key'
  python server.py

在浏览器访问 http://localhost:8765

【安全】Key 仅保存在本机进程环境变量中；不会出现在 HTML、JS 或交付文件中。你之前发到聊天中的 Key 建议立即在 DeepSeek 控制台撤销，并重新生成。
本地服务仅监听 127.0.0.1，不面向公网。不需要额外安装 Python 第三方库。

三、演示注意
- 连网模式使用 DeepSeek 官方 chat/completions 接口，按 API 供应商实际调用产生费用。
- 人格得分是交互产品原型，未经过心理测量学验证。
- 浏览器 localStorage 会保存对话历史及测试结果；可在「我的」页面删除。
- DeepSeek 连网时，输入内容会发送至 DeepSeek API。
- 如 API 不可用，测试可退回到预置问题与本地演示匹配。
