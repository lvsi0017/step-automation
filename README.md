# step-automation
每天自动提交步数到“王走走”平台（GitHub Actions 定时运行）

## 使用方式
1. 把本仓库 **Fork** 到你的账号下
2. 进入 `Settings → Secrets and variables → Actions → New repository secret`
   - Name: `ACCOUNTS`
   - Value: 单行 JSON，例：
     ```
     [{"username":"yundong11@126.com","password":"lvsi0017"},{"username":"yundong5@163.com","password":"lvsi0017"}]
     ```
3. 每天 UTC 5:30 自动运行，也可手动触发：`Actions → Run Step Submitter → Run workflow`
4. 运行日志在 Actions 控制台查看
