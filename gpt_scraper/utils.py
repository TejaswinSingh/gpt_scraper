from selenium.webdriver.common.by import By


def select_input_field(fields, inputmode=None, id="", name=None, tag_name=""):
    # Iterate over the fields
    for field in fields:
        # Check if the element has the desired attributes
        if (
            field.get_attribute("inputmode") == inputmode
            and (field.get_attribute("name") == name or field.tag_name == tag_name)
            and field.get_attribute("id") == id
        ):
            return field
    return None


def select_button_with_text(
    buttons, text="", type=None, in_div=False
):  # in_div=True searches the divs inside buttons
    # Iterate over the buttons
    for button in buttons:
        if (
            in_div == False
            and button.get_attribute("type").lower() == type
            and button.text.lower() == text
        ):
            return button

        if in_div == False and button.text.lower() == text.lower():
            return button

        elif in_div == True:
            try:
                # Find the div element inside the button
                divs = button.find_elements(By.XPATH, ".//div")
                for div in divs:
                    # Check if the text inside the div is 'Log in'
                    if div.text.lower() == text.lower():
                        return button
            except Exception:
                continue
    return None  # if given button not found


def select_button_with_svg(buttons, xmlns=""):
    # Iterate over the buttons and select the one with the desired span and SVG
    for button in buttons:
        span_elements = button.find_elements(By.TAG_NAME, "span")
        for span in span_elements:
            try:
                svg = span.find_element(By.CSS_SELECTOR, f'svg[xmlns="{xmlns}"]')
                return button
            except Exception:
                continue
