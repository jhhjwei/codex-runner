# Config-driven CSV/JSON Parser

一个可直接运行的 Python 小样品：字段顺序、目标字段名、类型、默认值、大小写、数值换算和校验规则都放在外部 CSV/JSON 配置中，无需修改核心代码。

## 为什么做这个样品

公开自由职业需求中，经常出现“原始数据格式会变化”“规则不能写死”“需要输出干净 CSV/JSON”的小型自动化项目。这个目录展示了可交付的最小版本。

## 功能

- 输入支持 CSV 或 JSON
- 配置支持 CSV 或 JSON
- 输出支持 CSV 或 JSON
- 支持 string / int / float / bool
- 支持必填、默认值、去空格、大小写转换
- 支持 multiplier / offset 数值换算
- 支持最小值、最大值和枚举校验
- 错误记录输出到独立 JSON 文件
- 仅使用 Python 标准库

## 运行

```bash
python parser.py \
  --config config.csv \
  --input input.csv \
  --output output.json \
  --errors errors.json
```

预期控制台输出：

```text
processed=3 accepted=3 rejected=0
```

## 测试

```bash
python -m unittest -v
```

## 可扩展成交版本

根据客户数据可继续加入：

- Excel 输入输出
- 日期、金额和单位规则
- 多文件批处理
- 字段依赖和条件规则
- 图形界面或网页上传
- 定时任务、日志和失败重试
- 打包为 Windows 可执行文件

需要类似定制，可通过项目主页的“提交技术需求”入口提供脱敏样例和验收标准。
