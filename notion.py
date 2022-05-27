import requests
import json
import time

# 공통
NOTION_VERSION = "2022-02-22"

# account info
with open('keys/notion_keys.json') as json_file:
    data = json.load(json_file)

    PERSONAL = data['PERSONAL']
    PUBLIC = data['PUBLIC']


# initialize headers info
def get_headers(parameter):
    headers = {
        "Accept": "application/json",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "Authorization": parameter["BEARER_TOKEN"]
    }
    return headers


# usage example: notion.select_pages(notion.PERSONAL)
def select_pages(account):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/databases/" + account["DATABASE_ID"] + "/query"

    while True:
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    items = json_object["results"]
    return items


# usage example: notion.create_page(notion.PERSONAL, page)
def create_page(account, page):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages"

    while True:
        response = requests.request("POST", url, headers=headers, json=page)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    item = json_object
    return item


# usage example: notion.select_page(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
def select_page(account, notion_page_id):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages/" + notion_page_id

    response = requests.request("GET", url, headers=headers)
    json_object = json.loads(response.text)
    item = json_object
    # print(item)
    return item


# todo
# usage example: notion.select_page_contents(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
def select_page_contents(account, notion_page_id):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/blocks/" + notion_page_id + "/children"

    while True:
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    items = json_object["results"]
    for item in items:
        print(item)
    return items


# usage example: notion.select_page_by_google_task_id(notion.PUBLIC, "dHRVYWtGUXFhckZuMjk3ZQ")
def select_page_by_google_task_id(account, task_id):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/databases/" + account["DATABASE_ID"] + "/query"

    search_filter = {
        "filter": {
            "property": "google task id",
            "rich_text": {
                "equals": task_id
            }
        }
    }

    while True:
        response = requests.request("POST", url, headers=headers, json=search_filter)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    if json_object["results"]:
        item = json_object["results"][0]
        return item
    else:
        return None


# usage example: notion.update_page_properties(notion_account, notion_page_id, notion_properties)
def update_page_properties(account, notion_page_id, properties):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages/" + notion_page_id

    while True:
        response = requests.request("PATCH", url, headers=headers, json=properties)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    item = json_object
    return item


def delete_page(account, notion_page_id):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/blocks/" + notion_page_id

    while True:
        response = requests.request("DELETE", url, headers=headers)
        if response.status_code == 200:
            break
        time.sleep(0.5)

    json_object = json.loads(response.text)
    item = json_object
    return item
