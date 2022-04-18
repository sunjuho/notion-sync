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
            page_id = item['id']

            insert_task = {}

            title = item['properties']['Todo']['title'][0]['text']['content']
            if title:
                insert_task["title"] = title
                print("타이틀 : " + title)

            if item['properties']['완료']['checkbox']:
                status = "completed"
            else:
                status = "needsAction"
            insert_task["status"] = status
            print("완료 : " + status)

            if item['properties']['일자']['date']:
                due = item['properties']['일자']['date']['start'] + "T00:00:00.000Z"
                insert_task["due"] = due
                print("일자 : " + due)

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
