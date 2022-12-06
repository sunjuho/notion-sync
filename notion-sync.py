import notion
import googletask
import sync

# pip install schedule
import schedule
import time
import datetime


def main_init():
    print('main_init_run')

    sync.init_read(notion.PERSONAL, googletask.PERSONAL)
    sync.init_read(notion.EXERCISE, googletask.EXERCISE)
    sync.init_read(notion.PUBLIC, googletask.PUBLIC)


def main_sync():
    print('main_sync_run')

    f = open('/git/notion-sync/keys/base_time.txt', 'r')
    last_synced_time = f.readline()
    f.close()

    base_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=15)).isoformat("T") + "Z"
    base_time = base_time if base_time < last_synced_time else last_synced_time

    print("now : " + str(datetime.datetime.now()) )

    sync.synchronize(notion.PERSONAL, googletask.PERSONAL, base_time)
    sync.synchronize(notion.EXERCISE, googletask.EXERCISE, base_time)
    sync.synchronize(notion.PUBLIC, googletask.PUBLIC, base_time)
    sync.update_last_synced_time(datetime.datetime.utcnow().isoformat())


main_init()
main_sync()
schedule.every(10).minutes.do(main_sync)
schedule.every(1).hours.do(googletask.refresh_token)

while True:
    schedule.run_pending()
    time.sleep(1)
