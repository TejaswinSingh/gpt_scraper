# gpt_scraper

The `gpt_scraper` is a Python script that uses Selenium and a Chrome WebDriver to interact with the OpenAI ChatGPT interface. It provides functionality to log in to the ChatGPT platform, send queries to the chatbot, and retrieve responses. The script handles login and query part.

## How to Setup

To set up the project and get it running, follow the steps below:

1. **Install Dependencies:** First, run the following command to install the project dependencies using `pip`:

   ```shell
   pip install -r requirements.txt
   ```

2. **Download ChromeDriver:**

   - Determine the version of Google Chrome installed on your system. You can find this information by opening Chrome and going to `chrome://version/`. Look for the "Google Chrome" field to find the version number.

   - Visit the [ChromeDriver download page](https://sites.google.com/chromium.org/driver/?pli=1).

   - Download the version of ChromeDriver that matches your Chrome browser version. Make sure to choose the appropriate version for your operating system.

   - Extract the downloaded ChromeDriver executable from the archive file (if it's zipped).

   - Move the ChromeDriver executable file to the same folder where your `gpt_scraper.py` script is located.

   Your folder structure should look like this:

   ```
   - gpt_scraper.py
   - utils.py
   - chromedriver (executable file)
   ```

3. **Configure ChromeDriver Version:**

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

   In the second-to-last line of the code block above, change the `version_main` parameter to match the version of ChromeDriver (or Chrome) you're using. It's recommended to use the latest version available.

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
