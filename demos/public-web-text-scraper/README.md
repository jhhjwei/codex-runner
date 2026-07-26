# Public Web Text Scraper

面向公开、无需登录页面的小型文本抓取样品。读取 JSON 配置，遵守 `robots.txt`，按固定间隔访问页面，并输出 CSV 或 JSON。

## 适用范围

- 公开帮助中心或文档页面
- 无登录、无验证码的网站文本归档
- 标题和正文提取
- 小规模、低频率、可审计的数据收集

不适用于绕过登录、验证码、付费墙、访问控制或站点限制。

## 功能

- 配置起始 URL、最大页数、延迟和超时
- 默认只跟随同域链接
- 检查 `robots.txt`
- 过滤脚本、样式和不可见内容
- 提取 URL、标题、正文、状态和错误
- 输出 CSV 或 JSON
- 仅使用 Python 标准库

## 运行

先根据目标站点规则修改 `config.json`：

```bash
python scraper.py --config config.json --output pages.csv
```

## 测试

```bash
python -m unittest -v
```

测试不访问外网，只验证 HTML 提取和 URL 范围控制。

## 可扩展成交版本

- 指定页面范围或路径白名单
- PDF 与文本附件下载
- 增量更新与去重
- JavaScript 页面支持
- Windows 图形界面或可执行文件
- 定时运行、日志和失败重试
- 针对客户授权网站的字段定制
