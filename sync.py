import notion
import googletask
import json
import datetime


# notion page로부터 task에 넣을 형태로 변환
def get_task_from_page(page):
    insert_task = {}

    title = ""
    if page['properties']['Todo']['title']:
        title = page['properties']['Todo']['title'][0]['text']['content']

    insert_task["title"] = title
    print("타이틀 : " + title)

    if page['properties']['완료']['checkbox']:
        status = "completed"
    else:
        status = "needsAction"
    insert_task["status"] = status
    print("완료 : " + status)

    due = ""
    if page['properties']['일자']['date']:
        due = page['properties']['일자']['date']['start'] + "T00:00:00.000Z"
    insert_task["due"] = due
    print("일자 : " + due)

    return insert_task


def get_page_from_task(notion_account, task):
    insert_page = {
        "parent": {
            "database_id": notion_account["DATABASE_ID"]
        },
        "properties": {
            "google task id": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": task['id']
                    }
                }]
            }
        }
    }

    title = task['title']
    todo = {
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ]
    }
    insert_page['properties']['Todo'] = todo
    print("타이틀 : " + title)

    if task['status'] == "needsAction":
        status = False
    elif task['status'] == "completed":
        status = True
    완료 = {
        "checkbox": status
    }
    insert_page['properties']['완료'] = 완료
    print("완료 : " + task['status'])

    if 'due' in task:
        due = task['due'][:10]
        일자 = {
            "date": {
                "start": due,
                "end": None
            }
        }
        insert_page['properties']['일자'] = 일자
        print("일자 : " + due)

    return insert_page


# notion에서 읽어서 google task id가 없는, google task 동기화가 안 된 것 찾아서
# task insert
# update notion google task id
def create_task_from_notion(notion_account, task_account):
    items = notion.select_page_not_synced(notion_account)

    if len(items):
        for item in items:
            print(item)
            notion_page_id = item['id']

            insert_task = get_task_from_page(item)
            """
            insert_task = {
                "title": title,
                "status": status,
                "due": due
            }
            """

            google_task_id = googletask.create_task(task_account, insert_task)
            print(google_task_id)

            notion_properties = {
                "properties": {
                    "google task id": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": google_task_id
                            }
                        }]
                    }
                }
            }

            notion.update_page_properties(notion_account, notion_page_id, notion_properties)


# 노션 값으로 태스크 수정. 이후 노션 정보에 최근 수정 정보 최신화.
def update_task_from_notion(notion_account, task_account):
    print("동기화 동작 기준 시간 : " + notion_account['LAST_SYNCED_TIME'])
    pages = notion.select_page_edited(notion_account, last_synced_time=notion_account['LAST_SYNCED_TIME'])

    if len(pages):
        updated = ""
        for page in pages:
            if page['properties']['google task id']['rich_text']:
                update_task = get_task_from_page(page)

                google_task_id = notion.get_task_id_from_page(page)
                updated = googletask.patch_task(task_account, google_task_id, update_task)

        # 동기화 성공 시간 기록
        print("last_synced_time : " + updated)
        notion_account['LAST_SYNCED_TIME'] = updated

    # togo : pages 가 없더라도 동기화에 성공한 건 맞음.

    return notion_account


# notion_keys파일에 마지막 동기화 시간 수정
def update_notion_keys_file():
    json_object_personal = {}
    json_object_personal['BEARER_TOKEN'] = notion.PERSONAL['BEARER_TOKEN']
    json_object_personal['DATABASE_ID'] = notion.PERSONAL['DATABASE_ID']
    json_object_personal['LAST_SYNCED_TIME'] = notion.PERSONAL['LAST_SYNCED_TIME']

    json_object_public = {}
    json_object_public['BEARER_TOKEN'] = notion.PUBLIC['BEARER_TOKEN']
    json_object_public['DATABASE_ID'] = notion.PUBLIC['DATABASE_ID']
    json_object_public['LAST_SYNCED_TIME'] = notion.PUBLIC['LAST_SYNCED_TIME']

    json_object = {'PERSONAL': json_object_personal, 'PUBLIC': json_object_public}
    file = open('keys/notion_keys.json', 'w')
    json.dump(json_object, file)
    file.close()


# 켜질 때 최초 동작. 읽고, past_pages 생성. 이후 이 past_pages로 트리거 동작.
def init_read_notion(notion_account, task_account):
    notion_account['PAST_PAGES'] = {}
    pages = notion.select_pages(notion_account)

    if pages:
        for page in pages:
            notion_page_id = page['id']

            # 연동
            if page['properties']['google task id']['rich_text']:
                google_task_id = page['properties']['google task id']['rich_text'][0]['text']['content']

            # 미연동
            else:
                google_task_id = create_task_from_page(notion_account, task_account, page)

            notion_account['PAST_PAGES'][notion_page_id] = google_task_id


# 주기적 싱크 동작
def sync_from_notion_to_task(notion_account, task_account, search_time):
    notion_account['NOW_PAGES'] = {}
    pages = notion.select_pages(notion_account)

    if pages:
        for page in pages:
            notion_page_id = page['id']

            # 연동
            if page['properties']['google task id']['rich_text']:
                google_task_id = page['properties']['google task id']['rich_text'][0]['text']['content']

                if page['last_edited_time'] > notion_account['LAST_SYNCED_TIME']:
                    update_task = get_task_from_page(page)

                    synced_task = googletask.select_task(task_account, google_task_id)

                    if update_task['title'] != synced_task['title'] or update_task['status'] != synced_task['status'] or update_task['due'] != synced_task['due']:
                        googletask.patch_task(task_account, google_task_id, update_task)

                notion_account['PAST_PAGES'].pop(notion_page_id)
            # 미연동
            else:
                google_task_id = create_task_from_page(notion_account, task_account, page)

            notion_account['NOW_PAGES'][notion_page_id] = google_task_id

    if len(notion_account['PAST_PAGES']) > 0:
        for past_notion_page_id in notion_account['PAST_PAGES'].keys():

            page = notion.select_page(notion_account, past_notion_page_id)
            # 노션에서 삭제된 경우 page['archived']
            if page['archived']:
                past_google_task_id = notion_account['PAST_PAGES'][past_notion_page_id]
                googletask.delete_task(task_account, past_google_task_id)

    notion_account['LAST_SYNCED_TIME'] = search_time
    notion_account['PAST_PAGES'] = notion_account['NOW_PAGES']
    notion_account['NOW_PAGES'] = {}


def create_task_from_page(notion_account, task_account, page):
    notion_page_id = page['id']
    insert_task = get_task_from_page(page)

    google_task_id = googletask.create_task(task_account, insert_task)

    notion_properties = {
        "properties": {
            "google task id": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": google_task_id
                    }
                }]
            }
        }
    }

    notion.update_page_properties(notion_account, notion_page_id, notion_properties)

    return google_task_id


def create_page_from_task(notion_account, task):
    insert_page = get_page_from_task(notion_account, task)

    page = notion.create_page(notion_account, insert_page)

    notion_page_id = page['id']

    notion_account['PAST_PAGES'][notion_page_id] = task['id']

    return notion_page_id


def init_read_task(notion_account, task_account):
    task_account['PAST_TASKS'] = {}
    pages = notion.select_pages(notion_account)
    tasks = googletask.select_tasks(task_account)

    if tasks:
        for task in tasks:
            google_task_id = task['id']
            page = notion.select_page_by_google_task_id(notion_account, google_task_id)

            # 연동
            if page:
                notion_page_id = page['id']

            # 미연동
            else:
                notion_page_id = create_page_from_task(notion_account, task)

            task_account['PAST_TASKS'][google_task_id] = notion_page_id


def init_read(notion_account, task_account):
    init_read_notion(notion_account, task_account)
    init_read_task(notion_account, task_account)


#init_read(notion.PERSONAL, googletask.PERSONAL)
