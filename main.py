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

    sync.update_notion_keys_file()


'''
schedule.every(5).minutes.do(syncronize_creation)
'''

# 최초 데이터 읽은 read() 실행
"""
syncronize_creation()
while True:
    schedule.run_pending()
    time.sleep(1)
"""


def main_init():
    print('main_init_run')
    sync.init_read_notion(notion.PERSONAL, task.PERSONAL)
    sync.init_read_notion(notion.PUBLIC, task.PUBLIC)


def main_sync():
    print('main_sync_run')
    sync.sync_form_notion_to_task(notion.PERSONAL, task.PERSONAL)
    sync.sync_form_notion_to_task(notion.PUBLIC, task.PUBLIC)
    sync.update_notion_keys_file()


#main_init()
main_sync()
schedule.every(5).minutes.do(main_sync)
#'''
while True:
    schedule.run_pending()
    time.sleep(1)
#'''

# notion.PERSONAL
