import json
from selenium import webdriver
from selenium.webdriver import Chrome, Firefox, Edge
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Union, TypeVar, Tuple, List, Optional
import logging
from librapage.config import BASE_URL
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import urljoin
import pyautogui
from enum import Enum, unique
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import RelativeBy

_D = Union[Chrome, Firefox, Edge]
_Loc_E = TypeVar('_Loc_E', WebElement, Tuple[str, str])
_Loc = Tuple[str, str]


@unique
class FormControlType(Enum):
    input = 'input.ant-input'
    number = 'input.ant-input-number-input'
    textarea = 'textarea.ant-input'
    select = 'nz-select.ant-select'
    # select_single = 'nz-select.ant-select>.ant-select-selection--single'
    upload = 'nz-upload'
    # select_multiple = 'nz-select.ant-select >.ant-select-selection--multiple'


class BasePage:
    _poll = 1
    title: str = None
    # 下拉选择
    select_value = (By.CSS_SELECTOR, '.cdk-overlay-pane .ant-select-dropdown ul>li')
    select_ant = (By.CSS_SELECTOR, 'nz-select .ant-select-selection__rendered')
    # 确认模态框按钮组
    confirm_modal_buttons = (By.CSS_SELECTOR, '.ant-modal-body .ant-modal-confirm-btns button')
    # 带表单模态框按钮组
    modal_buttons = (By.CSS_SELECTOR, '.ant-modal-content button.ant-btn')
    # 模态框
    modal = (By.CSS_SELECTOR, '.ant-modal-body')
    # 提示信息
    msg = (By.CSS_SELECTOR, 'nz-message-container>.ant-message nz-message')

    def __init__(self, driver: _D, timeout=10) -> None:

        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver=self.driver, timeout=self.timeout, poll_frequency=BasePage._poll)
        if not self.check_title():
            logging.error("\n当前请求页面title:\t{0}\n预期请求页面title:\t{1}".format(self.get_title, self.title))
            raise Exception("页面请求出错")

    def check_title(self) -> bool:
        _t = time.time()
        result = False
        while time.time() < _t + self.timeout:
            if self.get_title != self.title:
                time.sleep(BasePage._poll)
            else:
                result = True
                break
        return result

    def open(self, url: str):
        if url.startswith("http"):
            url = str(url).strip()
        else:
            url = urljoin(BASE_URL, url)
        self.driver.get(url)

    def clear(self, loc):
        element = self.wait.until(EC.visibility_of_element_located(loc))
        element.clear()

    def click(self, loc: _Loc_E, text: str = None, delay: Union[int, float] = 0.5) -> WebElement:
        e: WebElement
        if text:
            e = self.get_text_element(loc, text)

        else:
            e = loc if type(loc) == WebElement else self.wait.until(EC.element_to_be_clickable(loc))
        e.location_once_scrolled_into_view
        e.click()

        time.sleep(delay)
        return e

    def type(self, loc: _Loc_E, text) -> None:
        element: WebElement = self.wait.until(EC.visibility_of_element_located(loc)) if type(loc) != WebElement else loc
        element.location_once_scrolled_into_view
        logging.info(f"文本内容 {element.text}")
        element.clear()
        element.send_keys(text)

    def is_test_to_be_present(self, loc: _Loc, text: str = None):
        _start_time = time.time()
        try:
            _element = self.driver.find_element(*loc)
            while time.time() < self.timeout + _start_time:
                if _element.text.find(text) != -1:
                    return True
                else:
                    time.sleep(self._poll)
                    continue
            return False
        except EC.NoSuchElementException:
            raise "定位不到相关页面元素"

    def get_text(self, loc: _Loc_E) -> str:
        return self.wait.until(EC.visibility_of_element_located(loc)).text if type(loc) != WebElement else loc.text

    def get_text_element(self, loc: Union[_Loc, RelativeBy], text) -> Union[WebElement, None]:
        """

        :param loc:
        :param text: 期望匹配的元素text
        :return: 所有匹配的元素中text与参数text一致的第一个元素
        """
        try:
            # elements = self.wait.until(EC.visibility_of_any_elements_located(loc))
            elements = self.wait.until(visibility_of_any_elements_located(loc))

        except TimeoutException:
            raise NoSuchElementException(f"找不到匹配的页面元素:{text}")
        logging.info(json.dumps([i.text for i in elements], ensure_ascii=False))
        # logging.info("匹配到的元素信息：{0}".format(json.dumps([i.text for i in elements], ensure_ascii=False)))
        elements = list(filter(lambda e: e.text == text, elements))
        # logging.info("匹配到的元素信息：{0}".format(json.dumps(elements, ensure_ascii=False)))
        if elements:
            return elements[0]
        else:
            raise NoSuchElementException(f"找不到匹配的页面元素:{text}")

    def select_from_dropdown(self, loc: _Loc_E, choose_text: Union[List[str], str],
                             loc_text: Optional[str] = None):
        self.click(loc, loc_text)
        elements = self.wait.until(EC.visibility_of_all_elements_located(self.select_value))
        _es: List[WebElement, ...]
        logging.info(
            f"locator is :{loc}\t choose_text is {choose_text}\tloc_text is {json.dumps([i.text for i in elements], ensure_ascii=False)}")
        _es = list(filter(lambda e: e.text == choose_text if isinstance(choose_text, str) else e.text in choose_text,
                          elements))

        if _es:
            for _e in _es:
                if not _e.is_displayed():
                    _e.location_once_scrolled_into_view
                _e.click()
                if isinstance(choose_text, str):
                    break
            if isinstance(choose_text, List):
                pyautogui.press('esc', interval=1)
                time.sleep(1)
        else:
            logging.error(f"期望选择下拉值:\t{choose_text}")
            raise NoSuchElementException("找不到匹配的选项")

    @property
    def get_title(self) -> str:
        return self.driver.title

    def type_form_item(self, form_loc: _Loc_E, label: str, text: str = None):
        if text is None:
            return
            # css_form_item = 'nz-form-item '
        css_form_label = "nz-form-item  > nz-form-label "
        css_form_control = "nz-form-item  > nz-form-label + nz-form-control"
        base_form_element: WebElement = self.driver.find_element(*form_loc) if type(
            form_loc) != WebElement else form_loc
        elements_label: List[WebElement, ...] = base_form_element.find_elements(By.CSS_SELECTOR, css_form_label)
        elements_control: List[WebElement, ...] = base_form_element.find_elements(By.CSS_SELECTOR, css_form_control)
        result: bool = False

        for index, element in enumerate(elements_label):
            if self.get_text(element) == label:
                logging.info(f"找到元素{index}")
                _e_control = elements_control[index]
                for form_control_type_name, form_control_type_value in FormControlType.__members__.items():
                    # for css_class in ['input.ant-input', 'textarea.ant-input', 'nz-select.ant-select', 'nz-upload']:
                    try:
                        _p: WebElement = _e_control.find_element(By.CSS_SELECTOR, form_control_type_value.value)
                    except EC.NoSuchElementException as e:
                        continue
                    else:
                        # if css_class != 'nz-select':
                        if form_control_type_name in ['input', 'number', 'textarea']:
                            if form_control_type_name == "number":
                                webdriver.ActionChains(self.driver).double_click(_p).send_keys(
                                    Keys.BACKSPACE).send_keys(
                                    text).perform()
                            else:
                                self.type(_p, text)
                        elif form_control_type_name == 'select':
                            self.select_from_dropdown(_p, choose_text=text)
                        # elif form_control_type_name == 'select_multiple':
                        #     self.select_from_dropdown(_p, choose_text=text)
                        elif form_control_type_name == 'upload':
                            self.upload(_p, text)
                        result = True
                        break
                break
        if not result:
            raise "错误"

    def upload(self, locator: _Loc_E, filename: str, delay: Union[int, float] = 2):

        self.click(locator, delay=1)

        # 支持中文
        pyperclip.copy(filename)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 不支持中文
        # pyautogui.write(filename)
        # pyautogui.write("C:\\Users\\Athur\\Desktop\\新建文本文档.txt")
        pyautogui.press('enter', interval=0.1)
        if delay > 0:
            time.sleep(delay)

    def modal_action(self, text: str):

        try:
            self.click(self.modal_buttons, text)
        except NoSuchElementException:
            raise f"按钮{text}不存在"

    def is_element_visibility(self, locator: _Loc_E) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_locator_exist(self, locator) -> bool:
        start = time.time()
        res = False
        while time.time() < start + self.timeout:
            try:
                self.driver.find_element(locator)
            except:
                time.sleep(self._poll)
                continue
            else:
                res = True
                break
        return res


def visibility_of_any_elements_located(locator: Union[_Loc, RelativeBy]):
    def _predicate(driver):
        elements = driver.find_elements(locator) if isinstance(locator, RelativeBy) else driver.find_elements(
            *locator)
        return [element for element in elements if EC.visibility_of(element)]

    return _predicate
