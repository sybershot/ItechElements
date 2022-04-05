*** Settings ***
Variables  configuration/constants.py
Library  itechframework/modules/browser_manager/BrowserManager.py
Library  project/steps/ElementsSteps.py

Test Setup  Open Browser
Test Teardown  Close Browser  ${browser}

*** Keywords ***
Open Browser
    ${browser} =  Get Browser  ${BROWSER_TYPE}
    Set Suite Variable  ${browser}

*** Test Cases ***
Test Droppables
    Open Browser
    ${page_object} =  Open Demo  ${browser}
    Open Interactions Menu  ${page_object}
    Open Droppable  ${page_object}
    Get Submenu Contents  ${page_object}
    Open Draggable Tab  ${page_object}
    Perform Drag And Drop  ${page_object}
