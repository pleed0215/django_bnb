# AirBnb clone project from Nomadcoders.co

## making clone service using python with django, and front & back-end, both will be made by django.

## AirBnB course learning point

### Introduction and env. setup

- [ ] understanding why use pipenv, nico called pipenv bubble.
- [ ] install pacakge via pipenv, "pipenv shell", into the bubble.
- [ ] inside pipenv shell, install django.
- [ ] make github repository, and disploy. making gitingore, searching in web, "gitignore python"

## Introduction django

- [ ] django-admin startproject mysite ...??? Nope. -> use django-admin startproject config
  - 추후 확장문제 때문에 만들어주는 사이트보다, config 이용해서 세팅하는게 더 낫다고 한다.
  - 만들어진 config 폴더를 이름 바꾸고(ex. Aconfig) -> 하위 폴더에 있는 config를 끄집어 낸다. manage.py도 같이 끄집어 내어준다.
  -
- [ ] extension 에서 python 모듈을 설치.
- [ ] linter, fomatter 설치.

  - linter는 flake8을 추천.
  - 자동인스톨이 안되면, pipenv install flake8 --dev
  - fomater 자동 인스톨 안되면, pipenv install black --dev --pre
  - linter를 설치 후 나오는 E501 에러 관련하여, 이 부분은 신경 안써도 된다고 함.
    - setting.json 에서 이렇게 하면 없어진다고 한다. "python.linting.flake8Args": ["--max-line-length=91"]

- [ ] django 파일 구조 설명

  - config/**init**.py : python 에서 필요한 파일. js의 index.js와 비슷?
  - config/setting.py: application 에 필요한 모든 정보가 닮겨있다.
    - TIME_ZONE을 Asia/Seoul로 바꿈.

- CF. ctrl or command 버튼을 누르고 아무거나 누르면 definition으로 이동한다.
- [ ] python manage.py 실행해보기.

  - python manage.py runserver: 서버 구동.
  - python manage.py migrate : db migration.
    - python manage.py makemigrations: migration 파일을 만든다.
      - migration을 만들고 나서 migrate를 하는 과정을 거친다.
  - python manage.py createsuperuser: admin id 만들기.

- [ ] django의 project 구성에 대해 이야기 함.
  - project -> application -> functions
  - 프로젝트를 계획하기 쉽게 한다고 함.
    - ex> room application은 room을 create, search, delete, upload를 할 수 있어야 함.
    - 한 어플리케이션이 너무 커지면 안된다. divide & conquer 방식을 이용.
- [ ] 새로운 어플리케이션 만들기.
  - django-admin startapp [appname]
    - 여기서 만들어 준 파일들은 함부로 이름을 바꾸면 안된다.
  - rooms, users, reveiws, conversations, lists, reservations app 만듬.
  - django rule 대로 사용하여야 한다. django에 의해 생성된 것은 삭제하지 말어.
    - ex) users를 예를 들면..
      - views.py: 어떻게 보여질지.
      - admin.py: admin에서 user가 어떻게 보여질지..
      - models.py: model과 상호. -> migrations에 변경이 저장되고.. migrate해야 한다.
      - app.py: 별로 신경 쓸게 없으미. config파일임.
      - urls.py: 기본적으로 제공은 안되지만, 만들 수 있음. 하부 urls.
