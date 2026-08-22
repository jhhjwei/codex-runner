# Maven 构建故障急救

本仓库现在只承接一种固定范围的交付：修复一个可在本地复现的 Maven 依赖或构建阻塞。

## 固定服务

- 免费预检：判断问题能否复现、是否属于固定范围
- 价格：65 美元固定价
- 时间：接受可复现输入后 24 小时内交付
- 验收：事先约定的 Maven 命令返回 0
- 售后：48 小时内一次同范围修订

交付包括补丁或修正后的 `pom.xml`、修复前后依赖树、验证命令与日志、简短根因报告。

不承接生产环境登录、部署、数据库故障、新功能、长期维护、账号共享或包含凭据的任务。

## 入口

- 服务主页：https://jhhjwei.github.io/codex-runner/
- 免费预检：https://github.com/jhhjwei/codex-runner/issues/new?template=code-fix-request.yml
- 公开验证案例：[`demos/maven-build-rescue`](demos/maven-build-rescue)

## 验证案例

案例包含相同 Java 源码的故障版和修复版。故障版因依赖版本过旧无法编译，修复版升级依赖后可通过 Maven 构建。

```bash
cd demos/maven-build-rescue
bash verify.sh
```

GitHub Actions 会同时证明故障版失败、修复版成功。搜索、解释或未运行的修改不计为交付。
