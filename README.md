# gpt_scraper

The `gpt_scraper` is a Python script that uses Selenium and a Chrome WebDriver to interact with the OpenAI ChatGPT interface. It provides functionality to log in to the ChatGPT platform, send queries to the chatbot, and retrieve responses. The script handles various login and query-related scenarios.

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
