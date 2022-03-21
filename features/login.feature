Feature: 登录天平
  Scenario: 验证天平首页正常进入
    When 输入租户"sunny",用户名"new001",密码"@new001!"
    and 进入天平首页
    Then 检查登录结果"true"

