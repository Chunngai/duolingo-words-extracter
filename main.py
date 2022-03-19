import argparse
import os

import openpyxl
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def find_elements(by, value, driver, web_driver_wait):
    web_driver_wait.until(expected_conditions.presence_of_element_located(
        (by, value))
    )
    elements = driver.find_elements(by=by, value=value)
    return (
        elements
        if len(elements) >= 2
        else elements[0]
    )


def main(args: argparse.Namespace):
    lang = args.lang
    sheet_name = args.sheet

    # Ref: https://blog.csdn.net/qq_34253926/article/details/107856859
    options = webdriver.ChromeOptions()
    # W/o it the page will be closed automatically.
    options.add_experimental_option("detach", True)
    # Ref: https://www.baidu.com/s?wd=selenium%20%E6%97%A0%E5%A4%B4%E6%A8%A1%E5%BC%8F%20%E5%85%A8%E5%B1%8F&rsv_spt=1&rsv_iqid=0xd864cea90001b8ef&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_dl=tb&rsv_enter=1&oq=selenium%2520%25E6%2597%25A0%25E5%25A4%25B4%25E6%25A8%25A1%25E5%25BC%258F&rsv_btype=t&inputT=2534&rsv_t=54f576e6OdR8Ax3U%2Fksb2A%2Ft%2FWyNJ2yyYkU5L%2FrlJQM8%2FT%2FhQOnMvoncIfyo4Bifgo0d&rsv_sug3=25&rsv_sug1=16&rsv_sug7=100&rsv_pq=824466cf0002afe2&rsv_sug2=0&rsv_sug4=2787
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')

    # Ref: https://blog.csdn.net/Hacker_xiao/article/details/88907866
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    driver = webdriver.Chrome(options=options, desired_capabilities=capa)
    # driver.maximize_window()
    driver.get("https://www.duolingo.com/")

    web_driver_wait = WebDriverWait(driver, 20)

    with open(".account.config") as f:
        username, password = f.read().splitlines()

    have_account_button = find_elements(
        by=By.CSS_SELECTOR,
        value='._3mSsk',
        driver=driver,
        web_driver_wait=web_driver_wait
    )
    print(f"have_account_button: {have_account_button}")
    have_account_button.click()

    username_input, password_input = find_elements(
        by=By.CSS_SELECTOR,
        value="._3MNft",
        driver=driver,
        web_driver_wait=web_driver_wait
    )
    print(f"username_input: {username_input}")
    print(f"password_input: {password_input}")
    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = find_elements(
        by=By.CSS_SELECTOR,
        value='._2oW4v',
        driver=driver,
        web_driver_wait=web_driver_wait
    )
    print(f"login_button: {login_button}")
    login_button.click()

    # Ref: https://www.cnblogs.com/z-x-y/p/9718204.html
    more = find_elements(
        by=By.CSS_SELECTOR,
        value='._2oFpm',
        driver=driver,
        web_driver_wait=web_driver_wait
    )
    print(f"more: {more}")
    ActionChains(driver).move_to_element(more).perform()

    words_button = find_elements(
        by=By.XPATH,
        value="//a[contains(@href,'/words')]",
        driver=driver,
        web_driver_wait=web_driver_wait
    )
    print(f"words_button: {words_button}")
    words_button.click()

    # Scrolls to end. Ref: https://blog.csdn.net/weixin_33595571/article/details/88673253
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    driver.implicitly_wait(1)
    tbody = find_elements(
        by=By.TAG_NAME,
        value="tbody",
        driver=driver,
        web_driver_wait=web_driver_wait,
    )
    print(f"tbody: {tbody}")

    # Makes html. Ref: https://blog.csdn.net/qq_39451578/article/details/104142215
    html = tbody.get_attribute('innerHTML')
    html = etree.HTML(html)
    html = etree.tostring(html, encoding="utf-8", pretty_print=True, method="html")

    driver.quit()

    # Gets word list.
    soup = BeautifulSoup(html, "html.parser")
    word_list = []
    print("Making word list.")
    for tr in soup.find_all("tr"):
        if lang == "es":
            word_td, pos_td, last_practiced_td, _ = tr.find_all("td")
            pos = pos_td.text
        elif lang == "ru":
            word_td, last_practiced_td, _ = tr.find_all("td")
            pos = ""
        else:
            raise NotImplementedError

        word = word_td.span.text
        last_practiced = last_practiced_td.text

        word_list.append(
            (word, pos, last_practiced)
        )
    print("Word list made.")

    # Writes to duolingo_logs.xlsx.
    print(f"Writing word list to {lang}_logs.xlsx: {sheet_name}.")
    workbook = openpyxl.load_workbook(filename=f"{lang}_logs.xlsx")
    sheet = workbook.create_sheet(title=sheet_name)
    for line in word_list:
        # Ref: https://www.cnblogs.com/sxinfo/p/11723338.html
        sheet.append(line)
    workbook.save(f"{lang}_logs.xlsx")
    print("Word list written.")

    # Finds new words.
    print("Finding new words.")
    # TODO
    python_ = (
        "python3"
        if os.name == "posix"
        else "python"
    )
    os.system(f"{python_} find_new_words.py --lang {lang}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True)
    parser.add_argument("--sheet", required=True)
    args = parser.parse_args()

    # sheet_name = args.__getattribute__("sheet-name")
    # assert sheet_name is not None, "sheet_name not provided."

    main(args)
