import notion
import task
import json


# notion page로부터 task에 넣을 형태로 변환
def get_task_from_notion(page):
    insert_task = {}

    title = page['properties']['Todo']['title'][0]['text']['content']
    if title:
        insert_task["title"] = title
        print("타이틀 : " + title)

    if page['properties']['완료']['checkbox']:
        status = "completed"
    else:
        status = "needsAction"
    insert_task["status"] = status
    print("완료 : " + status)

    if page['properties']['일자']['date']:
        due = page['properties']['일자']['date']['start'] + "T00:00:00.000Z"
        insert_task["due"] = due
        print("일자 : " + due)

    return insert_task


# notion에서 읽어서 google task id가 없는, google task 동기화가 안 된 것 찾아서
# task insert
# update notion google task id
def create_task_from_notion(notion_account, task_account):
    items = notion.select_page_not_synced(notion_account)

    if len(items):
        for item in items:
            print(item)
            page_id = item['id']

            insert_task = get_task_from_notion(item)
            """
            insert_task = {
                "title": title,
                "status": status,
                "due": due
            }
            """

            google_task_id = task.create_task(task_account, insert_task)
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

            notion.update_page_properties(notion_account, page_id, notion_properties)


# 노션 값으로 태스크 수정. 이후 노션 정보에 최근 수정 정보 최신화.
def update_task_from_notion(notion_account, task_account):
    print("동기화 동작 기준 시간 : " + notion_account['LAST_SYNCED_TIME'])
    pages = notion.select_page_edited(notion_account, last_synced_time=notion_account['LAST_SYNCED_TIME'])

    if len(pages):
        updated = ""
        for page in pages:
            if page['properties']['google task id']['rich_text']:
                update_task = get_task_from_notion(page)

                google_task_id = notion.get_task_id_from_page(page)
                updated = task.patch_task(task_account, google_task_id, update_task)

        # 동기화 성공 시간 기록
        print("last_synced_time : " + updated)
        notion_account['LAST_SYNCED_TIME'] = updated

    # togo : pages 가 없더라도 동기화에 성공한 건 맞음.

    return notion_account


# notion_keys파일에 마지막 동기화 시간 수정
def update_notion_keys_file(notion_account_personal, notion_account_public, ):
    json_object = {'PERSONAL': notion_account_personal, 'PUBLIC': notion_account_public}
    file = open('keys/notion_keys.json', 'w')
    json.dump(json_object, file)
    file.close()
