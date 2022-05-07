import sync
import notion
import googletask


taskLists = googletask.select_tasks(googletask.PERSONAL) # Qlc5UXlXRWhyVUVjZU8wdQ

page = notion.select_page_by_google_task_id(notion.PERSONAL, 'MmZuMkhvRlBCc0ViREFIZg')
