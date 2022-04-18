import notion

page = {
    "parent": {
        "database_id": notion.EXAMPLE_DB["DATABASE_ID"]  # todo
    },
    "properties": {
        "Type": {
            "select": {
                "id": "f96d0d0a-5564-4a20-ab15-5f040d49759e",
                "name": "Article",  # todo
                "color": "default"
            }
        },
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "Python Test "  # todo
                    }
                }
            ]
        },
        "Status": {
            "select": {
                "id": "8c4a056e-6709-4dd1-ba58-d34d9480855a",
                "name": "Ready to Start",  # todo
                "color": "yellow"
            }
        },
        "Publisher": {
            "select": {
                "id": "01f82d08-aa1f-4884-a4e0-3bc32f909ec4",
                "name": "The Atlantic",  # todo
                "color": "red"
            }
        },
        "Publishing/Release Date": {
            "date": {
                "start": "2020-12-08T12:00:00Z",  # todo
                "end": None
            }
        },
        "Link": {
            "url": "https://www.nytimes.com/2018/10/21/opinion/who-will-teach-silicon-valley-to-be-ethical.html"  # todo
        },
        "Summary": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Some think chief ethics officers could help technology companies navigate political and social questions.",
                        # todo
                        "link": None
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": "Some think chief ethics officers could help technology companies navigate political and social questions.",
                    # todo
                    "href": None
                }
            ]
        },
        "Read": {
            "checkbox": False  # todo
        }
    }
}

# personal_test_db_create_result = notion.create_page(notion.EXAMPLE_DB, page)
notion.select_pages(notion.EXAMPLE_DB)
