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
def get_headers(parameter):
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
    headers = get_headers(account)
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
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages/" + page_id

    response = requests.request("GET", url, headers=headers)
    json_object = json.loads(response.text)
    item = json_object
    print(item)
    return item


# Retrieve block children
# usage example: notion.select_page_contents(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
def select_page_contents(account, page_id):
    headers = get_headers(account)
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
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages"
    # json to text
    page = json.dumps(page)

    response = requests.request("POST", url, headers=headers, data=page)
    json_object = json.loads(response.text)
    item = json_object
    print(item)
    return item


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

    response = requests.request("POST", url, headers=headers, json=search_filter)
    json_object = json.loads(response.text)
    item = json_object["results"][0]
    print(item)
    return item


# usage example: notion.select_page_not_synced(notion.PUBLIC)
def select_page_not_synced(account):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/databases/" + account["DATABASE_ID"] + "/query"

    search_filter = {
        "filter": {
            "property": "google task id",
            "rich_text": {
                "is_empty": True
            }
        }
    }

    response = requests.request("POST", url, headers=headers, json=search_filter)
    json_object = json.loads(response.text)

    items = json_object["results"]
    if items is not None:
        for item in items:
            print(item)
    return items


# update notion page.
# usage example: notion.update_page_properties(notion_account, page_id, notion_properties)
def update_page_properties(account, page_id, properties):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/pages/" + page_id

    response = requests.request("PATCH", url, headers=headers, json=properties)
    json_object = json.loads(response.text)

    item = json_object
    if item is not None:
        print(item)
    return item


# 특정 시간 이후로(optional), 최근 편집순 정렬 조회.
# usage example: notion.select_page_edited(notion.PUBLIC, last_synced_date='2022-04-18T11:43:00.000Z')
def select_page_edited(account, last_synced_date=None):
    headers = get_headers(account)
    url = "https://api.notion.com/v1/databases/" + account["DATABASE_ID"] + "/query"

    search_filter = {
        "sorts": [
            {
                "timestamp": "last_edited_time",
                "direction": "descending"
            }
        ]
    }

    # 최근 동기화 성공 일시가 있으면 성공 일시 기준 이후 조회
    if last_synced_date:
        search_filter["filter"] = {
            "timestamp": "last_edited_time",
            "last_edited_time": {
                "after": last_synced_date
            }
        }

    response = requests.request("POST", url, headers=headers, json=search_filter)
    json_object = json.loads(response.text)

    items = json_object["results"]
    if items is not None:
        for item in items:
            print(item)
    return items


def get_task_id_from_page(page):
    return page['properties']['google task id']['rich_text'][0]['text']['content']
