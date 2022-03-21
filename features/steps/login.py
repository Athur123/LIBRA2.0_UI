import logging

from behave import *
from librapage.loginpage import LoginPage


@given("打开登录页面")
def step_impl(context):
    context.page = LoginPage(context.driver)


@when('输入租户"{loginname}",用户名"{username}",密码"{passwd}"')
@given('输入租户"{loginname}",用户名"{username}",密码"{passwd}"')
def step_impl(context, loginname, username, passwd):
    context.execute_steps('''
        given 打开登录页面
    ''')
    context.page = context.page.login(loginname, username, passwd)


@when("进入天平首页")
@given("进入天平首页")
def step_impl(context):
    context.page = context.page.enter_libra_home()


@then('检查登录结果"{result}"')
def step_impl(context, result):
    # assert context.page.title == context.page.get_title if result == "true" else False
    logging.info(context.page.get_title)
    if result == "true":
        assert context.page.title == context.page.get_title
    else:
        assert context.page.title != context.page.get_title
