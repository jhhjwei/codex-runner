# publish-3platforms · 三平台一键发布（发布环节零 credits）

把一条已经写好的内容（正文 ＋ 图片/封面）发到小红书、百家号、今日头条。
**发布这一步不经过模型**：本机 Python 进程用 `osascript` 对你已经登录的 Safari
执行 `do JavaScript`，读 DOM、填表单、点按钮都是本地行为，不进任何会话上下文。

为什么这件事值得单独做成工具：模型该干的是**判断**（字够不够、图贴没贴对、成没成），
不是**动作**（开页、填标题、贴正文、传图、点发布、回读）。把动作写死成脚本之后，
发一次和发一百次的成本一样：零。

## 装

```bash
git clone https://github.com/jhhjwei/codex-runner
cp -R codex-runner/skills/publish-3platforms ~/.qoder-cn/skills/
```

前置：Safari → 设置 → 开发 → 勾选「允许来自 Apple 事件的 JavaScript」；
在 Safari 里登录小红书创作服务平台、百家号、头条号三个后台。

```bash
python3 ~/.qoder-cn/skills/publish-3platforms/scripts/publish.py probe --platform all --out /tmp/probe.json
```

三个都 `logged_in: true` 才继续。

## 用

一条内容一个目录，`manifest.json` 写清楚发给谁、图在哪、正文在哪：

```json
{
  "schema": "publish/1",
  "targets": [
    {"platform": "xhs", "kind": "note", "title": "≤20 字",
     "body": "xhs/body.txt", "images": ["img/01-cover.png", "img/02.png"]},
    {"platform": "baijiahao", "kind": "article", "title": "5–40 字",
     "body": "bjh/body.txt", "images": ["img/01-cover.png"], "cover": "img/01-cover.png"},
    {"platform": "toutiao", "kind": "weitoutiao", "body": "tt/body.txt",
     "images": ["img/01-cover.png"]}
  ]
}
```

```bash
P=~/.qoder-cn/skills/publish-3platforms/scripts/publish.py
python3 $P check   <draft>/manifest.json     # 只校验，不开浏览器
python3 $P fill    <draft>/manifest.json     # 填表但不点发布 —— 主力自测模式
python3 $P publish <draft>/manifest.json --yes
python3 $P readback --platform xhs --title "标题"
```

结果落 `<draft>/shots/result.json`。

## 三道闸

1. `check`：标题超长、图缺、字数不够、格式不收 → BLOCK，不发。
2. `fill`：填进去但不点发布，看"填进去的样子"对不对。
3. `publish --yes`：真发，发完强制回读平台列表；回读不到记 `unconfirmed`，**不重发**。

## 平台差异（全部实测踩出来的，已写进适配器）

| 平台 | 关键点 |
| --- | --- |
| 小红书 | 正文是 tiptap；发布键在闭合影子根里（`el._sr`）；数图按 blob URL 增量 |
| 百家号 | 正文编辑器在 `iframe#ueditor_0` 的 `contentWindow.editor`（`window.UE` 已失效）；标题是 Lexical；**一次 change 事件塞全部图**；一张图落两段容器，按 `img.src` 去重；成功跳 `/builder/rc/clue` 不是 `/content` |
| 头条 | ProseMirror 必须派 `text/html` 粘贴事件；草稿自动恢复会让正文翻倍；图片抽屉一次只吃一个文件；「确定」只点一次，点两次整批重插 |

## 已知限制

- v1 不发视频（字段留了，适配器没实现）。
- 不支持头条长图文（内嵌图），只做微头条。
- 不守候定时：`schedule` 只是记录，到点发布交给定时任务起跑这条命令。
- 锁屏时头条插图落不了（`visibilityState=hidden` 点「确定」只关窗），适配器降级成纯文字并记 `images_skipped`。
- 本机 WebDriver 路不通（macOS 27 上 `POST /session` 恒报未开远程自动化），所以走 AppleScript。

细节与原文写在 [SKILL.md](SKILL.md)。
