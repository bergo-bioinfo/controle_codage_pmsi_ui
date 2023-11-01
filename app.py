#!/usr/bin/env python
# coding: utf-8


"""
Web interface for controle_codage_pmsi.
"""


import os
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import subprocess
import sys
import yaml
from yaml.loader import SafeLoader


__author__ = "Yec'han Laizet"
__version__ = "0.1.0"


KEYWORDS_PATH = "tmp_keywords.xlsx"
RESULT_PATH = f"{os.path.splitext(KEYWORDS_PATH)[0]}_output.xlsx"


st.set_page_config(layout='wide', page_title="Consore codage PMSI")


################################################################################
#                          User credentials and auth                           #
################################################################################

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

if authentication_status:
    st.sidebar.write(f'Welcome *{name}*')
    authenticator.logout('Logout', 'sidebar')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# Stop here if auth failed for any reason
if not authentication_status:
    st.stop()


################################################################################
#                                      UI                                      #
################################################################################


st.title('Aide au codage PMSI via Consore')

col1, col2 = st.columns(2)

uploaded_file = col1.file_uploader("Charger un fichier keywords xlsx")

with open("/app/consore-services/tests/tests_controle_codage/referentiels/keywords.xlsx", "rb") as f:
    col1.download_button(
        label="Télécharger le fichier keyword exemple",
        data=f,
        file_name='keywords.xlsx',
        mime='application/vnd.openxmlformatsofficedocument.spreadsheetml.sheet',
    )

if uploaded_file is not None:
    kw = pd.read_excel(uploaded_file)
    with open(KEYWORDS_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    col1.write("Fichier chargé")
    col1.dataframe(kw)

datedeb = col2.date_input(
    "Date de début",
    "today",
    format="DD/MM/YYYY"
)

datefin = col2.date_input(
    "Date de fin",
    "today",
    format="DD/MM/YYYY"
)


# Dates checks
disable_search = False
delta = datefin - datedeb
if delta > 365:
    col2.error("La durée entre la date de début et la dte de fin ne peut pas excéder 1 an!")
    disable_search = True
if datedeb > datefin:
    col2.error("La date de fin doit être postérieure à la date de début!")
    disable_search = True

# Search Consore
if col2.button("Recherche Consore", type="primary", disabled=disable_search):
    with col2.status("Recherche en cours...", expanded=True) as status:
        st.write("Interrogation Consore...")
        subprocess.run([f"{sys.executable}", "/app/consore_services/controle_codage_pmsi/main.py", 
        "--consore", "consore.json", "--inputkeywords", f"/app/controle_codage_pmsi_ui/{KEYWORDS_PATH}",
        "--datedeb", datedeb.strftime("%Y-%m-%d"), "--datefin", datefin.strftime("%Y-%m-%d")])
        status.update(label="Recherche terminée", state="complete", expanded=False)
        with open(KEYWORDS_PATH, "rb") as f:
            col2.download_button(
                label="Télécharger le fichier de résultats",
                data=f,
                file_name=RESULT_PATH,
                mime='application/vnd.openxmlformatsofficedocument.spreadsheetml.sheet',
            )
        st.dataframe(pd.read_excel(RESULT_PATH))
