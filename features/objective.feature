Feature: 目标管理
  Background: 用户登录成功
    Given 输入租户"sunny",用户名"new001",密码"@new001!"
    And 进入天平首页

  Scenario Outline: 创建定性目标
    Given 进入我的目标菜单
    When 创建目标,目标名称"<name>",目标值"<value>",类型"test1",分类"<category>",单位"<uint>",备注"这是测试说明"
    """
    {"name":"<name>","value":"<value>","obtype":"test1",
    "uint":"<uint>","category":"<category>","content":"<content>"
    }
    """
    Then 检查创建目标结果
    Examples: 测试1
      |name|value|uint|category|content|
      |测试目标6-8|333.3||定性|备注123|
  @create
  Scenario Outline: 创建定量目标
    Given 进入我的目标菜单
    When 创建目标
    '''
      {
      "o_name": "<name>",
      "obtype": ["test1"],
      "content": "11111111111111111",
      "attach":"C:\\Users\\Athur\\Desktop\\aa.txt",
      "value": <value>,
      "category": "<category>",
      "staff":"全员可见",
      "kr": [
        {
          "name": "111111",
          "weigth": 50,
          "obtype": ["test1"],
          "category": "定性",
          "value": 10.1,
          "uint":""
        },
        {
          "name": "11222221111",
          "weigth": 50,
          "obtype": ["test1"],
          "category": "定量",
          "value": 20.1,
          "uint": "<uint>"
        }
      ]
    }
  '''
   and 搜索目标"<name>"
  Then 检查目标"<name>"是否存在"<result>"
   and 检查目标"<name>"状态是否为"<state>"
  Examples: 测试1
    |name|value|uint|category|content|result|state|
    |测试目标8-16|333.3|asd|定性|备注123|是|初定方案|
    |测试目标8-17|333.3|asd|定性|备注123|是|初定方案|

  @delete
  Scenario Outline: 删除目标
    Given 进入我的目标菜单
    When 删除目标"<name>"
    Then 检查目标"<name>"是否存在"<result>"
  Examples: 删除测试
    |name|result|
    |测试目标8-4|否|

  @audit
  Scenario Outline: 提交审核目标
    Given 进入我的目标菜单
    When 搜索目标"<name>"
     and 提交审核"<name>"
     and 切换tab至"<tab_name>"
     and 搜索目标"<name>"
    Then 检查目标"<name>"状态是否为"<state>"
     #and 检查目标"<name>"是否存在"<result>"
  Examples: 提交审核测试
    |name|tab_name|state|
    |测试目标8-14|进行中|确认方案|

  @disabled
  Scenario Outline: 失效目标
    Given 进入我的目标菜单
    When 切换tab至"<tab_name>"
     and 搜索目标"<name>"
     and 失效目标"<name>"
    Then 检查目标"<name>"是否存在"<result>"
     and 检查目标"<name>"状态是否为"<state>"
  Examples: 失效测试
    |name|result|tab_name|state|
    |测试目标8-5|是|进行中|失效审核中|

  @update
  Scenario Outline: 更新目标进度
    Given 进入我的目标菜单
    When 切换tab至"<tab_name>"
    and 更新目标"<name>"进度
  Examples: 失效测试
    |name|tab_name|
    |测试目标8-14|进行中|
