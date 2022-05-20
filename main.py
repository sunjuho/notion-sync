import datetime

import notion
import googletask
import sync

import time
# pip install schedule
import schedule


# def syncronize_creation():
#     sync.create_task_from_notion(notion.PUBLIC, googletask.PUBLIC)
#     sync.create_task_from_notion(notion.PERSONAL, googletask.PERSONAL)
#
#     notion.PUBLIC = sync.update_task_from_notion(notion.PUBLIC, googletask.PUBLIC)
#     notion.PERSONAL = sync.update_task_from_notion(notion.PERSONAL, googletask.PERSONAL)
#
#     sync.update_notion_keys_file()


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
    sync.init_read(notion.PERSONAL, googletask.PERSONAL)
    sync.init_read(notion.PUBLIC, googletask.PUBLIC)


def main_sync():
    print('main_sync_run')
    search_time = ( datetime.datetime.utcnow() - datetime.timedelta(minutes=5) ).isoformat("T") + "Z"
    print(search_time)
    sync.syncronize(notion.PERSONAL, googletask.PERSONAL, search_time)
    sync.syncronize(notion.PUBLIC, googletask.PUBLIC, search_time)
    sync.update_keys_file()


main_init()
main_sync()
schedule.every(5).minutes.do(main_sync)
#'''
while True:
    schedule.run_pending()
    time.sleep(1)
#'''

# notion.PERSONAL
