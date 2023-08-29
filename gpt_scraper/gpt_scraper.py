from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium import webdriver
from fake_useragent import UserAgent
import utils
import time
from webdriver_manager.chrome import ChromeDriverManager # *** for Chrome v.116 ***


class ChatGPT:
    def __init__(self, hidden=False):
        self.__openai_url = r"https://chat.openai.com/auth/login"
        self.__openai_login_credentials = {"email": None, "password": None}
        self.__queries_div_idx = 0
        self._clear_chats = True
        self._headless_mode = hidden
        self.__logged_in = False
        self.__timeout = 10
        self.__driver = self._set_driver()

    @property
    def _clear_chats(self):
        return self.__clear_chats

    @_clear_chats.setter
    def _clear_chats(self, setVal):
        if not isinstance(setVal, bool):
            raise TypeError("argument 'clear_chats' must be of type 'bool'")
        self.__clear_chats = setVal

    @property
    def _headless_mode(self):
        return self.__headless_mode

    @_headless_mode.setter
    def _headless_mode(
        self, setVal
    ):  # must be set at the time of instance initialization
        if not isinstance(setVal, bool):
            raise TypeError("argument 'hidden' must be of type 'bool'")
        self.__headless_mode = setVal

    def logged_in(self):
        return self.__logged_in

    # closes the uc driver
    def logout(self, clear_chats=True):
        self._clear_chats = clear_chats
        if self.__logged_in is False:
            raise IllegalLogoutError("User is not logged in")
        error = ""
        if self._clear_chats is True:
            try:
                self._clear_all_conversations()
            except TimeoutError as e:
                error = e
        self.__logged_in = False
        # clear cookies
        self.__driver.delete_all_cookies()
        # self.__driver.close() gives ConnectionLost Error somehow (Library Issues)
        self.__driver.quit()
        if error != "":
            raise TimeoutError(error)

    def change_openai_url(self, new_url):
        self.__openai_url = new_url

    # sets undetected chromedriver
    def _set_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={UserAgent.random}")

        # below gives error for 'options' paramater, works for 'chrome_options'
        if self._headless_mode == False:  # for visible mode
            options.add_argument("user-data-dir=./")
            options.add_experimental_option("detach", True)
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            return uc.Chrome(driver_executable_path=ChromeDriverManager().install(), chrome_options=options)

        # headless mode
        options.add_argument("--headless=new")  # for hidden mode
        return uc.Chrome(
            options=options, version_main=116, driver_executable_path=ChromeDriverManager().install()
        )  # change version_main to your chromedriver version

    def set_credentials(self, email, password):
        if not isinstance(email, str) or not isinstance(password, str):
            raise TypeError("credentials must be of type 'str'")
        if email.strip() == "" or password.strip() == "":
            raise ValueError("credentials can't be empty")
        self.__openai_login_credentials["email"] = email
        self.__openai_login_credentials["password"] = password

    # logins at openai_url
    def login(self):
        timeout = self.__timeout

        # check user credentials
        if any(value is None for value in self.__openai_login_credentials.values()):
            raise RuntimeError("Unable to log in. Credentials are not set")

        # goes to openai_url
        try:
            self.__driver.get(self.__openai_url)
            assert "ChatGPT" in self.__driver.title  # verifies the url
        except Exception:
            raise TimeoutError(
                "Wrong url"
            )  # gives selenium.common.exceptions.WebDriverException either for ERR_NAME_NOT_RESOLVED (when URL is incorrect) or ERR_INTERNET_DISCONNECTED (when not connected to internet)

        # clicks on Login button
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                buttons = self.__driver.find_elements(By.TAG_NAME, "button")
                login_button = utils.select_button_with_text(
                    buttons, text="log in", in_div=True
                )
                if login_button == None:
                    continue

                login_button.click()
                clicked = True
                break

            except Exception:
                continue
        if not clicked:
            raise TimeoutError("Log in button was not found")

        # puts email
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                input_fields = self.__driver.find_elements(By.TAG_NAME, "input")
                mail_input = utils.select_input_field(
                    input_fields, inputmode="email", id="username", name="username"
                )
                if mail_input == None:
                    continue

                mail_input.clear()
                mail_input.click()

                mail_input.send_keys(self.__openai_login_credentials["email"])
                clicked = True
                break

            except Exception:  # ElementNotInteractableException:
                continue
        if not clicked:
            raise TimeoutError("Email input area was not found")

        # clicks on Continue button
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            buttons = self.__driver.find_elements(By.TAG_NAME, "button")
            continue_button = utils.select_button_with_text(
                buttons, text="continue", type="submit"
            )
            if continue_button == None:
                continue

            continue_button.click()
            clicked = True
            break

        if not clicked:
            raise TimeoutError("Continue button was not found")

        time.sleep(0.5)
        # checks incase the email was invalid
        spans = self.__driver.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.text == "Email is not valid.":
                raise InvalidCredentialsError("Invalid email")

        # puts password
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                input_fields = self.__driver.find_elements(By.TAG_NAME, "input")
                password_input = utils.select_input_field(
                    input_fields, id="password", name="password"
                )
                if password_input == None:
                    continue

                password_input.clear()
                password_input.click()

                password_input.send_keys(self.__openai_login_credentials["password"])
                clicked = True
                break

            except Exception:  # ElementNotInteractableException:
                continue
        if not clicked:
            raise TimeoutError("Password input area was not found")

        # clicks on Continue button
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            buttons = self.__driver.find_elements(By.TAG_NAME, "button")
            continue_button = utils.select_button_with_text(
                buttons, text="continue", type="submit"
            )
            if continue_button == None:
                continue

            continue_button.click()
            clicked = True
            break

        if not clicked:
            raise TimeoutError("Continue button was not found")

        time.sleep(0.5)
        # checks incase the password was incorrect
        spans = self.__driver.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.text == "Wrong email or password":
                raise InvalidCredentialsError("Incorrect password")

        # clear popups
        self._clear_popups()
        # flag
        self.__logged_in = True


    # clears popups that come up after login
    def _clear_popups(self):
        timeout = (
            self.__timeout + 10
        )  # additional 10 seconds because sometimes popups load slowly

        # clears popup 1 - 'Next' and popup 2 - also 'Next'
        clicked = False
        start_time = time.time()
        text=r"Okay, let’s go"

        while time.time() - start_time < timeout:
            try:
                buttons = self.__driver.find_elements(By.TAG_NAME, "button")
                button = utils.select_button_with_text(
                    buttons, text=text.lower(), in_div=True
                )
                if button == None:
                    continue

                button.click()
                clicked = True
                break

            except Exception:
                continue
        if not clicked:
            raise TimeoutError(f"Pop-up '{text}' button was not found")

    # inputs a query to ChatGPT
    def query(self, prompt):
        timeout = self.__timeout

        # check login status
        if self.__logged_in == False:
            raise IllegalQueryError("Login before sending a query")

        # clean the prompt a bit
        prompt = prompt.replace("\n", " ").strip()
        if prompt == "":
            raise InvalidPromptError("Prompt was empty")

        # enters prompt in the text area (don't use send_keys, it is slow and prompts can be large sometimes)
        clicked = False
        start_time = time.time()

        while (
            time.time() - start_time < timeout + 10
        ):  # max limit to enter a prompt is 20 sec
            try:
                elements = self.__driver.find_elements(By.TAG_NAME, "textarea")
                prompt_area = utils.select_input_field(
                    elements, id="prompt-textarea", tag_name="textarea"
                )
                if prompt_area == None:
                    continue

                prompt_area.clear()
                prompt_area.click()

                self.__driver.execute_script(
                    "arguments[0].value = arguments[1]", prompt_area, prompt
                )
                # dont' know how the line below works, but apparently it dispacthes any event listeners (without it javascript can't enter text)
                self.__driver.execute_script(
                    'arguments[0].dispatchEvent(new Event("input", { bubbles: true }));',
                    prompt_area,
                )
                clicked = True
                break

            except Exception:
                continue
        if not clicked:
            raise TimeoutError("Prompt area was not found")

        # clicks on the Send button
        send_button = None
        clicked = False
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                elements = self.__driver.find_elements(
                    By.XPATH,
                    '//button[contains(@class, "absolute p-1 rounded-md md:bottom-3 md:p-2 md:right-3 dark:hover:bg-gray-900 dark:disabled:hover:bg-transparent right-2 disabled:text-gray-400 enabled:bg-brand-purple text-white bottom-1.5 transition-colors disabled:opacity-40")][@style="background-color: rgb(25, 195, 125);"]',
                )
                # finds send button using an svg inside it
                send_button = utils.select_button_with_svg(
                    elements, xmlns=r"http://www.w3.org/2000/svg"
                )
                if send_button == None:
                    continue

                send_button.click()
                clicked = True
                break

            except Exception:
                continue
        if not clicked:
            raise TimeoutError("Send button was not found")

        # this check whether ChatGPT has finished writing a reply
        # by leveraging the fact that the send button is disabled while the reply is still being written
        try:
            # sending text to prompt_area makes the send button green again
            prompt_area.send_keys("  ")
            while True:
                # when ChatGPT is still writing the reply
                # * the code below has another use                                                                  *
                # * Sometimes when the prompt is too big, ChatGPT gives prompt-too-long error                       *
                # * Now we can catch it by utilizing the fact that whenever such an excpetion occurs                *
                # * the prompt-area and the send-button become disabled. So when we try to access them below,       *
                # * a StaleElementReferenceException will ocuur, which we can catch in the try-except block outside *
                if not send_button.is_enabled() and prompt_area.is_enabled():
                    continue

                buttons = self.__driver.find_elements(By.TAG_NAME, "button")
                continue_generating_button = utils.select_button_with_text(
                    buttons, text="continue generating", in_div=True
                )

                # when ChatGPT has finished replying
                if send_button.is_enabled and continue_generating_button == None:
                    break

                # when continue-generating button appears
                elif send_button.is_enabled and continue_generating_button is not None:
                    continue_generating_button.click()
                    continue

        except Exception as e:
            # two-three exceptions occur here, can read divs/text to see the what exactly went wrong
            error_messages = {
                "You've reached our limit of messages per hour. Please try again later.": HourlyLimitReachedError,
                "An error occurred. Either the engine you requested does not exist or there was another issue processing your request. If this issue persists please contact us through our help center at help.openai.com.": NetworkError,
                "network error": NetworkError,
                "The message you submitted was too long, please reload the conversation and submit something shorter.": PromptTooLongError,
                "Only one message at a time. Please allow any other responses to complete before sending another message, or wait one minute.": MultiplePromptsError,
            }
            divs = self.__driver.find_elements(By.TAG_NAME, "div")
            for div in divs:
                if div.text in error_messages:
                    raise error_messages[div.text](div.text)
            # incase some other exception occurred
            self.__driver.save_screenshot("screenshot_prompt-reply_unknown_error.png")
            raise RuntimeError(e)

        # query response
        response = ""

        # we use i and self.__queries_div_idx to keep track of where we left off from previous response
        i = self.__queries_div_idx

        # gets the response from the chat area
        clicked = False
        start_time = time.time()

        while (
            time.time() - start_time < timeout + 10
        ):  # max time limit to collect the response is 20 sec
            try:
                divs = self.__driver.find_elements(
                    By.CSS_SELECTOR, "div.group.w-full"
                )  # all divs in the chat area have class "group w-full"
                for j in range(i, len(divs)):
                    if j % 2 != 0:  # select the response divs (odd ones)
                        response += divs[j].text
                clicked = True
                break
            except Exception:  # StaleElementReferenceException:
                continue
        response = response.strip()
        # if no response
        if not clicked or response == "":
            raise TimeoutError("ChatGPT took too much time to respond")
        self.__queries_div_idx = j + 1

        # return the query response
        return response

    # clears all previous conversations shows in the sidebar
    def _clear_all_conversations(self):
        timeout = self.__timeout

        # clicks on namebar
        try:
            elements = self.__driver.find_elements(By.TAG_NAME, "button")
            # namebar is the bottom-most element of the left hand sidebar , which shows user-email
            nameBar_btn = utils.select_button_with_text(
                elements, text=self.__openai_login_credentials["email"], in_div=True
            )
            if nameBar_btn == None:
                raise TimeoutError

            nameBar_btn.click()
        except Exception:
            raise TimeoutError("Namebar was not found")

        # fins <nav> where clear settings are located
        nav = self.__driver.find_element(By.CSS_SELECTOR, 'nav[role="none"]')

        # clicks on settings button
        elements = nav.find_elements(By.TAG_NAME, "a")
        for element in elements:
            if element.text == "Settings":
                clicked = False
                start_time = time.time()
                while time.time() - start_time < timeout:
                    try:
                        element.click()
                        clicked = True
                        break
                    except Exception:
                        time.sleep(0.5)
                        continue
                if not clicked:
                    raise TimeoutError("Settings button was not found")
                else:
                    break

        # find the settings div
        try:
            thediv = self.__driver.find_element(By.CSS_SELECTOR, "div.absolute.inset-0")
        except Exception:
            raise TimeoutError("Settings div not found")

        # click on clear button
        error = "Clear button was not found while clearing chats"
        try:
            clear_button = thediv.find_element(
                By.CSS_SELECTOR, "button.btn.relative.btn-danger"
            )
            time.sleep(0.1)
            if (
                not clear_button.is_enabled()
            ):  # clear button is disabled when no previous chats found
                error = "No chat history found"
                raise TimeoutError
            clear_button.click()
        except Exception:
            raise TimeoutError(error)

        # find the settings div again (coz it refreshes)
        try:
            thediv = self.__driver.find_element(By.CSS_SELECTOR, "div.absolute.inset-0")
        except Exception:
            raise TimeoutError("Settings div not found")

        # click on Confirm deletion button
        buttons = thediv.find_elements(By.TAG_NAME, "button")
        confirm_button = utils.select_button_with_text(buttons, "Confirm deletion")
        if confirm_button == None:
            raise TimeoutError("Confirm deletion button was not found")

        confirm_button.click()


class IllegalLogoutError(RuntimeError):
    pass


class IllegalQueryError(RuntimeError):
    pass


class InvalidCredentialsError(RuntimeError):
    pass


class PromptTooLongError(RuntimeError):
    pass


class HourlyLimitReachedError(RuntimeError):
    pass


class NetworkError(RuntimeError):
    pass


class MultiplePromptsError(RuntimeError):
    pass


class InvalidPromptError(RuntimeError):
    pass
