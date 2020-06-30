## USER APP

- User Model을 확장해야 함.
  - Document를 자주 참고할것..
  - setting.py 에서 AUTH_USER_MODEL = "myapp.MyModel" 이런식으로 추가해줘야 한다.
  - 베이스로 주어진 models.Model을 이용하지 않고, admin 화면에 나오는 유저 정보들이 필요하므로, django.contrib.auth.models 에서 AbstractUser를 베이스로 사용한다.
  - 먼저 setting.py에서 만들어진 앱을 추가해야 한다.
    - ex) users.apps.UserConfig (UserConfig는 apps.에 정의되어 있다.)
- 모델이 변경었으므로 python manage.py makemigrations, python manage.py migrate 명령어를 입력 해줘야 한다.

- admin 페이지에 가면 user 모델이 없어진 것을 확인할 수 있는데, custom 모델이라 그럼. 수동으로 admin에 연결해주면 된다.

  - Documentation의 admin site 참고해야 한다.
  - admin.py에 가서.
  - models.py import를 하고 ..
  - @admin.register (models.User)로 등록을 하고 ..
    - 이제 기억 났는데 이건 decorator라 불린다.
    - 마지막에 추가 작업이었던가..?
    - @admin.register (models.User)는 클래스 밑에
    - admin.site.register (models.User, CustomUserAdmin)을 한 효과이다.
  - class CustomUserAdmin(admin.ModelAdmin): 을 작성한다.
    - ModelAdmin.list_display: 리스트에서 어떤 필드를 표시할지..튜플 타입.
    - list_filter(fields): 리스트에서 필터를 표시해준다.

- user admin class 는 꼭 django.contrib.admin.ModelAdmin만 상속 받을 수 있는 것은 아니다.

  - django.contrib.auth.admin.UserModel이라는 클래스에서도 상속 받을 수 있다.
  - 이 경우에는 ModelAdmin과는 다르게 우리가 custom으로 추가한 field들을 모른다.
  - 그래서 fieldset을 추가해줘야 한다.
    - fieldset을 만드는 방법은 admin.py 코드를 참고.
    - 기존의 fieldsets와 합칠 수도 있다. 코드를 참고.
    - 기존의 fieldsets와 합칠 때에는 중복되는 field 있는지 확인 해야 한다.

- Model에 필드를 추가하는 방법.

  - Document를 일단 참고해야 함.
  - field를 만들 때 default값을 줘야함.
    - 빈 필드를 허용하려면 null=True를 넘겨주면 된다.
      - null을 허용한다고 해서 그 필드가 빈 필드가 된다는 것은 아니다.
      - 빈필드를 만들고 싶다면, blank=True 옵션을 줘야 한다.
    - CharField, TextField 차이: Single line or multiline 차이
      - CharField는 combobox로 만들 수 있는 방법이 있다. User model의 gender 필드 참고.
      - choices 옵션 이용, 튜플로 데이터 전달.
    - DateField는 두 종류가 있다.
      - DateField
      - DateTimeField
      - DateField는 blank가 될 수가 없다. null=True를 같이 넣어주자.
  - CF) class 를 만들 때 """ explaination """ 을 넣어두면 VSC에서 다이렉트로 실시간 설명을 볼 수 있다.

## TimeStampedModel에 대해...

- review, room, conversation 등 모두 만들어진 시간과 업데이트된 시간이 있기 때문에... 클래스 이용.
- 그래서 django-admin startapp core를 통해 core 앱을 만든 거지만...
- 우리는 core 앱의 model이 db에 등록되는 것을 원하지 않기 때문에...
- 안에 Meta라는 클래스를 만들어준다.
- class Meta: abtract = True를 이용하여 주는데, 추상적 모델이지 실제 db에는 반영되지 않음.
  - 위의 User model이 AbstractUser 모델을 상속 받는데, AbstractUser 모델은 db에 실제 등록되는 것이 아니다.
  - 그래서 이름을 **AbstractTimeStamped**로 내가 변경을 했다.

## ROOMS APP

- country filed : 모든 국가를 어떻게 입력해?? django countries 라는 라이브러리가 있음!
  - package import rules
    - python lib. -> django lib. -> third party lib. 순으로 import
  - **1:n - foreign key 지정 방법**.
    - Models.ForeignKey를 이용하면 된다.
      - on_delete = models.CASCADE, delete시 행동
      - documentation 참고, (CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET, DO_NOTHING)
      - ForeignKey를 지정할 때 string으로 해도 된다.
        - ex) ForeinKey(User) -> ForeignKey("User") 라고 해도 된다.
          - 다만 다른 앱의 모델을 지정할 때에는 모델까지 지정해줘야 한다.
          - Room에서 User를 참고할 때 "users.User" 라고 해줘야 한다.
      - forien key의 데이터 접속은 아주 쉽다. 그냥 클래스 쓰듯 하면 된다.
        - ex) user.name
  - n:n - Models.ManyToManyField
  - **str** method
    - db model 대표값을 리턴해준다.
- room 관련하여 여러가지 data model을 만들었는데...
  - AbstractTimeStampled 상속 받고,
  - AbstractItem class를 만들었는데, abstract라는 이름에 주목하도록...
  - Admin site에 등록할 때, 예를 들면, amenitys라고 admin site에 표시되는데...
    - 이는 class Meta에서 이름을 바꿀 수 있다.
      - Documentation을 참고하도록..
      - verbose_name_plural에서 복수형 설정할 수 있다.
      - ordering = ['-order_data']: order_data에는 order할 field 사용.
        - '-'가 들어가면 역순 정렬.
