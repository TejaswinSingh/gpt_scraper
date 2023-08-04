# gpt_scraper

The `gpt_scraper` is a Python script that uses Selenium  to interact with the OpenAI ChatGPT interface. It provides functionality to log in to the ChatGPT platform, send queries to the chatbot, and retrieve responses. It also handles errors on OpenAI's side, such as when the hourly limit for prompts is reached or when the entered prompt is too long, etc. Additionally, if the response is too large and a "Continue generating" button appears, it handles that case as well to obtain the complete response.

## How to Setup

To set up the project and get it running, follow the steps below:

1. **Install Dependencies:** First, run the following command to install the project dependencies using `pip`:

   ```shell
   pip install -r requirements.txt
   ```

2. **Change ChromeDriver Version:**

   Open the `gpt_scraper.py` script and locate the `ChatGPT` class. Inside the class, find the `_set_driver()` instance method. It should look like this:

   ```python
   def _set_driver(self):
       options = webdriver.ChromeOptions()
       options.add_argument(f"user-agent={UserAgent.random}")

       if self._headless_mode == False:  # for visible mode
           options.add_argument("user-data-dir=./")
           options.add_experimental_option("detach", True)
           options.add_experimental_option("excludeSwitches", ["enable-logging"])
           return uc.Chrome(chrome_options=options)

       # headless mode
       options.add_argument("--headless=new")  # for hidden mode
       return uc.Chrome(
           options=options, version_main=114
       )  # change version_main to your chromedriver version
   ```

   In the second-to-last line of the code block above, change the `version_main` parameter to match the version of Chrome (or ChromeDriver) you're using. It's recommended to use the latest version available.

## How to Use
   ```python
   import gpt_scraper
   
   def run():
      # create instance
       chat_instance = gpt_scraper.ChatGPT(
           hidden=True
       )  # give argument 'hidden=True' if you want to open chrome in headless mode. Default in non-headless
       chat_instance.set_credentials("youremail", "youropenaipassword")

      # login
       try:
           chat_instance.login()
       except gpt_scraper.InvalidCredentialsError as e:  # if credentails were invalid
           return
       except (
           TimeoutError
       ):  # if something else goes wrong during login (like if a button was not found after repeated tries)
           return

      # query
       question = 'Hey, how are you?'
       try:
           response = chat_instance.query(question)
           print(f"Response: {response}")
       except (
           TimeoutError
       ):  # if a button or web-element was not found after repeated tries. This exception is also raised by the query() method if ChatGPT gave an empty string ('') as reponse (rare)
           return
       except (
           RuntimeError
       ):  # if something goes wrong while getting the response. See error section below for more help
           return

      # logout
       try:
         if chat_instance.logged_in():
           chat_instance.logout(
               clear_chats=False
           )  # to not clear all chats before logging out. Default is True
       except TimeoutError:  # Exceptions can occur if clear_chats was set to True
           pass
   ```

**Handle Error Cases:** 

   ```
   Error Section: These are some of the common exceptions that I noticed occurring when getting a response. You can catch them specifically, like HourlyLimitReachedError, to try again after some time,
   or PromptTooLongError, to shorten up the prompt a bit. Or you can catch them all as RuntimeError.
   ___________________
       HourlyLimitReachedError: "You've reached our limit of messages per hour. Please try again later."
       NetworkError: "An error occurred. Either the engine you requested does not exist or there was another issue processing your request. If this issue persists, please contact us through our help center at help.openai.com."
       PromptTooLongError: "The message you submitted was too long, please reload the conversation and submit something shorter."
       MultiplePromptsError: "Only one message at a time. Please allow any other responses to complete before sending another message or wait one minute."
   ```

## Invalid Handle Error

If you encounter the following error related to the "undetected_chromedriver" library:

```
Exception ignored in: <function Chrome.__del__ at 0x000001BED7E284A0>
Traceback (most recent call last):
  File "C:\Users\PC\Downloads\mail_bot\.venv\Lib\site-packages\undetected_chromedriver\__init__.py", line 793, in __del__
  File "C:\Users\PC\Downloads\mail_bot\.venv\Lib\site-packages\undetected_chromedriver\__init__.py", line 748, in quit   
OSError: [WinError 6] The handle is invalid
```

You can resolve it by making the following changes to the '__init__.py' file in "undetected_chromedriver" library. If you're using VSCode, follow these steps:

1. Hover over the file name in the error output above. An option "Open file in editor" will appear, click on it.
2. Now the file is opened, go to line number 748:

Python code
```python
...
for _ in range(5):
    try:
        shutil.rmtree(self.user_data_dir, ignore_errors=False)
    except FileNotFoundError:
        pass
    except (RuntimeError, OSError, PermissionError) as e:
        logger.debug(
            "When removing the temp profile, a %s occured: %s\nretrying..."
            % (e.__class__.__name__, e)
        )
    else:
        logger.debug("successfully removed %s" % self.user_data_dir)
        break
    time.sleep(0.1)

# dereference patcher, so patcher can start cleaning up as well.
# this must come last, otherwise it will throw 'in use' errors
self.patcher = None
...
```

3. Comment out the code below by placing a '#' before it, like this -

```python
# time.sleep(0.1)
```

This should resolve the "Invalid Handle Error" issue.
