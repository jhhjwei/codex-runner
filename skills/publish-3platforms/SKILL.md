---
name: publish-3platforms
description: 把一条已经写好的内容（正文＋图片/封面）一键发到小红书、百家号、今日头条，纯本机脚本驱动已登录的 Safari，发布环节不经过模型、不消耗任何 credits。用于"稿子已经过了闸门，现在要上线"的场景；不负责写稿、配图、选题。发布后强制回读平台列表，回读不到只报告、不重发。
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
metadata:
  trigger: 发布到小红书/百家号/头条、一键发布、图文上线、笔记上线
  source: 2026-11-08 三平台真实发布后固化的产线；脚本事实源 ops/common/publish/，台账 publish-ledger.md
---

# 三平台一键发布（零 credits）

## 什么时候用

稿子已经定了，只差"发出去"。**不用于**写稿、改稿、配图、选题——那些走各平台自己的产线。

## 为什么发布不花钱

拆开一条发布，只有两类动作：判断（字够不够长、图贴没贴对、按钮在哪、到底成没成）本该由模型做，
动作（开页、填标题、贴正文、传图、点发布、回读）不需要判断。这个工具把动作全部写死成脚本，
用 `osascript` 对**你已经登录的 Safari** 执行 `do JavaScript`。

所以发布这一步零模型调用、零会话 token。**注意边界**：接一个新平台的编辑器、或者页面改版后重新
摸选择器，仍然要人陪着看页面，那一段是会花 credits 的。零成本指"接完之后的每一次发布"。

## 前置（只做一次）

1. Safari → 设置 → 开发 → **允许来自 Apple 事件的 JavaScript**。
2. 在 Safari 里**登录**三个平台（小红书创作服务平台、百家号、头条 mp）。
3. 确认通道活着：

```bash
python3 <skill>/scripts/publish.py probe --platform all --out /tmp/probe.json
```

三个都 `logged_in: true` 才继续。哪个 false，就让用户在 Safari 里登录那个平台——
**不要用内置浏览器代替**，那会消耗 credits，也绕开了这条零成本通道。

（`<skill>` 指本 skill 目录；仓库里的等价路径是 `ops/common/publish/`。）

## 内容怎么摆

一条内容一个目录，`manifest.json` 在根，正文单独 txt，图片相对路径：

```
<draft>/
  manifest.json
  xhs/body.txt  bjh/body.txt  tt/body.txt   # 三平台正文可以各写一份
  img/01-cover.png  img/02.png …
```

```json
{
  "schema": "publish/1",
  "targets": [
    {"platform": "xhs", "kind": "note", "title": "≤20 字",
     "body": "xhs/body.txt", "images": ["img/01-cover.png", "img/02.png"],
     "topics": [], "schedule": null},
    {"platform": "baijiahao", "kind": "article", "title": "5–40 字",
     "body": "bjh/body.txt", "images": ["img/01-cover.png"],
     "cover": "img/01-cover.png"},
    {"platform": "toutiao", "kind": "weitoutiao", "title": "只用于台账/回读",
     "body": "tt/body.txt", "images": ["img/01-cover.png"]}
  ]
}
```

规格唯一事实源是 `core/contract.py` 的 `LIMITS`：小红书 note 标题 1–20 字／正文 1–1000／图 1–18；
百家号 article 标题 5–40／正文 200–20000／图 1–20 且必须有封面；头条微头条无标题栏／正文 10–2000／图 0–9。
`check` 会逐条报 BLOCK/WARN，BLOCK 一条都不发。

## 怎么发

```bash
# 1. 校验（不开浏览器）
python3 <skill>/scripts/publish.py check <draft>/manifest.json

# 2. 填表但不发 —— 先看这一遍，这是主力自测模式
python3 <skill>/scripts/publish.py fill <draft>/manifest.json

# 3. 真发（必须 --yes）
python3 <skill>/scripts/publish.py publish <draft>/manifest.json --yes

# 4. 回读（publish 会自动做一次）
python3 <skill>/scripts/publish.py readback --platform xhs --title "标题"
```

结果落 `<draft>/shots/result.json`。

## 铁律

- **`publish --yes` 才点发布键**。fill 模式永远不点。
- **回读不到 = `unconfirmed`，只报告、不重发**（宁缺勿重发）。
- `fill` 通过不代表发得出去，但**不通过一定别发**：它验的是"填进去的样子"。
  头条草稿自动恢复会让正文翻倍（实测 431→832 字），只有 `fill` 的 `body_len` 读数能发现。
- 报错就停。适配器内置硬拦（正文没灌够／图没进够／图多插了／标题被吞字），
  **别加 `|| true` 绕过**，也别在外面再补点一次发布键。
- 一条内容只用同主题素材；缺图就是缺图，不要拿别的图补。
- 屏幕锁着时别发带图的内容，尤其头条（见下）。

## 坑位速查（都已写进适配器，改脚本前先读这段）

| 平台 | 坑 | 现在的做法 |
| --- | --- | --- |
| 小红书 | 正文编辑器已换成 tiptap，`.ql-editor` 失效 | 用 `div.tiptap.ProseMirror` |
| 小红书 | 发布键在闭合影子根里，`el.shadowRoot` 是 null | 只有 `el._sr` 拿得到（WebKit 私有属性） |
| 小红书 | 缩略图不是稳定 `<img>` 集合 | 按 blob URL 增量去重计数 |
| 百家号 | `window.UE` 现在是 undefined | 正文走 `iframe#ueditor_0` 的 `contentWindow.editor` |
| 百家号 | 标题是 Lexical，`selectAll+delete` 会留残字 | `parseEditorState` + `setEditorState` |
| 百家号 | **一次 change 事件里塞全部图** | 逐张塞会重复、卡 0%、确认键点不动 |
| 百家号 | 一张图落成两段容器（图＋图注） | 数图按 `img.src` 去重 |
| 百家号 | 成功不是跳 `/content` | 认 `/builder/rc/clue` + toast「已经发布成功」 |
| 百家号 | 封面已有草稿时只显示「更换」 | 先读封面状态，已设就跳过，不硬开弹窗 |
| 头条 | 改 `innerText` 不进 ProseMirror 模型态 | 先清空并回读 ≤5 字，再派 `text/html` 粘贴事件，贴完卡上界 |
| 头条 | 图片抽屉一次只吃**一个**文件 | 多文件赋值会变成 `files.length=0` |
| 头条 | 「确定」点两次整批重插 | 只点一次，插完回数正文图片数 |

## 已知限制

- v1 不支持视频（`video` 字段留了、三个适配器都没实现，视频走另一套编辑器）。
- 不支持头条长图文（内嵌图那次失败，降级成微头条）。
- 脚本不守候定时：`schedule` 只是记录。要定时就用一次性 `at` 任务在发布时刻起跑这条命令。
- **锁屏时头条插图落不了**：`visibilityState=hidden` 时抽屉能开、能传、能显示已上传，
  点「确定」只关窗不落图。适配器检测到页面不可见就只发文字并把 `images_skipped`
  记进 `result.json`。这是限制不是 bug，解锁才能解。
- Safari 的 `do JavaScript` 只能同步执行（拿不到 Promise），所有等待靠轮询；
  JS 不包函数体会语法错，一律裹 IIFE。
