import os
import time
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def InitWebDriver():
    chrome_driver_path = "./chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.executable_path = chrome_driver_path
    #    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def GetEmail():
    ret = os.environ.get("FANTIA_EMAIL_ADDR")
    if ret is None:
        print(f"FANTIA_EMAIL_ADDR is not defined.")
        ret = None
    return ret

def GetPassword():
    ret = os.environ.get("FANTIA_PASSWORD")
    if ret is None:
        print(f"FANTIA_PASSWORD is not defined.")
        ret = None
    return ret

def LogIn(driver, email, password):
    user_email_input = driver.find_element(By.ID, "user_email")
    user_email_input.send_keys(email)
    user_password_input = driver.find_element(By.ID, "user_password")
    user_password_input.send_keys(password)
    login_button = driver.find_element(
        By.CLASS_NAME, "btn.btn-primary.btn-block.mb-10.p-15"
    )
    login_button.click()
    time.sleep(2)
    return


def _getLinks(driver, selector_word):
    anchor_elements = driver.find_elements(By.CSS_SELECTOR, selector_word)
    ret_link_list = []
    for anchor in anchor_elements:
        href = anchor.get_attribute("href")
        print("Href:", href)
        ret_link_list.append(href)
    if len(ret_link_list) > 0:
        return ret_link_list
    else:
        return None


def GetDownloadLinks(driver):
    return _getLinks(driver, "a.link-block")


def GetNextPageLinks(driver):
    return _getLinks(driver, "a.page-link")


def GenNextPageLinks():
    base_uri = "https://fantia.jp/fanclubs/xxx/posts?page="
    ret_uri = []
    # for ii in range(1, 50):
    for ii in range(1, 60):
        ret_uri.append("{0}{1}".format(base_uri, ii))
    return ret_uri


def DownloadFile(driver):
    try:
        file_link = driver.find_element(
            By.CSS_SELECTOR, "a.btn.btn-success.btn-very-lg[download]"
        )
        if file_link is not None:
            file_link.click()
            time.sleep(2.5)
    except Exception as e:
        print(e)
    # for link in file_links:
    #    href = link.get_attribute("href")
    #    print("Href:", href)


def main():

    email = GetEmail()
    password = GetPassword()
    if email is None or password is None:
        exit()

    current_page = 1
    driver = InitWebDriver()
    driver.get("https://fantia.jp/sessions/signin")
    LogIn(driver)
    driver.get("https://fantia.jp/fanclubs/322/posts")
    time.sleep(1.5)

    page_completed = {}

    # pg_links = GetNextPageLinks(driver)
    pg_links = GenNextPageLinks()
    if pg_links is None:
        print("次ページのリンク取得に失敗しました")
        exit(0)
    # pg_links.insert(0, driver.current_url)

    for page_uri in pg_links:
        if page_uri is None:
            continue

        if page_uri in page_completed:
            break
        page_completed[page_uri] = 1

        driver.get(page_uri)
        time.sleep(1.5)

        dl_links = GetDownloadLinks(driver)
        if dl_links is None:
            print("公開ページのリンク取得に失敗しました")
            continue

        for target_uri in dl_links:
            driver.get(target_uri)
            time.sleep(2)
            DownloadFile(driver)
            driver.back()
            time.sleep(1)
    # screenshot_path = "screenshot.png"
    # driver.save_screenshot(screenshot_path)
    driver.quit()


if __name__ == "__main__":
    main()
