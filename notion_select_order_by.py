import notion
import sync

notion.select_page_edited(notion.PUBLIC, last_synced_time=sync.last_synced_time)
