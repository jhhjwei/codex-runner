# 小型代码修复与 Python 自动化服务

本仓库展示可在 24–72 小时内交付的小型技术任务：代码报错定位、CSV/JSON 数据处理、公开网页文本抓取、HTML/CSS 修复和简单落地页。

## 入口

- 服务主页：https://jhhjwei.github.io/codex-runner/
- 提交需求：https://github.com/jhhjwei/codex-runner/issues/new?template=code-fix-request.yml
- 收入冲刺看板：https://github.com/jhhjwei/codex-runner/issues/1

## 公开可运行案例

### 配置驱动 CSV/JSON 解析器

目录：[`demos/config-driven-parser`](demos/config-driven-parser)

通过外部配置完成字段映射、类型转换、默认值、大小写、数值换算和校验，无需修改核心代码。

### 公开网页文本抓取器

目录：[`demos/public-web-text-scraper`](demos/public-web-text-scraper)

面向公开、免登录页面，检查 `robots.txt`、限制同域范围与访问频率，并输出 CSV/JSON。

## 参考价格

- 免费初步判断
- 小型代码修复：¥49–¥99
- Python / CSV 自动化：¥199 起
- 简单落地页：¥399 起

确认输入、输出、验收标准和固定价格后再开始。请勿提交密码、Cookie、Token、私钥或真实个人数据。

## 本地验证

每个案例目录都包含独立测试：

```bash
cd demos/config-driven-parser
python -m unittest -v

cd ../public-web-text-scraper
python -m unittest -v
```

GitHub Actions 会自动执行所有案例测试。
