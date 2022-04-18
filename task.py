# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
from __future__ import print_function

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# account info
with open('keys/task_keys.json') as json_file:
    data = json.load(json_file)

    PERSONAL = data['PERSONAL']
    PUBLIC = data['PUBLIC']

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

"""Shows basic usage of the Tasks API.
Prints the title and ID of the first 10 task lists.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('keys/token.json'):
    creds = Credentials.from_authorized_user_file('keys/token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'keys/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('keys/token.json', 'w') as token:
        token.write(creds.to_json())


def select_task_list():
    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the Tasks API
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print('No task lists found.')
            return

        print('Task lists:')
        task_lists = {}
        for item in items:
            print(u'{0} ( {1} )'.format(item['title'], item['id']))
            task_lists[item['title']] = item['id']
        return task_lists

    except HttpError as err:
        print(err)


def select_tasks(task_list):
    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the Tasks API
        results = service.tasks().list(tasklist=task_list).execute()
        items = results.get('items', [])

        if not items:
            print('No tasks found.')
            return

        print('Tasks:')
        tasks = {}
        for item in items:
            print(u'{0} ( {1} )'.format(item['title'], item['id']))
            print(item)
            tasks[item['title']] = item['id']
        return tasks

    except HttpError as err:
        print(err)


def create_task(task_list, task):
    try:
        service = build('tasks', 'v1', credentials=creds)

        result = service.tasks().insert(tasklist=task_list, body=task).execute()
        print(result)
        return result['id']

    except HttpError as err:
        print(err)
