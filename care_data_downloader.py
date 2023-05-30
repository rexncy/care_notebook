# Login and download AED and Account data csv
from splinter import Browser
import logging, os, time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from file_utils import back_dir, download_wait
from care_data_utils import assign_serial_number, fetch_aed_serial_number
from app_logger import get_logger

today = datetime.today().strftime("%Y%m%d")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TODAY_DIR = os.path.join(DATA_DIR, today)

if not os.path.exists(TODAY_DIR):
    os.makedirs(TODAY_DIR)
else:
    back_dir(TODAY_DIR)



logger = get_logger(__name__, logging.INFO, True, True)

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
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");

# when the page needs more time to wait
EXTENDED_TIMEOUT = 15

with Browser(
    "chrome",
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    options=options,
    headless=True,
    service=ChromeService(ChromeDriverManager().install()),
) as b:
    login_page = "https://es.hkfsd.gov.hk/care/cms/en"
    username = "admin"
    password = "Fsd_aed10"

    b.visit(login_page)

    username_field = b.find_by_name("username")
    username_field.fill(username)

    password_field = b.find_by_name("password")
    password_field.fill(password)

    # slide to login
    logger.info("Login attempt...")

    draggable = b.find_by_css(".ui-draggable-handle")
    droppable = b.find_by_css(".ui-droppable")
    draggable.drag_and_drop(droppable)

    if b.is_element_present_by_text('Logout') or b.is_element_present_by_value('Logout'):
        logger.info("Login successful.")

        # download AED export file via direct link
        b.visit("https://es.hkfsd.gov.hk/care/cms/en/aed/export/?_sort=id&_order=desc")
        # download AED export file via direct link
        b.visit(
            "https://es.hkfsd.gov.hk/care/cms/en/account/export/?_sort=id&_order=desc"
        )

        logger.info('Awaiting download to complete...')
        download_wait(TODAY_DIR, 10)
        logger.info('Download completed.')

        # assign serial num to new AEDs
        aed_df = assign_serial_number(os.path.join(TODAY_DIR, 'AED.xlsx'), True)
        logger.info(f'df_aed: {aed_df.shape[0]}')

        # process aed approval preparation 
        # Find all tr elements that contain img with src="img/icon-offer_0.png"
        b.visit('https://es.hkfsd.gov.hk/care/cms/en/aed/main/')
        tr_elements = b.find_by_xpath('//tr[.//img[@src="img/icon-offer_0.png"]]')
        arr_aed_id = []
        for tr in tr_elements:
            arr_aed_id.append(tr['data-id'])

        for aed_id in arr_aed_id:
            logger.info(f"Processing AED = {aed_id}")

            # visit get the edit link
            b.visit(f'https://es.hkfsd.gov.hk/care/cms/en/aed/main/edit/{aed_id}/')
            # get the assigned Serial number

            title_field = b.find_by_id('title_1')
            address_field = b.find_by_id('address_1')
            location_field = b.find_by_id('location_1')

            sn = fetch_aed_serial_number(aed_df, title_field.value, address_field.value, location_field.value)
            # fill the assigned Serial number
            if( sn and len(sn) > 0):
                logger.info(f'Existing participant: filling sn for aed_id: { aed_id }; sn: {sn}')
                b.find_by_id('serial_no').fill(sn)
            else:
                b.find_by_id('serial_no').fill('')
                logger.info(f'New participant: aed_id: { aed_id }')

            # click save button
            b.find_by_id('btn-save').first.click()

        b.visit("https://es.hkfsd.gov.hk/care/cms/en/logout/main/")
        logger.info("Logout successful.")
    else:
        logger.info("Login failure.")
