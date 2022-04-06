from robot.api.logger import error

from itechframework.modules.robot_browser.browser import Browser
from itechframework.modules.base_page.base_page import BasePage
from itechframework.modules.robot_browser.browser_element import BrowserElement


class ElementsPage(BasePage):
    ACCORDION_LIST_LOCATOR = '//div[@class="element-group"]/span'
    PAGE_CONTENTS_LOCATOR = '//div[contains(@class, "md-6")]/div[not(contains(@class, "Advertisement"))]'
    MENU_ELEMENTS_LOCATOR = '//div[contains(@class, "show")]/ul/li'

    def __init__(self, browser: Browser):
        super().__init__(browser)
        self.elements, self.forms, self.alertframewin, self.widgets, self.interactions, self.book_store =\
            self.browser.find_elements('xpath', self.ACCORDION_LIST_LOCATOR)
        self.menu_contents = None
        self.page_contents = None

    def get_element_list(self, parent: BrowserElement):
        element_list = self.browser.find_elements('xpath', self.MENU_ELEMENTS_LOCATOR)
        return element_list

    def open_menu(self, menu_element: BrowserElement):
        if menu_element.element.find_element('xpath', '..').text in menu_element.element.text:
            menu_element.move_to_element()
            menu_element.click_element()
            self.browser.wait_until_visible('xpath', self.MENU_ELEMENTS_LOCATOR)
        self.menu_contents = self.get_element_list(menu_element)

    def open_submenu(self, submenu_element: BrowserElement):
        submenu_element.click_element()
        self.page_contents = self.browser.find_element_or_raise('xpath', self.PAGE_CONTENTS_LOCATOR)

    def update_contents(self, by, locator):
        self.page_contents = self.browser.find_elements(by, locator)
        if not self.page_contents:
            error(f"Couldn't find any of the submenu contents by {by} {locator}!")
            raise Exception('PageContentsUpdateException')
