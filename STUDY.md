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
        - 여러가지 field들어갈 수 있음.

### Reservation, Review, List, Photo model

- 위에서 한 것들로 전부 커버가 되는 내용이라 딱히 적을 내용은 없다.

## 6. Room Admin

### Admin page 꾸미기

- ModelAdmin page 참고.
- list_display
- list_filter
- search_fields
  - searching text 관련하여 icontains 참고바람..
    - ^: Start with, =: exact, @: search, None: icontains,
    - foreign key 접근 하는 방법
      - ex) host\_\_usrename
- filter_horizontal, filter_vertical
  - ManyToManyFields 에서만 작동.
- 'classes': 'collapse'
  - fieldssets 에 fields와 같이 사용 가능하다.
  - category를 접을 수 있음.
- amenities, facilities 등은 갯수를 보여줘야 할 때도 있는데...
  - list_display의 필드자리에 함수를 추가..
    - ex) , count_amenities
    - def count_amenities (self, obj): ~~~
  - 위의 obj는 QuerySet Object이다...
    - 참고는 당연히 documentation을 해야하고..
  - 이런 함수는 admin에서 뿐만 아니라, models에서는 만들 수 있다.
    - review의 average 얻는 것을 참고.
    - admin page에 함수를 만드는 것과의 차이점은..
      - 전자는 admin에서만 사용, 후자는 여러 페이지에서 사용 가능하다는 점..
  - custom으로 만든 함수가 boolean 타입인데...
    - 그냥 사용하면 list_display에서 True, False식으로 표시되는데.
    - function.boolean = True로 하면.. 아이콘 모양으로 바뀐다.

### Manager & QuerySet

- cf. python shell 을 이용하여 django에 접근하려면..

  - python manage.py shell을 이용하여야 한다.
  - shell 안에서..

    - 이 두가지를 배워야 한다.
    - dir: 현재 정의한 것들의 이름을 반환.
    - vars: attribute를 반환.
    - User를 import 한 후(shell에서 from users.models import User) User.objects를 쳐보면..
      - django.contrib.auth.models.UserManager 라는 오브젝트를 반환.
      - Room은 manager를 반환.
    - Document를 참고하면...
      - data model을 만들면, django가 자동으로 database-abtracion API를 줘서, object를 CRUD 할 수 있게끔 해준다한다.
    - 유용한 method

      - all
      - filter
      - count
      - get
      - QuerySet Object들을 리턴해주는 경우가 있는데..

        - QuerySet에서 .. forein key의 역으로... 이를테면.. 한 유저가 여러개의 방을 가지고 있다고 가정해보자.

          - 그 유저의 QuerySet에서.. room_set 메소드를 활용을 하면.. manager가 만들어지는데..

            - naming rule: '\<modelname\>\_set' 인것을 알 수 있다.
            - **naming을 바꾸려면 foreignkey를 생성할 때, related_name 옵션을 주면 된다.**
            - related_name은 foreignkey 대상을 위한 것이다.
            - set 메소드를 사용하지 않고, 대상을 확인하려면..
              - models.Photo.objects.filter(room\_\_id=obj.id) 이런식으로...
              - 상대 model에서 filter해도 될 것이다.

          - UserQuerySet.room_set을 shell에 입력해 보면 알 수 있다.
            - the result will be 'django.db.models.fileds.related_descriptors.create_reverse_may_to_one_manager'

        - id로 object를 얻는 방법
          - ex) Room.objects.get (id=1)
          - id 대신 pk(Primary Key)를 써도 된다.

## django media

- ImageField로 올린 image들을 보면... 링크로 연결이 안된다.

### MEDIA_ROOT

- config/settings.py에서 MEDIA_ROOT를 설정해줘야 한다.
  - 당연히 documentation 참고 해야하며..
  - absolute root를 가진다.
  - settings.py에 보면 이미 BASE_DIR로 절대 경로를 제공해준다.
  - os.path.join (BASE_DIR, 'uploads')등으로 설정해주면 된다.
- upload된 photo 등을 확인해보면 링크가 있는데, 클릭 해보면 이동하지 않는다.
  - 이상한 url을 나타내며..
  - ex) room/1/photo/change/@@@ 이런식으로..

### MEDIA_URL

- URL that handles the media served from MEDIA_ROOT, used for managing stored files. It must end in a slash if set to a non-empty value. You will need to configure these files to be served in both development and production environments.
- '/'로 끝나야 한다.
- MEDIA_URL을 다룰 때에는 absolute path, relative path를 알아야 한다.
  - django bnb에서는 absolute path로 한다.
  - 이렇게 한다고 해도 바로 연결이 되는 건 아니다.

### URLConfig

- config/urls.py
  - setting을 import해야 하는데..
    - 같은 폴더라고 from . import settings 하면 안된다.
    - from django.conf import settings로 import해야 한다.
- static 제공.
  - from django.conf.urls.static import static.
  - local 파일을 제공하는 것은 좋지 않기 때문에 debug 모드에서만 제공하는 것이 좋다.
  - debug mode. if settings.Debug:

### Media로 다시 돌아가서.. ImageField의 속성 확인.

- 생각보다 많다.
- print 해보면 경로만 나와서 object가 아닌 것으로 착각하는 경우가 많음.
- dir을 해보거나, type(obj)로 확인해보자.
- PhotoAdmin에 get_thumbnail 함수를 만들었는데...
  - return f'\<img src="{obj.image.url}"/\>'
  - 해도 별 반응 없다. django의 security 기능임.
  - from django.utils.html import mark_safe 해서 사용하면 됩니다~

### raw_ids and inline admin

- raw_ids

  - raw_ids_fields
    - 기본적으로 django는 foreignkey selection에 input select를 사용한다.
    - input select를 바꾸는 것.
    - 예를 들어, room에 user가 너무 많으면.. 리스트에서 찾기 어려우니까..

- InlineModelAdmin

  - admin page에 다른 admin page를 추가하는 것.
  - InlineModelAdmin, TabularInline, StackedInline이 있음.
  - 먼저 InlineModel class를 만든다.
    - class PhotoInline(TarbularInlineModel):
      models = models.Photo
    - 그리고 삽입할 admin에 inlines = ( PhotoInline)을 추가하면 된다.

- save() method, -+\*models의 event를 가로채보자.

  - save method를 overriding해서 부모의 save 메소드 나중에 호출하는 것.
  - django documentation의 overriding predefined method 내용 참고.

- admin 페이지에서도 save시의 이벤트를 가로챌 수 있다.
  - save_model (self, request, obj, form, change)
    - change: 변경된 것이 있는지..
    - form: form 그자체의 html

## django seed

- 가짜 데이터를 빠르게 만들 수 있게 해준다.
- install: pipenv install django-seed

  - settings.py에 django_seed를 추가한다.
    - django seed의 document 참고. 검색해서..
  - 더미 유저 만들 때 사용했는데, superuser, staff 권한은 주지 않아야 한다는 것 참고.
    - seeder.add_entity(Model, howmany, { entity option })
    - option 자리에 따로 데이터를 지정할 수 있다.

### python manage.py <<command>>

- application 폴더에 들어가서 management라는 폴더를 만들어 준다(일종의 하위 어플리케이션)
  - django에서 자동으로 이용하는 것...
  - management안에
    - \_\_init\_\_.py를 만들도록 한다.
    - commands라는 폴더를 만들고 그 안에도 \_\_init\_\_.py를 만든다.
    - 그리고 command 안에 command 칠 python 파일을 만든다.
      - python manage.py fileyoumade
        - 라고 입력을 하면 커맨드가 완성된 것..
        - 그리고 만든 파일에 class Command를 만들어 준다..
          - 이 클래스는 django.core.management.base 의 BaseCommand 클래스를 상속 받는다.
          - 필요 메소드: handle(self, \*args, \*\*options)
            - handle에서 console로 메시지를 찍을 때, print 써도 되지만, success message를 쓰고 싶은 경우.
              - self.stdout.write (self.style.SUCCESS("message"))를 권장.
              - error 메시지는 style.ERROR 이용.
          - --times 와같은 argument를 넣고 싶다면, parser.add_arguments(self, parser) 함수를 만든다.
            - parser의 add_argument에 원하는 argument 넣어주면 된다.
            - action, default, type, help 등을 인자로 받음.
    - rooms / management/commands/seed_amenities 코드 확인.
