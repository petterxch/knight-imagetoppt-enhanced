# 实现注意事项

## 坐标与文字

采用源图像素坐标，使用 `px / source_width * slide_width` 转换至 EMU。保持源图比例或明确记录页面比例调整。字体磅与行距分别设置；字号要求整数，不意味着行距必须整数。

`pptx_helpers.add_text_runs(slide, name, runs, box, source_size, slide_size)` 接收 `[(text, int_pt, hex_color), ...]`。包含换行的 run 建新段；同一行继续用 runs。该函数不做自动适配，先执行文字测量并保存证据。

在常见 Linux 字体环境中 SimSun 可能缺失。`fc-match SimSun` 返回替代字体不等于 SimSun 已安装；检查实际文件和字体家族。可用 Noto Serif CJK SC 作预览替代，记录这一限制。禁止加入无分发许可的字体文件。

## 渐变与斜切

`set_gradient(shape, stops, angle)` 的 stops 是 `(0..100000, RRGGBB, 0..100000)`，最后一个值为 alpha（100000 不透明）。角度使用 OOXML 单位，60000 表示 1°。渐变必须至少两个停靠点，按位置升序。

`set_polygon(shape, points, width, height)` 修改形状或图片几何，点与 width/height 使用整数的同一坐标系；保留图像的 crop 以维持纵横比。不要把浮点坐标写进 `a:pt`，避免 PowerPoint 提示修复。对于图像蒙版边界，先试渲染，再决定裁剪主体；左边斜切会遮掉照片左侧内容。

对于多个填充类型、多个几何节点，先移除旧值再设置新值。OOXML 的 `spPr` 子节点顺序必须为变换、几何、填充、线条、效果等。不要直接在末尾重复追加 `solidFill` 和 `gradFill`。`normalize` 只负责目标节点的次序，不是 XML 任意修复工具。

## 独立素材

背景、真实照片和独立透明图标分别存放。使用紧边裁剪脚本处理 PNG alpha；对去背景、移除文字、清理图像等真正图片编辑任务，遵循所在环境图像编辑工具规则。图像生成工具存在时优先按其规则执行，不能把切边脚本用于伪造实拍。

保留原图、衍生图、网页出处、下载时间、裁剪参数和授权备注。RGBA 透明边不应进入最终屏幕可见区域，但为防抗锯齿截断保留至少 10px 的透明安全边。

## 渲染

```bash
libreoffice -env:UserInstallation=file:///absolute/project/lo-profile \
  --headless --convert-to pdf --outdir qa output.pptx
```

给并行或相邻任务独立 profile 路径。命令名可能是 `soffice` 而不是 `libreoffice`。中文字体替代未实际生效时，创建项目本地 Fontconfig 配置，将 SimSun/宋体映射到已安装的 CJK 字体，使用 `FONTCONFIG_FILE` 调用渲染器，并记录替代；不要修改系统配置。

用 PyMuPDF 将 PDF 以源图大小渲染成 PNG。查看全页及局部，确认动态裁剪和渐变在渲染器中有效。结构检查通过仍可能存在文字遮挡、主题阴影或字体替代，需要视觉检查。
