from robot.api.logger import info, debug, warn
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver import ActionChains

from itechframework.configuration.constants import BROWSER_TYPE
from itechframework.modules.waitutils import waituntiltrue


def updateifstale(func, max_attempts=5):
    def wrapper(self, *args, **kwargs):
        attempt = 1
        while True:
            try:
                func(self, *args, **kwargs)
            except StaleElementReferenceException:
                warn(f'Tried to interact with stale element {self.by!r} {self.locator!r}! Updating...')
                if attempt >= max_attempts:
                    raise Exception(f'Maximum number of tries reached for {self.by!r} {self.locator!r}!')
                self.update_element()
                attempt += 1
                continue
            return func

    return wrapper


class BrowserElement:
    GOOGLE_AD_BANNER_CLOSE_LOCATOR = '//a[@id="close-fixedban"]'

    def __init__(self, element, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        self.browser = BrowserManager().get_browser(BROWSER_TYPE)
        self.element = element
        self.by = by
        self.locator = locator

    @classmethod
    def from_locator(cls, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        browser = BrowserManager().get_browser(BROWSER_TYPE)
        return browser.find_element_or_raise(by, locator)

    @classmethod
    def find_elements(cls, by, locator):
        from itechframework.modules.browser_manager.BrowserManager import BrowserManager

        browser = BrowserManager().get_browser(BROWSER_TYPE)
        return [BrowserElement(e.element, by, locator) for e in browser.find_elements(by, locator)]

    @updateifstale
    def input_text(self, text):
        info(f'Sending {text!r} to {self.by!r} {self.locator!r}')
        self.element.send_keys(text)

    @updateifstale
    def click_element(self, max_attempts=5):
        debug(f'Clicking {self.by!r} {self.locator!r}')
        try:
            if self.wait_clickable():
                self.log_screenshot()
                self.element.click()
            else:
                return False
        except ElementClickInterceptedException:
            warn(f'Element by {self.by!r} {self.locator!r} is obstructed!'
                 f'Looking for advert banners and closing them if possible...')
            ad_banner_close = self.browser.find_elements('xpath', self.GOOGLE_AD_BANNER_CLOSE_LOCATOR)
            if ad_banner_close:
                for i in ad_banner_close:
                    i.element.click()
            self.element.click()

    def move_to_element(self):
        debug(f'Moving to {self.by!r} {self.locator!r}')
        self.browser.driver.execute_script("arguments[0].scrollIntoView();", self.element)

    def log_screenshot(self):
        info(f'<img src="data:image/png;base64, {self.element.screenshot_as_base64}">', html=True)

    @waituntiltrue
    def wait_clickable(self):
        if self.element.is_displayed() and self.element.is_enabled():
            return True

    def update_element(self):
        self.element = BrowserElement.from_locator(self.by, self.locator).element

    def drag_and_drop(self, target):
        info(f'Performing drag and drop of {self.by!r} {self.locator!r} to {target.by!r} {target.locator!r}')
        cursor: ActionChains = ActionChains(self.browser.driver).drag_and_drop(self.element, target.element)
        cursor.perform()
