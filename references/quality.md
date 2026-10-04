# 检查证据

每页保存：

- `reference.png`：规范化原页。
- `asset_registry.json`：项目素材稳定 ID、路径、大小、来源、分类、适用主题。
- `asset_manifest.json`：本页最终图片、复用来源、裁剪/alpha 边界、放置区域；真实照片附 URL 和出处核实状态。
- `text_fit_report.json`：对象 ID、完整文字、预期字体、预览实际字体、整数字号、槽位、行数、测量宽高、是否适配。
- `preview.png` 与必要 `*_render.png` / `*_reference.png` 局部对比。
- `asset_contact_sheet.png`：最终图标及线稿，不要把未使用的源素材页混入最终素材。
- `xml_check.json`：目标 OOXML 与字体检查输出，写明不是完整 SDK 验证。
- `rebuild_execution_report.json`：最终一次性总结。

执行报告键包括 `input_prepared`、`visual_inventory_done`、`asset_classification_done`、`assets_done`、`text_fit_done`、`pptx_built`、`render_qa_done`、`local_crop_qa_done`、`validation_done`、`limitations`。仅记录实际做过的步骤；缺失步骤应标为 blocked 或 draft。

发现问题后的优先级：

1. 文字内容错误、主体/活动错误、地图错误、文件无法打开。
2. 文字溢出/遮挡、照片主体截断、原图残影、字号/字体不符。
3. 渐变丢失、箭头方向错误、边框缺失、重复阴影与层级错误。
4. 图标碎片、透明边过大、选择框接近整页、过多文本框。
5. 与参考图的色彩、间距和装饰差异。

对于真实照片替换，评估语义与构图，不要求逐像素相同；文本及组件仍应对照原页。备注说明替换，不把画面当事实论据。
