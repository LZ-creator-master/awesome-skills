# LightGCN：论文到组会提纲

[在线案例](https://lz-creator-master.github.io/awesome-skills/examples/lightgcn/) · [组会提纲](../examples/lightgcn/outline.md) · [返回首页](../README.md)

日期：2026-09-07。环境：Windows上的Codex对话，当前任务模型配置；精确模型快照未记录。实际读取本库 `paper-analyzer` 入口，按学术型流程完成来源阅读、中文解读、教学图和10分钟组会提纲。

实际阅读：[LightGCN arXiv v4](https://arxiv.org/html/2002.02126v4) 正文§1–6、表1–6和图注；没有逐张测量原图。案例选择表3三层数据，不把表4最佳配置混入同条件对照。相对百分比按展示的小数重算，Yelp的10.36%与原文显示的10.38%差异已注明。

源码：论文指向的[PyTorch实现](https://github.com/gusye1234/LightGCN-PyTorch)，固定提交 `947ca2b3b1d2d3545b114145710cb06c4e57b3d2`，核对 `code/model.py` 的传播、均值组合和BPR项。未安装训练环境、未下载数据集、未训练模型。

产物：HTML解读、小图传播交互、基础/进阶切换、三道有解析的自测题、Markdown组会提纲。提纲为文本产物，没有把它记成 `paper-deck` 的PPTX或图像流程验证。

本次是多步骤制作，非单条提示词的未经修订输出。教学图的向量由本案例构造，不是训练出来的嵌入。下载整个仓库后，页面使用仓库内 `assets/learning.css` 和 `assets/learning.js`；无外部CDN依赖。
