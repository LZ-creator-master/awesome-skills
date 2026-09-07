# GitHub发布指南

[返回首页](../README.md)

此目录可以作为仓库根目录。中文首页为 `README.md`，安装入口为 `scripts/install.py`。

## 首次发布

1. 确定GitHub账号、仓库名称及可见性；如果推送到已有仓库，先读取远程内容。
2. 查看 `.gitignore`，确保本机维护记录、备份与凭据不进入提交。
3. 运行校验和测试，检查 `git diff --cached` 后创建提交。
4. 添加经确认的远程地址并正常推送，不使用强制推送覆盖已有历史。
5. 在仓库页面确认README、17个技能与自动校验结果。

在线导航使用 GitHub Pages。在仓库 Settings → Pages 中选择 GitHub Actions，运行 Publish skill navigation 工作流。`python scripts/build_pages.py` 只把导航页写入 `dist/pages/index.html`，文档链接转向 GitHub，不发布工作目录中的其他文件。根目录HTML仍可离线使用。

## 内容状态

发布版本包含技能使用方法、来源和适配说明，不表示所有第三方工具可用，也不声明已经获得统一开源许可。参阅[来源与授权状态](来源与授权状态.md)。
