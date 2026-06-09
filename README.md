简易 Illustrator 应用入口 (Python 3.10+) — DeepSeek AI 驱动版

基于 PyQt5 实现的矢量图形编辑器，集成 DeepSeek 大模型交互式对话。
支持：选择、矩形、椭圆、钢笔路径、文字工具
AI功能：自然语言对话生成矢量文本海报（6种模板，9种配色方案）
功能：图层管理、属性编辑、颜色填充/描边、编组、导出PNG/SVG

启动方式：
    python main.py                                    # 默认启动
    python main.py --api-key sk-xxx                   # 指定 API Key
    python main.py --model deepseek-reasoner          # 指定模型
    set DEEPSEEK_API_KEY=sk-xxx && python main.py     # 环境变量方式
