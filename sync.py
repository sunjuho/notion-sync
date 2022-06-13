import notion
import googletask
import json


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
    insert_task['status'] = status
    print("완료 : " + status)

    due = ""
    if page['properties']['일자']['date']:
        due = page['properties']['일자']['date']['start'] + "T00:00:00.000Z"
    insert_task["due"] = due
    print("일자 : " + due)

    return insert_task


# google task로부터 page에 넣을 형태로 변환
def get_page_from_task(page, task):
    title = task['title']
    todo = {
        "title": [{
            "text": {
                "content": title
            }
        }]
    }
    page['properties']['Todo'] = todo
    print("타이틀 : " + title)

    status = False
    if task['status'] == "completed":
        status = True
    status_value = {
        "checkbox": status
    }
    page['properties']['완료'] = status_value
    print("완료 : " + task['status'])

    if 'due' in task:
        due = task['due'][:10]
        due_value = {
            "date": {
                "start": due,
                "end": None
            }
        }
        page['properties']['일자'] = due_value
        print("일자 : " + due)

    return page


def get_insert_page_from_task(notion_account, task):
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

    return get_page_from_task(insert_page, task)


def get_update_page_from_task(task):
    update_page = {
        "properties": {}
    }

    return get_page_from_task(update_page, task)


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
    insert_page = get_insert_page_from_task(notion_account, task)

    page = notion.create_page(notion_account, insert_page)

    notion_page_id = page['id']

    return notion_page_id


def update_last_synced_time(base_time):
    f = open('keys/base_time.txt', 'w')
    f.write(base_time)
    f.close()


# 켜질 때 최초 동작. 읽고, past_pages 생성. 이후 이 past_pages로 트리거 동작.
def init_read_notion(notion_account, task_account):
    pages = notion.select_pages(notion_account)

    if pages:
        for page in pages:
            notion_page_id = page['id']

            # 연동
            if page['properties']['google task id']['rich_text']:
                google_task_id = page['properties']['google task id']['rich_text'][0]['text']['content']

            # 미연동
            else:
                print("################################################################ 노션 > 태스크 생성")
                google_task_id = create_task_from_page(notion_account, task_account, page)
                task_account['PAST_TASKS'][google_task_id] = notion_page_id

            notion_account['PAST_PAGES'][notion_page_id] = google_task_id


def init_read_task(notion_account, task_account):
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
                print("################################################################ 태스크 > 노션 생성")
                notion_page_id = create_page_from_task(notion_account, task)
                notion_account['PAST_PAGES'][notion_page_id] = google_task_id

            task_account['PAST_TASKS'][google_task_id] = notion_page_id


# 주기적 싱크 동작
def sync_from_notion_to_task(notion_account, task_account, base_time):
    notion_account['NOW_PAGES'] = {}
    pages = notion.select_pages(notion_account)

    if pages:
        for page in pages:
            notion_page_id = page['id']

            # 연동
            if page['properties']['google task id']['rich_text']:
                google_task_id = page['properties']['google task id']['rich_text'][0]['text']['content']

                if page['last_edited_time'] > base_time:
                    task_object = get_task_from_page(page)
                    task = googletask.select_task(task_account, google_task_id)

                    if task_object['title'] != task['title'] or task_object['status'] != task['status'] or task_object['due'] != task['due']:
                        if page['last_edited_time'] > task['updated']:
                            print("################################################################ 노션 > 태스크 수정")
                            googletask.patch_task(task_account, google_task_id, task_object)

                if notion_page_id in notion_account['PAST_PAGES'].keys():
                    notion_account['PAST_PAGES'].pop(notion_page_id)
            # 미연동
            else:
                isDeleted = False
                for past_task_value in task_account['PAST_TASKS'].values():
                    if past_task_value == notion_page_id:
                        isDeleted = True

                if isDeleted:
                    continue

                print("################################################################ 노션 > 태스크 생성")
                google_task_id = create_task_from_page(notion_account, task_account, page)
                task_account['PAST_TASKS'][google_task_id] = notion_page_id

            notion_account['NOW_PAGES'][notion_page_id] = google_task_id

    if len(notion_account['PAST_PAGES']) > 0:
        for past_notion_page_id in notion_account['PAST_PAGES'].keys():

            page = notion.select_page(notion_account, past_notion_page_id)
            # 노션에서 삭제된 경우 page['archived']
            if page['archived']:
                print("################################################################ 노션 > 태스크 삭제")
                past_google_task_id = notion_account['PAST_PAGES'][past_notion_page_id]
                googletask.delete_task(task_account, past_google_task_id)
                if past_google_task_id in task_account['PAST_TASKS'].keys():
                    task_account['PAST_TASKS'].pop(past_google_task_id)

    notion_account['PAST_PAGES'] = notion_account['NOW_PAGES']
    notion_account['NOW_PAGES'] = {}


# 주기적 싱크 동작
def sync_from_task_to_notion(notion_account, task_account, base_time):
    task_account['NOW_TASKS'] = {}
    tasks = googletask.select_tasks(task_account)
    if tasks:
        for task in tasks:
            google_task_id = task['id']
            page = notion.select_page_by_google_task_id(notion_account, google_task_id)
            if 'due' not in task.keys():
                task['due'] = ""

            # 연동
            if page:
                notion_page_id = page['id']

                if task['updated'] > base_time:
                    task_object = get_task_from_page(page)

                    if task_object['title'] != task['title'] or task_object['status'] != task['status'] or task_object['due'] != task['due']:
                        if task['updated'] > page['last_edited_time']:
                            # task를 notion_properties로 바꿔서 수정.
                            print("################################################################ 태스크 > 노션 수정")
                            notion_properties = get_update_page_from_task(task)
                            notion.update_page_properties(notion_account, notion_page_id, notion_properties)

                if google_task_id in task_account['PAST_TASKS'].keys():
                    task_account['PAST_TASKS'].pop(google_task_id)
            # 미연동
            else:
                isDeleted = False
                for past_page_value in notion_account['PAST_PAGES'].values():
                    if past_page_value == google_task_id:
                        isDeleted = True

                if isDeleted:
                    continue

                # 태스크로 노션 생성
                print("################################################################ 태스크 > 노션 생성")
                notion_page_id = create_page_from_task(notion_account, task)
                notion_account['PAST_PAGES'][notion_page_id] = google_task_id

            task_account['NOW_TASKS'][google_task_id] = notion_page_id

    if len(task_account['PAST_TASKS']) > 0:
        for past_google_task_id in task_account['PAST_TASKS'].keys():

            task = googletask.select_task(task_account, past_google_task_id)
            # 태스크에서 삭제된 경우 task['deleted']
            if 'deleted' in task or task is None:
                print("################################################################ 태스크 > 노션 삭제")
                past_page_id = notion.select_page_by_google_task_id(notion_account, past_google_task_id)['id']
                notion.delete_page(notion_account, past_page_id)
                if past_page_id in notion_account['PAST_PAGES'].keys():
                    notion_account['PAST_PAGES'].pop(past_page_id)

    task_account['PAST_TASKS'] = task_account['NOW_TASKS']
    task_account['NOW_TASKS'] = {}


def init_read(notion_account, task_account):
    notion_account['PAST_PAGES'] = {}
    task_account['PAST_TASKS'] = {}

    init_read_notion(notion_account, task_account)
    init_read_task(notion_account, task_account)


def syncronize(notion_account, task_account, base_time):
    sync_from_notion_to_task(notion_account, task_account, base_time)
    sync_from_task_to_notion(notion_account, task_account, base_time)
