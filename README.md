# Knight Image To PPT · 增强版

将已有幻灯片图片、截图、图片型 PPT 或 PDF 页面转换为分层可编辑 PPTX。基于 [knight6669/knight-imagetopptx-skill](https://github.com/knight6669/knight-imagetopptx-skill)（MIT），加入连续页实践形成的增强流程。

## 增强能力

- 复用已授权的项目素材，建立稳定 ID 与来源清单。
- 现代场景优先核实并使用真实照片；地图采用真实地理底图。
- 图标紧边裁剪、透明边保护和独立图片对象，方便选中与移动。
- 相邻同一行文字使用一个文本框，支持混色 runs；连续说明合并。
- 默认宋体、整数磅；记录预览环境实际替代字体。
- 原生渐变、alpha 淡出、斜切图片及简单可编辑符号。
- 文字适配、整页/局部渲染及针对性 OOXML 检查。

## 安装与调用

本仓库根目录就是技能目录。下载或克隆仓库，将整个目录安装到支持 `SKILL.md` 的技能宿主中；不要只复制单个文件。

Codex CLI 示例：

```bash
git clone https://github.com/petterxch/knight-imagetoppt-enhanced.git ~/.codex/skills/knight-imagetoppt-enhanced
```

在支持个人技能的 ChatGPT/Codex 环境中，可通过技能安装机制添加；已安装后显式调用：

> 使用 @knight-imagetoppt-enhanced 转换本页，复用已有素材，真实照片优先，保留渐变。

也可使用宿主支持的 `$knight-imagetoppt-enhanced` 调用语法。技能不是一键 OCR 转换器；由代理读取页面、规划对象并执行附带工具。跨页素材仅来自当前获准文件，不自动读取其他对话。

## 依赖与脚本

Python 3.10+；Python 依赖安装：

```bash
python -m pip install -r scripts/requirements.txt
python scripts/asset_registry.py --root /path/to/approved/assets --output asset_registry.json
python scripts/crop_asset.py source.png icon.png --padding 12
python scripts/ppt_text_fit.py --help
python scripts/validate_pptx.py rebuilt.pptx --font 宋体 --json qa/xml_check.json
```

另外需要 LibreOffice/PowerPoint 渲染器与有授权的中文字体。宋体不可用时可提供 Noto Serif CJK SC 作为预览替代，并记录替代结果。图像生成和网页检索能力由宿主提供。

## 校验范围

已完成技能格式检查、脚本执行及独立单页试用，包括同框混色标题、宋体整数磅、原生渐变和整数多边形坐标。渲染使用 LibreOffice 与 Noto Serif CJK SC 替代字体。

结构检查是针对性的 DrawingML/包关系检查，不是完整 OpenXML SDK 验证。实际 Microsoft PowerPoint 打开未测试；不得据此承诺任何复杂页面都无需修复。

## 来源与许可

上游固定版本：`9265818222fdbdd326410793956ad23a950d72a7`。原版全文见 `references/knight-upstream.md`，扩展说明见 `references/provenance.md`。保留原作者 Knight | 贺的 MIT 许可；不附带用户课件、私人照片、会话记录或专用素材。
