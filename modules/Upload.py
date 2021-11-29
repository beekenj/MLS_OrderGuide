#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
from googleapiclient.http import MediaFileUpload
from modules.Google import Create_Service


# In[7]:

def drive_upload():

    CLIENT_SECRET_FILE = './.app_info/client_secret.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # replace existing file on gdrive
    file_id = '18Mbt-SJbMpC7R7x1BJiplNBohWh4P3JH'

    media_content = MediaFileUpload('MLS_prices-order.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    service.files().update(
        fileId=file_id,
        media_body=media_content
    ).execute()

