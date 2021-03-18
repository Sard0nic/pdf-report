from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import sys

# This function loads a site, waits until JavaScript has rendered the whole site and then stores
# the parsed HTML in a list. Then it goes on to the next page as many times as defined and
# repeats this process in the end the list with all parsed sides is returned
def loadHTML_JS_New(url):
    # Setting up Selenium
    # Run Firefox in Headless Mode (Invisible)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # Getting fully loaded HTML (After JS) from selenium
    driver.get(url)
    html = []

    # Draw progress bar
    startProgress('Loading sites')

    #time.sleep(5)
    html.append(driver.execute_script("return document.documentElement.outerHTML"))

    # Value for xpath to find the correct button on the site
    btnvalue = 2
    # Repeats following steps until btnvalue reaches specified limit
    while btnvalue <= 308:
        pct = int(100 / 308 * btnvalue)
        progress(pct)

        # Click Button
        xpath = '//*[@id="submitBtn" and @value="' + str(btnvalue) + '"]'
        button = driver.find_element_by_xpath(xpath)
        button.click()
        btnvalue += 1

        # Get Page Content
        #time.sleep(5)
        html.append(driver.execute_script("return document.documentElement.outerHTML"))

    # End progress bar
    endProgress()

    # Closing Firefox diver
    driver.close()

    return html

# Draw progress bar to shell, call before the loop
def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

# Update progress bar, has to be included in the loop
def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x -progress_x))
    sys.stdout.flush()
    progress_x = x

# Finish progress bar and write next output to new line, call after loop
def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()
