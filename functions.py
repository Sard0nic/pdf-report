from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import sys

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

    btnvalue = 2
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

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x -progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()