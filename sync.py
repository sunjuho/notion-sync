import notion
import task


# notion에서 읽어서 google task id가 없는, google task 동기화가 안 된 것 찾아서
# task insert
# update notion google task id
def create_task_from_notion(notion_account, task_account):
    items = notion.select_page_not_synced(notion_account)

    if items is not None:
        for item in items:
            print(item)

            title = item['properties']['Todo']['title'][0]['text']['content']
            print("타이틀 : " + title)

            if item['properties']['완료']['checkbox']:
                status = "completed"
            else:
                status = "needsAction"
            print("완료 : " + status)

            due = item['properties']['일자']['date']['start'] + "T00:00:00.000Z"
            print("일자 : " + due)

            insert_task = {
                "title": title,
                "status": status,
                "due": due
            }
            google_task_id = task.create_task(task_account, insert_task)
            print(google_task_id)


create_task_from_notion(notion.PUBLIC, task.PUBLIC)
