from splinter import Browser
from loguru import logger
import os

def login(b):
    login_page = "https://es.hkfsd.gov.hk/care/cms/en"
    username = "admin"
    password = os.environ.get('PASSWORD')

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

    return b

def isLoggedIn(b):
    return b.is_element_present_by_text('Logout') or b.is_element_present_by_value('Logout')

def download_aed_file(b):
    # download AED export file via direct link
    b.visit("https://es.hkfsd.gov.hk/care/cms/en/aed/export/?_sort=id&_order=desc")
    return b

def download_account_file(b):
    # download Account export file via direct link
    b.visit(
        "https://es.hkfsd.gov.hk/care/cms/en/account/export/?_sort=id&_order=desc"
    )
    return b

def scrape_unapproved_aed_ids(b):
    b.visit('https://es.hkfsd.gov.hk/care/cms/en/aed/main/')
    tr_elements = b.find_by_xpath(
        '//tr[.//img[@src="img/icon-offer_0.png"]]')
    arr_aed_id = []
    for tr in tr_elements:
        arr_aed_id.append(tr['data-id'])

    return arr_aed_id


def logout(b):
    b.visit("https://es.hkfsd.gov.hk/care/cms/en/logout/main/")
    return b