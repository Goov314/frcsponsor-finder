import streamlit as st
import requests
import datetime
import pandas as pd

token = st.secrets['TOKEN']

from itertools import chain
from collections import Counter

def group_by_sponsor(sponsor_list):
    flat_list = chain.from_iterable(sponsor_list)
    return dict(Counter(flat_list))


st.title("FRC Sponsor Finder")

year = datetime.datetime.now().year
district = st.text_input("District Code: ")
sponsors = []

if district:
    for currentyear in [str(year), str(year-1)]:
        for page in ["1", "2", "3"]:
            url = f"https://frc-api.firstinspires.org/v3.0/{year}/teams?districtCode={district}&page={page}"
            payload={}
            headers = {
            'Authorization': token,
            'If-Modified-Since': ''
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            teams = response.json()
            for team in teams["teams"]:
                sponsors.append(team["nameFull"].replace("&", "/").split("/"))

    sponsor_dict = group_by_sponsor(sponsors)
    sponsor_df = pd.DataFrame({
        "Sponsor": sponsor_dict.keys(),
        "Count": sponsor_dict.values()
    })

    st.dataframe(sponsor_df.sort_values(by=["Count"], ascending=False, ignore_index=True))

