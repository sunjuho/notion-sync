import notion

notion.select_pages(notion.PUBLIC)

# contents 있음
notion.select_page(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")
notion.select_page_contents(notion.PUBLIC, "c4e4c3b3-8747-4a93-ba4a-7b148d5ca8dc")

# contents 없음
notion.select_page(notion.PUBLIC, "18ef6a98-57fe-44ef-94f8-835fef33a80d")
notion.select_page_contents(notion.PUBLIC, "18ef6a98-57fe-44ef-94f8-835fef33a80d")
