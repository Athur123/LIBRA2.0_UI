import json
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from librapage.basepage import BasePage, _D
from selenium.webdriver.common.by import By

from typing import Union, TypeVar, Tuple, List, Mapping
from selenium.webdriver.support.relative_locator import locate_with


class PersonalBoardPage(BasePage):
    title = "我的目标"

    buttons = (By.CSS_SELECTOR, ".outer-box-border-header .outer-box-border-btn-group button")
    add_button: str = "新增目标"
    finish_button: str = "完成目标"
    search_input = (By.CSS_SELECTOR, 'app-search-block nz-input-group input')
    search_button = (By.CSS_SELECTOR, 'app-search-block nz-input-group button')
    objective_items = (By.CSS_SELECTOR, 'app-objective-list-item .item-header-title')
    tabs = (By.CSS_SELECTOR, '.ant-tabs-nav-container .ant-tabs-tab')
    objective_checkbox = (By.CSS_SELECTOR, '.objective-checkbox')
    objective_status = (By.CSS_SELECTOR, '.item-header-tags')
    # 是否关注的icon
    objective_icon = (By.CSS_SELECTOR, '.item-header-icon >i>svg')
    # 编辑完成情况按钮
    completion_button = (By.CSS_SELECTOR, '.completion-link-btn>button')

    # 目标创建时间、类型等content内容
    objective_items_content = (By.CSS_SELECTOR, 'app-objective-list-item .objective-item-content')
    # 完成值
    objective_completion_value = (By.CSS_SELECTOR, 'app-objective-value > input')
    # 完成进度
    objective_completion_progress = (By.CSS_SELECTOR, '[formcontrolname="accomplishProgress"] input')

    def create_objective_page(self):
        """
        创建目标
        :return: 新增目标子页面
        """

        self.click(self.buttons, self.add_button)

        return CreateObjectivePage(self.driver)

    def search_objective(self, objective_name, search: bool = False, delay: int = 0) -> bool:
        """

        :param delay: 延迟时间，搜索结果延迟时间
        :param objective_name:搜索的目标名称
        :param search:是否请求搜索，为false时，不执行搜索，直接在列表检索目标，为True时，执行搜索指定目标
        :return:
        """
        if delay:
            time.sleep(delay)
        if search:
            self.type(self.search_input, objective_name)
            self.click(self.search_button)
        try:
            self.get_text_element(self.objective_items, objective_name)
        except NoSuchElementException:
            return False
        else:
            return True

    def switch_tab(self, tab_name: str):
        # logging.debug(f"进入tab{tab_name}")
        self.click(self.tabs, tab_name)

    # 操作目标
    def objective_action(self, action_type: str, objectives_names: Union[List[str], str]):
        """
        :param action_type: 关注、提交审核、失效、删除、完成目标
        :param objectives_names:目标名称，支持批量操作
        :return:
        """
        objectives_names = objectives_names if isinstance(objectives_names, List) else [objectives_names]
        for objective_name in objectives_names:
            e = self.get_text_element(self.objective_items, objective_name)
            c = locate_with(*self.objective_checkbox).to_left_of(element_or_locator=e)
            es = self.driver.find_elements(c)
            es[0].click()
            logging.info(es)
        self.click(self.buttons, action_type)
        if self.is_element_visibility(self.confirm_modal_buttons):
            self.modal_action("确定")

    def check_objective_state(self, objective_name, objective_state) -> bool:
        """
        :param objective_state: 目标状态
        :param objective_name:目标名称
        :param objective_status:目标状态
        :return:bool
        """
        e = self.get_text_element(self.objective_items, objective_name)
        if not e:
            raise f"找不到目标{objective_name}"
        c = locate_with(*self.objective_status).to_right_of(element_or_locator=e)
        try:
            # self.get_text_element(c,objective_state)
            # e_status = self.driver.find_element(c)
            if self.get_text_element(c, objective_state):
                return True
            else:
                return False
        except TimeoutError:
            raise f"找不到目标状态{objective_name}"

    def check_attention_state(self, objective_name, is_attention: bool = False) -> bool:
        """
        :param objective_name:目标名称
        :param is_attention:目标状态
        :return:bool
        """
        e = self.get_text_element(self.objective_items, objective_name)
        if not e:
            raise f"找不到目标{objective_name}"
        c = locate_with(*self.objective_icon).to_right_of(element_or_locator=e)
        return self.is_locator_exist(c)

    def update_objective_progress(self, objective_name: str, objective_completion_value: str,
                                  objective_completion_progress: int = None) -> bool:
        e = self.get_text_element(self.objective_items, objective_name)
        # 获取目标的文本描述行内容
        items_content = locate_with(*self.objective_items_content).below(element_or_locator=e)
        # 定位点击更新进度按钮
        edit_button = self.driver.find_element(items_content).find_element(
            *self.completion_button)
        # 点击更新进度按钮
        self.click(edit_button)
        # logging.info
        self.type_form_item(self.modal, "完成值", objective_completion_value)
        if objective_completion_progress:
            self.type_form_item(self.modal, "完成进度", str(objective_completion_progress))
        self.modal_action("确认")
        # 检查更新提示文本
        return self.is_test_to_be_present(self.msg, "更新完成值成功")


class CreateObjectivePage(BasePage):
    title = "新增我的目标"

    objectiveName = (By.CSS_SELECTOR, '[formcontrolname="objectiveName"]')
    objectiveValue = (By.CSS_SELECTOR, '[formcontrolname="objectiveValue"]>input')
    # 目标分类
    objectiveTypeId = (By.CSS_SELECTOR, '[formcontrolname="objectiveTypeId"]>nz-select')

    # 定性/量
    category = (By.CSS_SELECTOR, '[formcontrolname="category"]')
    # 目标描述
    content = (By.CSS_SELECTOR, '[formcontrolname="content"]')
    # button
    buttons = (By.CSS_SELECTOR, '.objective-footer button')

    add_key_result_button = (By.CSS_SELECTOR, '.objective-add .kr-form-container button')
    base_form = (By.CSS_SELECTOR, '.objective-add>div> form:first-child')
    kr_form: str = "app-new-kr-form:nth-child({index}) form"

    # 更多设置
    more_set = (By.CSS_SELECTOR, 'app-dashed-collapse .btn:first-child')
    save: str = "保存"
    message = (By.CSS_SELECTOR, '.cdk-overlay-container .ant-message')

    def create_objective(self, *args, **kwargs):
        """
        新增目标
        :param args:
        :param kwargs:
            o_name:目标名称
            category:定量/定性
            value:目标值
            uint:单位
            content：目标描述
            obtype：目标分类，List[str]
            attach:附件
            kr:Object，关键结果

        :return:
        """
        self.type_form_item(self.base_form, "目标名称", kwargs.get('o_name', None))
        self.type_form_item(self.base_form, "定性/量", kwargs.get('category', None))
        self.type_form_item(self.base_form, "目标值", kwargs.get('value', None))
        if kwargs.get('uint', None):
            logging.info(" ".join([self.base_form[1], self.select_ant[1]]))
            self.select_from_dropdown((By.CSS_SELECTOR, " ".join([self.base_form[1], self.select_ant[1]])),
                                      loc_text="请选择单位",
                                      choose_text=kwargs.get('uint'))
        self.click(self.more_set)
        self.type_form_item(self.base_form, "目标描述", kwargs.get('content', None))
        self.type_form_item(self.base_form, "分类", kwargs.get('obtype', None))
        if kwargs.get('attach', None):
            self.type_form_item(self.base_form, "上传附件", kwargs.get('attach'))
        self.type_form_item(self.base_form, "适用员工", kwargs.get('staff', None))
        krs: List[Mapping, ...] = kwargs.get('kr', None)
        logging.info(json.dumps(kwargs, ensure_ascii=False))
        if krs:
            for index, kr in enumerate(krs):
                self.click(self.add_key_result_button, '新增关键结果')
                _s = self.kr_form.format(index=(index + 1))
                logging.info(f"这是第几个？{index + 1}\t{_s}")
                _f = (By.CSS_SELECTOR, _s)
                self.type_form_item(_f, "关键结果名称", kr.get("name", None))
                self.type_form_item(_f, "权重", kr.get("weigth", None))
                self.type_form_item(_f, "分类", kr.get("obtype", None))
                self.type_form_item(_f, "定性/量", kr.get("category", None))
                self.type_form_item(_f, "目标值", kr.get("value", None))
                if kr.get('uint', None):
                    logging.info(kr.get("uint"))
                    self.select_from_dropdown((By.CSS_SELECTOR, " ".join([_s, self.select_ant[1]])),
                                              loc_text="请选择单位",
                                              choose_text=kr.get("uint"))
        self.click(self.buttons, self.save)
        if self.is_test_to_be_present(self.message, "目标已保存！"):
            return PersonalBoardPage(self.driver)
        else:
            return self
