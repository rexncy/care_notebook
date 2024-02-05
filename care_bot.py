# Login and download AED and Account data csv
from splinter import Browser
import os
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from care_data_utils import rename_file_if_exists

from file_utils import back_dir, download_wait
from care_navigator import (
    login,
    isLoggedIn,
    download_aed_file,
    download_account_file,
    download_unapproved_aed_file,
    scrape_unapproved_aed_ids,
    download_outstanding_aed,
    logout,
    append_to_field_value,
)

from app_logger import get_logger
import logging

logger = get_logger(__name__, logging.DEBUG, True, True)

today = datetime.today().strftime("%Y%m%d")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TODAY_DIR = os.path.join(DATA_DIR, today)

if not os.path.exists(TODAY_DIR):
    os.makedirs(TODAY_DIR)
else:
    back_dir(TODAY_DIR)


logger.info(f"TODAY_DIR: {TODAY_DIR}")

# Setting a download directory and disable the promting for downloads via the prefs
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": TODAY_DIR,
    "download.directory_upgrade": "true",
    "download.prompt_for_download": "false",
    "disable-popup-blocking": "true",
}

options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")


# when the page needs more time to wait
EXTENDED_TIMEOUT = 90

with Browser(
    "chrome",
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    options=options,
    service=ChromeService(ChromeDriverManager().install()),
) as b:
    b = login(b)

    if isLoggedIn(b):
        try:
            logger.info("Login successful.")

            # process aed approval preparation
            # Find all tr elements that contain img with src="img/icon-offer_0.png"
            logger.info("Scraping unapproved AED IDs...")
            arr_aed_id = scrape_unapproved_aed_ids(b)

            for aed_id in arr_aed_id:
                logger.debug(f"Processing AED = {aed_id}")

                # visit get the edit link
                b.visit(f"https://es.hkfsd.gov.hk/care/cms/en/aed/main/edit/{aed_id}/")
                # get the assigned Serial number

                # fill serial_no as aed_id
                serial_no_field = b.find_by_id("serial_no")
                if not serial_no_field.value or len(serial_no_field.value) == 0:
                    logger.debug(f"Fill serial_no: {aed_id}")
                    b.find_by_id("serial_no").fill(aed_id)

                    # see whether yellow-dot.png exists, if not, remark warning

                    if "yellow-dot.png" in b.html:
                        logger.debug(f"Yellow-dot.png exists for {aed_id}")
                    else:
                        logger.info(f"未完成地圖設定: {aed_id}")
                        append_to_field_value(b, "remark_3", "未完成地圖設定")

                    # The following code does not work in headless mode, despite wait_time is supplied for the element to show
                    # it appears to be a driver bug
                    # click save button
                    # b.find_by_id('btn-save').last.click()

                    # workaround: use js to submit the form
                    b.execute_script("$('form:first').submit();")
                else:
                    logger.debug(f"AED = {aed_id} already processed.")

            logger.info(f"Downloading unapproved AED file...")
            b = download_unapproved_aed_file(b)
            download_wait(TODAY_DIR, EXTENDED_TIMEOUT)
            rename_file_if_exists(TODAY_DIR, "AED.xlsx", "AED_unapproved.xlsx")

            logger.info(f"Downloading AED files...")
            b = download_aed_file(b)
            download_wait(TODAY_DIR, EXTENDED_TIMEOUT)

            logger.info(f"Downloading account files...")
            b = download_account_file(b)
            download_wait(TODAY_DIR, EXTENDED_TIMEOUT)

            logger.info(f"Downloading outstanding AED files...")
            b = download_outstanding_aed(b)
            download_wait(TODAY_DIR, EXTENDED_TIMEOUT)

            logout(b)
            logger.info("Logout successful.")
        except:
            logger.exception("Exception occurred.")
    else:
        logger.info("Login failure.")
