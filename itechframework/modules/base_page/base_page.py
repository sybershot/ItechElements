from itechframework.modules.robot_browser.browser import Browser


class BasePage:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.url = browser.get_location

    def save_screenshot(self, fname):
        self.browser.capture_page_screenshot(fname)

    def get_current_location(self):
        return self.url
