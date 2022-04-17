import notion

# todo : 모듈화

page = {
    "parent": {
        "database_id": notion.PERSONAL["DATABASE_ID"]
    },
    "properties": {
        "Todo": {
            "title": [
                {
                    "text": {
                        "content": "구글 태스크 연동"  # todo
                    }
                }
            ]
        },
        "완료": {
            "checkbox": False  # todo
        },
        "일자": {
            "date": {
                "start": "2022-04-17",  # todo
                "end": None
            }
        },
        "google task id": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "",  # todo
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
                    "plain_text": "",  # todo
                    "href": None
                }
            ]
        }
    }
}
'''
    ,
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Lacinato kale"
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "paragraph", # todo 아래와 동일
            "paragraph": { # todo 위와 동일
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm."
                        }
                    }
                ]
            }
        }
    ]
'''

personal_test_db_create_result = notion.create_page(notion.PERSONAL, page)
