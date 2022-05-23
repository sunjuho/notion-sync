import datetime

import notion
import googletask
import sync

# pip install schedule
import schedule
import time

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

    f = open('base_time.txt', 'r')
    last_synced_time = f.readline()
    f.close()

    base_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=15)).isoformat("T") + "Z"

    base_time = base_time if base_time < last_synced_time else last_synced_time

    print("now : " + datetime.datetime.utcnow().isoformat() + ", base_time : " + base_time)

    sync.syncronize(notion.PERSONAL, googletask.PERSONAL, base_time)
    sync.syncronize(notion.PUBLIC, googletask.PUBLIC, base_time)
    # sync.update_keys_file()
    sync.update_last_synced_time(datetime.datetime.utcnow().isoformat())


main_init()
main_sync()
schedule.every(10).minutes.do(main_sync)

while True:
    schedule.run_pending()
    time.sleep(1)
