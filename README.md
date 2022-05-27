# notion-sync

노션과 구글 태스크 동기화를 위한 프로젝트

### History

평소, 개인적인 할 일은 핸드폰과 연동되는 구글 태스크로, 업무에 사용하는 할 일은 노션으로 관리하고 있었습니다.

어느 날, 업무를 하면서 생기고 처리한 일들을 구글 태스크를 통해서도 뿌듯하게 보고 싶다는 마음이 들었습니다.

노션과 태스크를 연동하는 게 있겠지 싶어서 찾아봤지만, 자동화 사이트에선 유료 기능을 사용해야 하고, 그마저도 제대로 동작하지 않는 상황이 발생하여 직접 기능을 만들기로 하여 이 프로젝트를 시작하게 되었습니다.

<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white"/><img src="https://img.shields.io/badge/Pycharm-000000?logo=pycharm&logoColor=white"/><img src="https://img.shields.io/badge/Google Task-4285F4.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXcgMCAwIDE5MiAxOTIiIGhlaWdodD0iMTZweCIgdmlld0JveD0iMCAwIDE5MiAxOTIiIHdpZHRoPSIxNnB4Ij48cmVjdCBmaWxsPSJub25lIiBoZWlnaHQ9IjE5MiIgd2lkdGg9IjE5MiIvPjxnPjxnPjxwb2x5Z29uIGZpbGw9IiNGRkZGRkYiIHBvaW50cz0iMTQ3LjM0LDM0LjY2IDEzNCw0MiAxMjcuNDIsNTQuNTggMTM0LDcwIDE0Ni40OCw4My41MiAxNjAsNzYgMTY4LjI5LDYxLjcxIDE2MCw0NCIvPjxwYXRoIGQ9Ik05NS43OCw4Ni4yMmwzMS42NC0zMS42NGM5LjMyLDcuMDgsMTYuMTcsMTcuMjMsMTkuMDYsMjguOTRsLTQzLjQxLDQzLjQxYy0zLjkxLDMuOTEtMTAuMjQsMy45MS0xNC4xNCwwIEw1OS42Niw5Ny42NmMtMy4xMi0zLjEyLTMuMTItOC4xOSwwLTExLjMxbDEyLjQ3LTEyLjQ3YzMuMTItMy4xMiw4LjE5LTMuMTIsMTEuMzEsMEw5NS43OCw4Ni4yMnogTTE4Mi4zNCwzNi4zNGwtMTIuNjktMTIuNjkgYy0zLjEyLTMuMTItOC4xOS0zLjEyLTExLjMxLDBsLTExLDExYzguNzksNy4zNiwxNS45NywxNi41OCwyMC45NSwyNy4wNWwxNC4wNS0xNC4wNUMxODUuNDcsNDQuNTMsMTg1LjQ3LDM5LjQ3LDE4Mi4zNCwzNi4zNHogTTE0OCw5NmMwLDI4LjcyLTIzLjI4LDUyLTUyLDUycy01Mi0yMy4yOC01Mi01MnMyMy4yOC01Miw1Mi01MmMxMS44MSwwLDIyLjY5LDMuOTQsMzEuNDIsMTAuNThsMTkuOTItMTkuOTIgQzEzMy40NSwyMy4wMiwxMTUuNTUsMTYsOTYsMTZjLTQ0LjE4LDAtODAsMzUuODItODAsODBjMCw0NC4xOCwzNS44Miw4MCw4MCw4MHM4MC0zNS44Miw4MC04MGMwLTEyLjI3LTIuNzctMjMuOS03LjcxLTM0LjI5IGwtMjEuODEsMjEuODFDMTQ3LjQ3LDg3LjUyLDE0OCw5MS43LDE0OCw5NnoiIGZpbGw9IiNGRkZGRkYiLz48L2c+PC9nPjwvc3ZnPg=="/><img src="https://img.shields.io/badge/Notion-000000?logo=notion&logoColor=white"/>

<img src="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/aa506466-3f81-4656-8c8b-960204e07c93/Untitled.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220527%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220527T161534Z&X-Amz-Expires=86400&X-Amz-Signature=855e9895e81e3cf401eb7d7a40dad410f6da692bf3e7e6b5bd5fdb2ac3d89860&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.jpeg%22&x-id=GetObject"/>
