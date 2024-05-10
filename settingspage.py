import streamlit as st
import psycopg2
from dbConnector import connect
from imageUploader import UploadedImage
import io
from PIL import Image
import pandas as pd


def uimage(userid):
    uploaded_file = st.file_uploader("Upload your profile picture", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        person = connect()
        person.uploadprofileimage(userid, uploaded_file)


def showdoctors(userid):
    person = connect()
    df = person.showdoctors_()
    st.dataframe(df)

    dname = st.text_input('enter Doctor name to follow')
    if st.button('follow'):
        person.followdoctor_(userid, dname)


def settingmain(uid):
    uimage(uid)
    showdoctors(uid)
