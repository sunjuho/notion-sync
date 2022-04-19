import notion
import task
import sync

import time
# pip install schedule
import schedule


def syncronize_creation():
    sync.create_task_from_notion(notion.PUBLIC, task.PUBLIC)
    sync.create_task_from_notion(notion.PERSONAL, task.PERSONAL)

    sync.update_task_from_notion(notion.PUBLIC, task.PUBLIC)
    sync.update_task_from_notion(notion.PERSONAL, task.PERSONAL)


schedule.every(5).minutes.do(syncronize_creation)

while True:
    schedule.run_pending()
    time.sleep(1)
