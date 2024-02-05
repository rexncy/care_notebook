from splinter import Browser
from app_logger import get_logger
import os
import logging

logger = get_logger(__name__, logging.DEBUG, True, True)


def login(b):
    login_page = "https://es.hkfsd.gov.hk/care/cms/en"
    username = "admin"
    password = os.environ.get("PASSWORD")

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
    return b.is_element_present_by_text("Logout") or b.is_element_present_by_value(
        "Logout"
    )


def download_unapproved_aed_file(b):
    b.visit(
        "https://es.hkfsd.gov.hk/care/cms/en/aed/export/?_sort=id&_order=desc&approved=0"
    )
    return b


def download_aed_file(b):
    # download AED export file via direct link
    b.visit("https://es.hkfsd.gov.hk/care/cms/en/aed/export/?_sort=id&_order=desc")
    return b


def download_account_file(b):
    # download Account export file via direct link
    b.visit("https://es.hkfsd.gov.hk/care/cms/en/account/export/?_sort=id&_order=desc")
    return b


def download_outstanding_aed(b):
    # download Account export file via direct link
    b.visit(
        "https://es.hkfsd.gov.hk/care/cms/en/outstanding/export/?status=0&_sort=id&_order=desc"
    )
    return b


def append_to_field_value(b, field_name, field_value):
    field = b.find_by_name(field_name)

    if not field:
        return None

    original_value = field.value
    if original_value:
        field_value = original_value + "\n" + field_value
    else:
        field.fill(field_value)
    return field


def scrape_unapproved_aed_ids(b):
    page = 1
    arr_aed_id = []
    while True:
        b.visit(
            f"https://es.hkfsd.gov.hk/care/cms/en/aed/main/?_sort=id&_order=desc&page={page}"
        )
        tr_elements = b.find_by_xpath('//tr[.//img[@src="img/icon-offer_0.png"]]')
        found = False
        for tr in tr_elements:
            all_text = tr.text
            contain_sn = "Serial No.:" in all_text
            data_id = tr["data-id"]
            if not contain_sn:
                logger.info(f"Found unprocessed AED: {data_id = }")
                arr_aed_id.append(data_id)
                found = True
            else:
                logger.debug(f"AED already processed: {data_id = }")
        if not found:
            break
        else:
            page += 1

    return arr_aed_id


def logout(b):
    b.visit("https://es.hkfsd.gov.hk/care/cms/en/logout/main/")
    return b
