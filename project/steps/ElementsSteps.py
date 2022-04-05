from robot.api.deco import keyword

from itechframework.modules.robot_browser.browser import Browser
from configuration.constants import DEMO_URL
from project.page_objects.elemens_page import ElementsPage


class ElementsSteps:

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
        page.update_contents('xpath', '//nav[contains(@class, "nav-tabs")]/a')

    @staticmethod
    @keyword(name="Open Draggable Tab")
    def open_draggable_tab(page: ElementsPage):
        page.page_contents[3].click_element()
        page.update_contents('xpath', '//div[@class="revertable-drop-container"]')


    @staticmethod
    @keyword(name="Perform Drag And Drop")
    def perform_drag_and_drop(page: ElementsPage):
        sources = page.browser.find_elements('xpath', '//div[@id="revertableDropContainer"]/div/div[contains(@class,"drag-box")]')
        target = page.browser.find_element_or_raise('xpath', '//div[@id="revertableDropContainer"]/div[@id="droppable"]')
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
