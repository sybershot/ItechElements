*** Settings ***
Variables  itechframework/configuration/constants.py
Library  itechframework/modules/browser_manager/BrowserManager.py
Library  project/steps/ElementsSteps.py

Test Setup  Open Enviroment
Test Teardown  Close Browser  ${browser}

*** Keywords ***
Open Enviroment
    ${browser} =  Get Browser  ${BROWSER_TYPE}
    ${page_object} =  Open Demo  ${browser}
    Set Suite Variable  ${page_object}
    Set Suite Variable  ${browser}

*** Test Cases ***
Test Droppables
    Open Interactions Menu  ${page_object}
    Open Droppable  ${page_object}
    Get Submenu Contents  ${page_object}
    Open Draggable Tab  ${page_object}
    Perform Drag And Drop  ${page_object}

Test Alerts
    Open Alerts Menu  ${page_object}
    Open Alerts  ${page_object}
    Test Simple Alert  ${page_object}
    Test Timed Alert  ${page_object}
    Test Confirm Alert  ${page_object}
    Test Input Alert  ${page_object}

Test Windows And Tabs
    Open Alerts Menu  ${page_object}
    Open Windows  ${page_object}
    Test New Tab  ${page_object}
    Test New Window  ${page_object}
    Test New Message Window  ${page_object}