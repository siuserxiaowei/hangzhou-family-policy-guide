# 杭州家庭迁居与出海创业政策手册

在线阅读：[打开 GitHub Pages](https://siuserxiaowei.github.io/hangzhou-family-policy-guide/)
资料包：[下载 HTML、政策批注和来源清单](https://siuserxiaowei.github.io/hangzhou-family-policy-guide/downloads/hangzhou-family-policy-pack.zip)

为西安家庭迁居杭州整理的静态阅读手册：教育与转学、居住区域、落户、出海创业支持、签约清单、咨询话术和零补贴成本试算。含 14 张政策解读卡、24 条来源及办事入口。

## 来源与恢复方式

内容来自用户提供的 [ChatGPT 分享对话](https://chatgpt.com/share/6ab9d326-54ec-83e8-9914-4e1cbd555cf0)。分享里的临时附件无法直接取得，因此从该分享页保留的生成代码与后续修订记录恢复手册，按记录应用五条内容修订。本次发布增加资料包下载入口和内嵌图标，未重新编写政策正文。未取得原 ZIP 二进制文件，不能声称恢复文件与原附件逐字节一致。

政策资料沿用原手册标注的 **2026-09-28** 核验口径。本次完成文件恢复与网页部署验证，没有重新审核所有政策或家庭个人资格。原手册明确列出的余杭转学与高中招生、当期落户、企业入库等待核项目仍然保留。资料包包含阅读批注和原文链接，不是政府原始附件的完整离线副本。

## 文件

- `index.html`：GitHub Pages 入口，无需构建。
- `build_report.py`：恢复后的标准库生成器，重建网页与文档。
- `docs/`：离线 HTML、政策批注、结构化来源和解读卡。
- `docs/publication-verification.json`：本次网页功能、排版和发布验证记录。
- `downloads/hangzhou-family-policy-pack.zip`：离线资料包。
- `.nojekyll`：GitHub Pages 按普通静态文件发布。

## 本地预览与重建

```bash
python3 build_report.py
python3 -m http.server 8766 --bind 127.0.0.1
```

浏览器打开 `http://127.0.0.1:8766`。生成器不联网，不需要第三方依赖。资料 ZIP 是发布快照；更新政策后需一并重新打包。

## 发布

GitHub Pages 使用 `main` 分支根目录，后续推送自动发布。页面的勾选和备注保存在当前浏览器，导出记录用于本地备份。
