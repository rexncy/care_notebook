# -*- coding: utf-8 -*-

import pandas as pd
import os

def assign_serial_number(to_aed_xlsx, will_generate_excel=False):
    if not os.path.exists(to_aed_xlsx):
        return None
    df = pd.read_excel(to_aed_xlsx)
    df["Serial No."] = df["Serial No."].fillna("")

    # rearrange the column for readability
    col = df.pop("Title (En)")
    df.insert(1, "Title (En)", col)

    col2 = df.pop("Master Owner Email")
    df.insert(2, "Master Owner Email", col2)

    # create a dictionary to store the latest serial number for each domain
    latest_serial_nums = {}

    tuples_highlight_yellow = []

    # reversely iterate over each row in the dataframe
    # to make sure old Serial No. get fetched into latest_serial_nums first
    for index, row in df.iloc[::-1].iterrows():
        domain = row["Master Owner Email"].split("@")[
            1
        ]  # extract the domain from the email
        sn = row["Serial No."]
        if len(str(sn)) > 0:
            latest_serial_nums.update({domain: sn})
        else:
            if domain in latest_serial_nums:
                latest_serial_num = latest_serial_nums[domain]
                new_serial_num = latest_serial_num[:3] + str(
                    int(latest_serial_num[3:]) + 1
                ).zfill(
                    3
                )  # increment the serial number
                df.at[index, "Serial No."] = new_serial_num  # update new serial number
                tuples_highlight_yellow.append(index)
                latest_serial_nums.update({domain: new_serial_num})
            else:
                df.at[index, "Serial No."] = ""  # leave the serial number blank


    if will_generate_excel:
        # apply style
        st = df.style.applymap(
            lambda x: "background-color: yellow",
            subset=pd.IndexSlice[tuples_highlight_yellow, ["Serial No."]],
        )
        parent_dir = os.path.dirname(to_aed_xlsx)
        st.to_excel(
            os.path.join(parent_dir, "AED_sn_assigned.xlsx"),
            index=False,
            header=True,
            encoding="utf-8",
            engine="openpyxl",
        )

    return df

# assume from_df is not None
# expect 
def fetch_aed_serial_number(from_df, title, address, location):
    filt_title = (from_df['Title (En)'] == title)
    filt_address = (from_df['Address (En)'] == address)
    filt_location = (from_df['Location (En)'] == location)

    df_filt = from_df[filt_title & filt_address & filt_location]

    sn = df_filt['Serial No.'].iat[0]

    return str(sn)