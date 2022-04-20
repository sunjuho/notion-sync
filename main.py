import notion
import task
import sync

import time
# pip install schedule
import schedule


def syncronize_creation():
    sync.create_task_from_notion(notion.PUBLIC, task.PUBLIC)
    sync.create_task_from_notion(notion.PERSONAL, task.PERSONAL)

    notion.PUBLIC = sync.update_task_from_notion(notion.PUBLIC, task.PUBLIC)
    notion.PERSONAL = sync.update_task_from_notion(notion.PERSONAL, task.PERSONAL)

    sync.update_notion_keys_file(notion.PERSONAL, notion.PUBLIC)


schedule.every(5).minutes.do(syncronize_creation)

while True:
    schedule.run_pending()
    time.sleep(1)
