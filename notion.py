import requests
import json

# 공통
NOTION_VERSION = "2022-02-22"
# todo : 사용하는지 확인
payload = {"page_size": 100}

# account info
with open('keys/notion_keys.json') as json_file:
    data = json.load(json_file)

    PERSONAL = data['PERSONAL']
    PUBLIC = data['PUBLIC']
    EXAMPLE_DB = data['EXAMPLE_DB']


# initialize headers info
def getHeaders(parameter):
    headers = {
        "Accept": "application/json",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "Authorization": parameter["BEARER_TOKEN"]
    }
    return headers


# Query a database
# usage example: notion.select_pages(notion.PERSONAL)
def select_pages(account):
    headers = getHeaders(account)
    url = "https://api.notion.com/v1/databases/" + account["DATABASE_ID"] + "/query"

    response = requests.request("POST", url, headers=headers)

    # str to json
    json_object = json.loads(response.text)
    items = json_object["results"]
    for item in items:
        print(item)
    return items


# Retrieve a page
# usage example: notion.select_page(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
def select_page(account, page_id):
    headers = getHeaders(account)
    url = "https://api.notion.com/v1/pages/" + page_id

    response = requests.request("GET", url, headers=headers)
    json_object = json.loads(response.text)
    item = json_object
    print(item)
    return item


# Retrieve block children
# usage example: notion.select_page_contents(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
def select_page_contents(account, page_id):
    headers = getHeaders(account)
    url = "https://api.notion.com/v1/blocks/" + page_id + "/children"

    response = requests.request("GET", url, headers=headers)
    json_object = json.loads(response.text)
    items = json_object["results"]
    for item in items:
        print(item)
    return items


# Create a page with content
# usage example: notion.create_page(notion.PERSONAL, page)
def create_page(account, page):
    headers = getHeaders(account)
    url = "https://api.notion.com/v1/pages"
    # json to text
    page = json.dumps(page)

    response = requests.request("POST", url, headers=headers, data=page)
    json_object = json.loads(response.text)
    item = json_object
    print(item)
    return item
