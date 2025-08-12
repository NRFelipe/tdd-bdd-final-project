# features/steps/ui_buttons_steps.py
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _button_id(label: str) -> str:
    # Ajuste os IDs se seu index.html usar outros!
    mapping = {
        "Create": "create-btn",
        "Clear": "clear-btn",
        "Retrieve": "retrieve-btn",
        "Update": "update-btn",
        "Delete": "delete-btn",
        "Search": "search-btn",
    }
    if label not in mapping:
        raise AssertionError(f"Unknown button label: {label}")
    return mapping[label]

@when('I press the "{button}" button')
def step_press_button(context, button):
    btn_id = _button_id(button)
    driver = context.driver
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, btn_id)))
    driver.find_element(By.ID, btn_id).click()

@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    driver = context.driver
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "flash_message")))
    text = (driver.find_element(By.ID, "flash_message").text or "").strip()
    assert message in text, f'Expected flash message to contain "{message}", got "{text}"'
