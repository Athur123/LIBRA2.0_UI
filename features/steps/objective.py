import logging

from behave import *
from librapage.personal_board import *
import json
from parse_type import TypeBuilder
import parse


@parse.with_pattern(r"\w*")
def type_test(text):
    logging.info("单位：{}".format(text))
    return text


register_type(MM=type_test)


@given("进入我的目标菜单")
def step_impl(context):
    context.page = context.page.enter_personal_board()


@when('创建目标')
def step_impl(context):
    logging.info(context.text)
    req_json = json.loads(context.text)
    # logging.info(json.loads(t))
    logging.info(req_json)
    context.page = context.page.create_objective_page()
    context.page = context.page.create_objective(**req_json)


@when('删除目标"{name}"')
def step_impl(context, name):
    context.page.objective_action(action_type="删除", objectives_names=name)


@when('提交审核"{name}"')
def step_impl(context, name):
    context.page.objective_action(action_type="提交审核", objectives_names=name)


@when('关注目标"{name}"')
def step_impl(context, name):
    context.page.objective_action(action_type="关注", objectives_names=name)


@when('失效目标"{name}"')
def step_impl(context, name):
    # context.page.switch_tab("进行中")
    context.page.objective_action(action_type="失效", objectives_names=name)


@when('完成目标"{name}"')
def step_impl(context, name):
    # context.page.switch_tab("进行中")
    context.page.objective_action(action_type="完成目标", objectives_names=name)


@when('切换tab至"{tab_name}"')
def step_impl(context, tab_name):
    context.page.switch_tab(tab_name)


@when('搜索目标"{name}"')
@then('搜索目标"{name}"')
def step_impl(context, name):
    context.page.search_objective(name, search=True)


@when('更新目标"{name}"完成值"{value}"')
@when('更新目标"{name}"完成值"{value}"进度"{progress}"')
def step_impl(context, name, value, progress=None):
    context.page.update_objective_progress(name, objective_completion_value=value,
                                           objective_completion_progress=progress)


@then('检查目标"{name}"是否存在"{result}"')
def step_impl(context, name, result):
    res = context.page.search_objective(name, search=False)
    logging.info(f"搜索结果{res}")
    if result == '是':
        assert res
    else:
        assert not res


@then('检查目标"{name}"状态是否为"{state}"')
def step_impl(context, name, state):
    assert context.page.check_objective_state(objective_name=name, objective_state=state)


@then('检查目标"{name}"状态是否已关注"{attention_state}"')
def step_impl(context, name, attention_state):
    r = context.page.check_attention_state(objective_name=name, is_attention=attention_state)
    logging.info(f"检查结果：{r}")
    assert r
