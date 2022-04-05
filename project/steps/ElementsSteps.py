from robot.api.deco import keyword
from robot.api.logger import info

from itechframework.modules.robot_browser.browser import Browser
from configuration.constants import DEMO_URL, ALERT_TEXT
from project.page_objects.elemens_page import ElementsPage


class ElementsSteps:
    NAV_TABS_LOCATOR = '//nav[contains(@class, "nav-tabs")]/a'
    DRAGGABLE_TAB_LOCATOR = '//div[@class="revertable-drop-container"]'
    DRAGGABLE_OBJECTS_LOCATOR = '//div[@id="revertableDropContainer"]/div/div[contains(@class,"drag-box")]'
    DRAGGABLE_TARGET_LOCATOR = '//div[@id="revertableDropContainer"]/div[@id="droppable"]'
    ALERT_BUTTONS_LOCATOR = '//button[contains(@id, "Button")]'
    ALERT_CONFIRM_RESULT_LOCATOR = '//span[@id="confirmResult"]'
    PROMPT_RESULT_LOCATOR = '//span[@id="promptResult"]'

    @staticmethod
    @keyword(name="Open Demo")
    def open_demo(browser: Browser):
        browser.go_to(DEMO_URL)
        return ElementsPage(browser)

    @staticmethod
    @keyword(name="Open Interactions Menu")
    def open_interactions(page: ElementsPage):
        page.open_menu(page.interactions)

    @staticmethod
    @keyword(name="Open Droppable")
    def open_droppable(page: ElementsPage):
        page.open_submenu(page.menu_contents[3])

    @staticmethod
    @keyword(name="Get Submenu Contents")
    def get_submenu_contents(page: ElementsPage):
        page.update_contents('xpath', ElementsSteps.NAV_TABS_LOCATOR)

    @staticmethod
    @keyword(name="Open Draggable Tab")
    def open_draggable_tab(page: ElementsPage):
        page.page_contents[3].click_element()
        page.update_contents('xpath', ElementsSteps.DRAGGABLE_TAB_LOCATOR)


    @staticmethod
    @keyword(name="Perform Drag And Drop")
    def perform_drag_and_drop(page: ElementsPage):
        sources = page.browser.find_elements('xpath', ElementsSteps.DRAGGABLE_OBJECTS_LOCATOR)
        target = page.browser.find_element_or_raise('xpath', ElementsSteps.DRAGGABLE_TARGET_LOCATOR)
        revert_location = sources[0].element.location
        norevert_location = sources[1].element.location
        for i in sources:
            i.drag_and_drop(target)
            if 'Dropped!' not in target.element.text:
                raise Exception(f'Target did not update after drag and drop action!')
        if revert_location == sources[0].element.location and norevert_location != sources[1].element.location:
            return True
        else:
            raise Exception(f'Something went wrong when doing drag and drop!')

    @staticmethod
    @keyword(name="Open Alerts Menu")
    def open_alerts_menu(page: ElementsPage):
        page.open_menu(page.alertframewin)

    @staticmethod
    @keyword(name="Open Alerts")
    def open_alerts(page: ElementsPage):
        page.open_submenu(page.menu_contents[1])
        page.update_contents('xpath', ElementsSteps.ALERT_BUTTONS_LOCATOR)

    @staticmethod
    @keyword(name="Test Simple Alert")
    def test_simple_alert(page: ElementsPage):
        page.page_contents[0].click_element()
        page.browser.wait_for_alert()
        page.browser.alert.accept()
        info(f'Successfully accepted simple alert.')

    @staticmethod
    @keyword(name="Test Timed Alert")
    def test_timed_alert(page: ElementsPage):
        page.page_contents[1].click_element()
        page.browser.wait_for_alert()
        page.browser.alert.accept()
        info(f'Successfully accepted timed alert.')

    @staticmethod
    @keyword(name="Test Confirm Alert")
    def test_confirm_alert(page: ElementsPage):
        page.page_contents[2].click_element()
        page.browser.wait_for_alert()
        page.browser.alert.accept()
        if element := page.browser.find_element_or_raise('xpath', ElementsSteps.ALERT_CONFIRM_RESULT_LOCATOR):
            info(f'Successfully accepted confirmed alert. Result: {element.element.text}')

    @staticmethod
    @keyword(name="Test Input Alert")
    def test_input_alert(page: ElementsPage):
        page.page_contents[3].click_element()
        page.browser.wait_for_alert()
        page.browser.alert.send_keys(ALERT_TEXT)
        page.browser.alert.accept()
        element = page.browser.find_element_or_raise('xpath', ElementsSteps.PROMPT_RESULT_LOCATOR)
        assert ALERT_TEXT in element.element.text, f'Cannot find {ALERT_TEXT} in {element.element.text}!'
        info(f'Successfully entered {ALERT_TEXT} in alert input.\nResult:{element.element.text}')
