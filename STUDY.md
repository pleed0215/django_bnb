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

- ForkeyKey를 seed 하고싶을 때에는..??

  1. rooms를 예를 들면, host가 필요할 것인데..

  - 일단 유저들을 데이터베이스에서 가져온다.
    - 모든 유저들을 가져오는 것은 현명하지 못하다.
    - test이기에 일부 유저만 가져오는 것이 좋다.
    - 유저드이 너무 많을 때에는?? 데이터베이스에서 너무 많이 가져와야 되니까.
  - 개중요한 내용
    - 자바스크립트처럼 익명 함수를 넣어줄 수 있다.
    - lambda x:
    - python이 정말 편한 함수들이 많구나.
      - random.choice (array)
        - 이렇게 하면 배열에서 임의 원소 하나 끄집어 낸다.
  - 임의로 넣어주는 내용이 마음에 들지 않으면..
    - 위의 foreignkey 설정한 것처럼 해주면 된다.
    - lambda x: random.randint(r_min, r_max)
  - faker 라이브러리를 활용하는 것도 좋다.
  - photos 가 import하기 어려운 것 중 하나.
    - seeder의 execute를 실행하면, pk의 id list를 리턴한다.
    - 만들어진 list는 밑의 django.contrib.admin.utils.flatten을 이용하여 pk리스트를 만든다.
    - 만들어진 리스트를 이용하여 get(pk) 하여 room을 얻고..
    - Photo.object.create 하는데... 강의에서는 3~10/17 장의 사진을 만들어낸다.
    - photo를 upload 폴더에 넣어서.. media에 접근.. (기억이 나지 않으면 static 부분 참고)
    - 1~31까지의 랜덤을 이용하여 사진을 만들어 낸다.
  - django의 flatten
    - double array된 list를 끄집어 낼 때 사용..
    - from django.contrib.admin.utils import flatten
  - n:n 필드를 seeding
    - 여러가지 방법이 있을 수 있겠다만, 여기서는 랜덤정수를 줘서 짝수이면 어메니티를 추가.
      - room이 많을 경우는 문제가 있을 수도 있다.
    - 일단 따르자.
    - n:n field에서 아이템을 넣는 방법은 add 메소드를 사용하면 된다.
  - 또 중요한 내용.
    - 쿼리셋에서 배열로 데이터를 얻고 싶을 때에는 \*를 사용한다.(list의 command 참고)
    - 이걸 몰라서 엄청 삽질 했다...
    - choices를 사용하여 add 성공.
  - timedelta.
    - python은 기본 라이브러리들이 참 좋네..

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

# view part 시작

## Introduction to views and urls

- views.py

  - HttpResponse
    - view는 HttpResonse를 리턴해줘야 한다. django.http.HttpResponse
  - 실제로는 템플릿 렌더하는 경우가 더 많아서.. render 함수를 이용한다.
  - 템플릿을 사용하려면, settings.py -> TEMPLATES에 템플릿이 어디에 있는지 알려줘야한다.
    - DIRS 배열에, 현재 디렉토리의 template위치를 알려줘야한다. 지금 프로젝트인 경우에는 /templates라는 폴더를 사용한다.
      - So, we add a line that 'os.path.join(BASE_DIR, "templates")
    - 템플릿에 변수를 보낼 수 있다.
      - render의 context를 이용하면 됨. 딕셔너리 방식.
      - html에서는 \{\{\}\}: 변수 사용. \{% %\}: 파이썬 로직 사용.
        - 로직 사용시에는 일반 파이썬과는 달리 endif, endfor 등을 넣어 줘야한다.
  - template 사용
    - base.html을 상속 받아서 쓸 수 있음.
    - {% extends %}
    - {% block namespace %}
    - {% include %}

- urls.py
  - project가 작다면 config에 urls.py에 모든 url을 넣을 수 있지만, 프로젝트가 커지면 힘드니.. 분리하자.
  - 각각 프로젝트에 urls.py를 만들고, core에는 home, login, logout 등의 앱이 없는 url을 추가해주자.
    - url path는 기본적으로 django.urls.path를 이용한다.
      - path에 render를 지정할 때, *name*을 지정할 수 있다.
    - 이러한 urls.py는 config/urls.py에 django.urls.include를 이용하여 추가한다.
      - in config/urls.py -> urlpatterns = \[path("", include("core.urls")\] 이런식으로..
      - path와 비슷하게, include에서는 namespace를 지정할 수 있다.
        - namespace를 사용할 때에는 반드시, app_name을 같이 지정해줘야 한다.

## Home view

- view 만드는 방법 세가지로 보여준다 함.

  1. 100% 수동. 완전히 python만 이용.
  2. 코드 어느정도 사용..
  3. 코드 없이 view만으로 작업.

- home view에서 만약, 10개 씩의 방을 보여주고 싶다면..
  - Room.objects.all()\[0:10\]이런 식으로 제한을 주고 오프셋을 주면 된다.
  - 일반적으로 페이지 쿼리는 ~~/?page=1 이런식으로 쿼리를 주는 것이다.
    - 이런 파라미터들은 GET method
    - view의 인자로 들어오는 request.GET에서 가져오면 되는데...
    - GET은 QueryDict ...형태..
- QuerySet에 대해서..
  - QuerySet에서 all() method를 호출 한다고 해서 바로 모든 오브젝트들을 읽어 오진 않는다.
  - QuerySet은 게으르다.
  - print 등으로 사용하면 바로 데이터베이스에서 읽어온다.
- template에서...
  - python 문법을 전부다 사용 할 수 있는 것은 아니다..
  - 이를 테면.. for i in range(0, 100) 이런식으로 range 사용할 수 없다..
  - 또, 숫자 더하기 조차도 되지 않는다...
    - current_page + 1 이런 건 허용되지 않고, current_page|add:1, 이런식으로 필터링을 사용한다.
- template에서 여태까지 pagination을 만들었는데, django paginator라는 라이브러리가 있다고 한다.
  - django.core.paginator import Paginator하면 된다.
  - paginator = Paginator (list, size)
  - render에 넘겨줄 변수는 rooms = paginator.get_page(page_number) 이용하면, 여러가지 정보를 갖는 paginator를 얻는다.
    - object_list: 해당 페이지의 리스트
    - number: 현재 페이지
    - paginator.num_pages: 페이지 갯수, 마지막 페이지.
    - paginator에서 만약 잘못된 페이지로 가면... 마지막 페이지 등으로 이동하는데.. 예외처리가 몇 가지가 있는 것..
    - orphans의 개념
      - 마지막 페이지 등에 몇개의 아이템만 남는 경우가 많을 것인데..page보다 작은 요소..
      - orphans 옵션을 주면 옵션에 따라.. 옵션보다 작은 숫자의 아이템들은 표시되지 않는다.
    - get_page / page 차이
      - get_page는 페이지를 잘못 들어가도, 1페이지 또는 마지막 페이지로 이동..
      - 에러 핸들링에는 page를 사용하는 것이 더 낫다.
      - redirect하는 방법 배움.
- templateview를 이용하는 방법.

  - ListView: ClassBasedView 에서 파생..
    - django.views.generic.ListView
    - view class들은 as_view 함수가 내장되어 있다.
    - urls.py에 가서 render를 바꿔준다. HomeView.as_view()이런식으로..
    - 기본적으로 template을 갖는다. modelname_list.html 형태를 갖는다.
    - object_list를 내장하고 있다.
    - ClassBasedView를 보려면 좀 .. 쉽지 않아서..
      - ccv.co.uk 사이트에 가면 class based view에 대한 내용을 한눈에 보기 편하게 해놨다.
    - paginated_by
    - page_kwargs = 'page' 가 기본인데..
      - 놀랍게도 GET method의 page 입력이 자동으로 설정되어 있는 것.. 그래서 page라는 키워드라면... 자동으로... pagination
    - template_name_suffix = "\_list" 이렇게 되어 있기 때문에.. model_list.html 을 자동으로 찾는 것..
    - page_obj
  - 1,2 번째 방법에 비해 Class를 이용하니 코드가 아주 간단해 졌다.
  - class based view vs. function based view.

    - class based view: 한가지만 잘함.
    - function based view: 여러가지 잘하려면.. function based view가 더 낫다...

  - get_context_data를 overriding 해서 return 값을 주면.. context를 넘겨줄 수도 있다.

## Detail View

- rooms/:id 로 갈 것이기 때문에, urls.py를 만들어서 config해줘야 한다.
  - config/urls.py에도 추가할 것. app_name 추가하는 것도 잊지 말 것.
- js 와는 다른 url 패턴을 가진다.
  - js에서는 :id 등으로 들어가지만 django에서는 \<int:id> 형식으로 들어간다.
  - django document를 참고하는 것이 좋다.
  - int, str, slug, uuid, path
- rooms/urls.py에서 urlpattern에 \<int:pk> 를 추가.
  - detail_view() got an unexpected keyword argument 'pk' 이러한 메시지가 뜬다...
  - detail_view에 pk라는 argument를 추가해야 한다.
  - namespace를 사용하는 이유.
    - 일일히 urlpattern을 다 기억안하고 있어도 된다.
    - url tag를 사용하면 된다. {% url "namespace:name" path_arg %} 이런식으로.. 예를 들면,
      - "{% url "rooms:detail" r.pk %}" 이렇게 사용.
      - "{% url "core:home" %}" 얘는 argument가 없어도 된다.
- get_absolute_url
  - models.py에서 만든다. model에서 get_absolute_url을 override하는 것.
  - admin 사이트에서 이용하는 것인듯..
  - admin에서 그 모델에 해당하는 사이트로 이동하게 해준다...
  - django.urls.reverse 라는 함수를 이용..
    - 위 처럼 namespace를 이용할 수 있게 해준다.
    - reverse ("namespace:name", kwargs = { ...keyword arguments })
      - ex) reverse("homes:detail", kwargs = {'pk': self.pk})
- template에서 django object에 접근하는 것은 쉬운편.. 기본적으로 장고에서 사용하는 방법과 동일.
- exception
  - django.db.models DoesNotExist
- 404 error
  - from django.http import Http404
    - error 코드라, raise Http404 하면 된다.
  - template에 가서. 404.html페이지를 만들면 된다.
  - _error handling이 하라는대로 했는데, 잘안됨. 나중에 따로 해야 될 부분인듯.._

### DetailView Class

- Detail 역시 View class가 존재한다.
- 복잡하지 않기 때문에 굳이 function 타입을 지우지 않아도 될 듯하다.
- 그래도 알아야 하니..

# Searchview

- 어려운 내용은 없는데..
- template 파일 이름에 변경이 조금 들어갔다.
- #13.2 Select choices 2:40 경 내용에 보면,, {**form, **choice} 이런 내용이 나오는데...
  - 아마도 오브젝트들을 합치는 것 같은데..
  - \*\*키워드 인자로 만들어주는 연산자가 아닐까 추정.
- is 와 == 차이
  - is 는 오브젝트 타입도 같아야 true
  - == 는 오브젝트 타입이 달라도 값이 같으면 True
- request.GET.get, request.GET.getlist 차이
  - getlist는 같은 이름을 갖는.. 애들의 리스트를 리턴해서..
  - 만약 체크박스에서 같은 이름을 갖는 애들을 한 번 얻고 싶으면, getlist를 사용하여야 한다.
    - search view확인 하면 예를 볼 수 있다.
    - getlist 값들은 string이라는 점..
  - pk는 int이기 때문에 stringify해야 하는데... django template에서는 str함수가 안된다.
    - slugify라는 필터링을 이용하면 된다.

## Filtering

- filter
  - django document 확인 필수 적으로 해야 할듯하다.
  - SQL을 몰라도.. SQL 조건문을 이용할 수 있는 것..
  - 여러가지 필터링을 할 수도 있고.. 조건부 필터링을 걸 수도 있다.
    - 예를들어, guest가 0이라면, 0으로 검색하면 안된다.
  - filter는 chaining이 가능하다. 여러가지 필터링을 걸어야 하는 것..
    - 코드 꼭 확인 문서 꼭 확인.
  - 강의에서 filtering trick을 알려준다.
    - dictionary를 만들어서.. kwargs 형태로 filter에 넘겨줌.
    - 코드확인.
  - many to many field 를 filter해주는 것에서 강의 내용이 조금 이상했다.

## django form..

- 위에 개.. 긴 코드 및 삽질을 django form이 해준단다. 얼쑤~
- search.html, search_view 모두 지워야 한다고 해서..
- 사본 만들거나 주석처리 하였음.

### forms.py를 만들자.

- model을 정의한 것처럼, form을 정의 해주면 된다.
- 항상 그렇듯 documentation을 많이 참조해야 한다.
- model이 field를 가진 것처럼, form도 field를 갖는다.
  - Charfield
    - initial을 줄 수 있다.
- 보이는 형태. html
  - html을 확인 해보면 기본적으로 table로 나오는데..
  - as_p, as_ul, as_table로써 변경할 수 있다.
- 문서를 참고하고..
  - initial 초기값
  - required
  - widget => 보여지는 형태를 정해주는 기본이라 할 수 있는데..
    - CharField 같은 경우에는 TextInput 등으로 되어 있는데 .. 시험삼아 Textarea등으로 바꾸면.. 보여지는 형태로 바뀐다.
    - many to many field를 선택할 경우 기본적으로 선택하는 방식이 좀 지저분해 보이긴한다.
      - amenity를 예를 들면.. ModeMultipleChoiceField 기본적으로 스크롤하면서, 컨트롤을 누르면서 여러가지 아이템을 선택하는 것.
      - widget을 forms.CheckboxSelectMultiple로 바꿔보자.
- django form을 사용하지 않고, python으로만 했을 때 form 값을 기억하는 방법은 request.GET.~~을 사용하였는데..
  - django form에서 그 값을 기억 시키려면, 생성자에서 request.GET을 넘겨주면 된다.
  - unbound form -> bound form 가면서 data 유효성도 검사한다.
  - is_valid 메소드. form 데이터가 다 옳은가 검사.
- cf. alt + 더블클릭. 여러 줄 선택할 때 사용.. 맥에서는 command+shift+L, 윈도우에서는 alt+shift+L
- 결과값들을 paginator 하기..
  - 한가지 문제점: paginating 할 때마다 filter 및 query 수행할 것인데.. 괜찮을까..??

# User Login / Logout

# 14. LoginView

### Relatively harder way making authentication

- 이쯤 되면 위에서 배운 내용이 중복되서 나오는...
- form view를 이용하여 form을 만드는데..
- 패스워드 필드 만드는 방법
  - charfield 이용하여 만든다. 스택오버플로우 검색 내용으로는 CharField(widget=forms.PassInput())으로 하면 된다고 하고 실제로 작동하긴 함.
- method post로 form 데이터를 넘길 때..

  - csrf_token을 줘야 한다. 잘못된 입력 방지.. 위해. 해킹 방지 등.. cross site request forgery

- data 유효성 확인 및 정리.

  - clean\_(fieldname)
    - 아무것도 리턴하지 않으면, 그 필드 값을 지워버린다.
  - cleaned_data는 모든 데이터 정리한 결과.
  - data validation과 error handling 방법 화인할 필요가 있음.
  - password 맞는지 체크하려면 유저데이터를 가지고 와야 한다.

  - clean method.

    - clean\_(fieldname) 방식으로 유효성 검사하기에는 좀 그런경우.. 여러가지 데이터를 같이 검증해야 하는 경우 사용.

    - error handling
      - add_error(field, error)
      - clean method를 사용하려면, 어디에서 에러가 발생했는지.. 알려줘야 한다. 코드 참고.
        - 이 경우에는 raise를 굳이 사용할 필요는 없다.
    - clean method를 사용했다면, cleaned_data를 리턴해줘야 하는 것이.. 옳다.

  - django.contrib.auth lib에 보면.. authenticate, login 함수가 있다.
    - authenticate 이후 login을 하게 되면..
    - request.user 가 활성화...
    - request.user.is_authenticated 확인하면.. 로그인 여부를 알 수 있는 것.
      - request의 user정보가 어떻게 넘어왔을까??
      - django의 context_processor라는 것에 의해.
        - template에 정보를 추가하는 역할을 한다.
    - logout은 상대적으로 굉장히 간단.

## easy way making authentication

- LoginView라는 것도 있는데..?
  - django.contrib.auth.views.LoginView
- FormView 활용..

  - django.views.generic.FormView

- reverse_lazy
  - config.url 을 불러오기 전에 reverse가 호출되면...
  - url 관련 에러가 발생하는데.. 이를 막기 위한 것..
- login 만드는 방법은 여러가지가 있는 것 같아~~
- django.contrib.auth.LoginView를 이용도 해봤고..
- 직접 폼을 만들어서 로그인까지 진행도 해보고, FormView를 이용해서도 해봤다.

## 15. Signup View

- 다른 건 로그인과 비슷..
- clean 사용법 좀더 익히고..
- save method 오버라이딩 하는 것 참고.
  - user 만드는 방법도 참고.

* Signup은 일종의 데이터베이스 모델에 있는 데이터를 폼에 렌더링하고 폼의 데이터를 데이터베이스에 입히는 것..이지만..!
  - django에서는 이것을 도와주는 ModelForm이라는 것이 있다...
    - ModelForm을 상속 받고..
    - Meta class를 안에 만들어주면 된다.
      - 속성으로 models, fields를 만들어주면 된다.
    - 기본적으로 clean method들과 save 메소드가 있다.
      - Form 버전과는 달리 굳이 uniqueness validation을 하지 않아도 된다.
      - 기본적으로 만들어져 있기 때문에, save method가 원하는 바대로 잘 되지 않을 수 있다.
        - 이를테면, username에 email을 넣고 싶은데.. 잘 안된다.
        - save method를 overriding해야 하는데, commit=False 옵션을 save에 줘야 한다.
          - commit=False의 의미는 데이터베이스에 데이터를 만드는데, 데이터베이스에 데이터를 올리는 것은 아닌 단계..
          - 즉 save method commit=False하여, username=email을 넘겨주면 되는 것이다.

# 16.Email verification

## from django.core.mail import send_mail

### mailgun.com

- google 계정이나 다른 계정에서 지금 서버에서 메일을 보내면 스팸 처리가 될 것..
- 그래서 mailgun.com이라는 사이트를 이용해보자.
  - singup 시 웬만하면 카드 정보를 입력해야 한다. 그렇지 않으면, 너가 등록한 이메일 계정으로 밖에 이메일을 보낼 수 밖에 없음.
  - 언제나 그렇듯 documentation을 참고해야 한다.
    - django sendmail은 smtp를 사용하므로, 일단은 setting.py에 EMAIL_HOST, EMAIL_PORT를 설정해줘야 한다.
    - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD 설정도 해줘야한다.
    - password를 소스코드에 남기는 심각한 문제가 발생하는데...!
    - django environment라는 라이브러리를 사용한다. dotenv cross env와 비슷헌듯..
      - manage.py 에 main 시작 또는 시작전에 dotenv import하고 dotenv.read_dotenv()함수 호출하고..
      - 사용은 os.environ.get("key")로 사용하면 된다.
- 설정이 완료 되었으면,
  - User model에 가서 field를 추가해주자.
  - is_email_confirmed = models.BooleanField로 ...
  - email_verify_key도 하나 만들어주자.
    - 기본적으로 verification을 해야 하니.. verification 키가 있는 것이 맞다.
  - from django.conf import setting 하면.. setting에 있는 설정들 쓸 수 있다.
  - send_mail 함수에서 html_message를 사용하여야 html태그를 이메일에 첨부할 수 있다.
    - 그냥 message에서 사용하면 태그들이 들어가지 않는다..
    - from django.utils.html import strip_tags를 사용하면, html 태그를 일반 텍스트로 바꿔준다..
      - mail message는 html 메시지로 작성을 하고, strip_tags(html_message)를 이용하여 일반 텍스트도 만들어줘야 한다.
        - 가끔 html이 포함안되는 메일들이 있기 때문이다.
      - from django.template.loader import render_to_string 을 이용..하여..
        - template을 문자열로 만든다.
- 강의에서는 verification failed 시에 일단 나중에 알려준다고 넘어감.
  - django message에 대해..
  - 나는 일단 template으로 처리했다.

# 17. Log in with github

- OAuth 프로토콜 이용하는 모든 로그인 방법 다 통한다.
- partials/social_login.html을 만들어서 login에 include.
- view와 url에 일단 social login 관련 url / view를 만들어주고...
  - github 같은 경우 my / settings / development setting / oauth apps에 가서 setting 진행.
    - callback url등 지정하고, 세팅 완료 후, clientid, client_secret key를 밭게 되는데 이를 .env에 저장.
    - django로 돌아와서 callback 관련된 url 및 view도 만들어줘야 한다.
    - .env에 관련된 변수들도 만들어주자.
- models.py로 가서 login method 관련 필드를 만들어주자.
- github login은 총 3단계,
  1. app에 접근하여 get method로 보내라는 데이터 보내고 나서, code를 얻는다.
  2. 얻은 코드와 client id, client secret, code 등을 post method로 보내 token을 얻는다.
  3. 얻은 토큰을 get method 이용하여 해당하는 api 주소에 가서 정보를 받아 온다.
- github에서 콜백이 되면 code 관련된 파라미터가 리턴으로 들어오는데, 이를 GET을 이용하여 get하자.
  - 나중에 이 코드를 github auth 관련된 주소에 POST로 보내야 한다.
  - 자세한건 github auth 관련된 페이지를 참고하면 된다.
  - django나 python에서 post하는 방법에 대해서는 알려주지 않았는데.. 이부분은 나중에 알아도 되고...
  - python scraping에서 사용하였던, requests 라이브러리를 사용한다고 한다.
    - post method 사용 시, github auth 페이지에 가면...
    - json type으로 데이터를 받거나 xml타입으로 받고 싶으면.. header에 옵션을 application/json, xml 등으로 줘야 한다고 적힘.
      - headers 주는 것도 한 번 확인 해보길..

# 18. Log in with kakao

- 스스로 먼저해보기.
- kakao는 development 페이지에서 설정해줄 것이 몇가지 있다. 이설정을 안해주면 정보를 얻어 올 수 없어.
- profile image url을 추가하는 것이 쉽지 않다.
- User model의 avatar는 ImageField인데, FieldFile과 같다.

  - FieldFile은 save메소드가 있는데, save(name, content, save=True)인데.. filename과 filecontent를 스토리지 클래스에 넘겨준다(저장한다는 뜻..)
  - content에 들어갈 것은 말그대로 이미지 파일 정보.
  - 여기서는 kakao profile 의 이미지를 가져오는데.. requests module을 통하여 가져온다.. 그러면.. kakao profile url에 있는 내용을 requests를 통해서 가져올 수 있으며..
    - 이는 requests.get의 결과값에 content attribute를 이용하면 content를 가져올 수 있는 것.
  - 여기서 또 한가지 어려운 개념이 나오는데..
    - 위의 content만으로는 django에서 부족하다, 니코의 이야기에 따르면 bullshit 이 필요한데..
      - django.core.files.base import ContentFile 클래스를 이용하는데..
      - 실제파일이라기 보다는 raw-content를 갖는..File-like object라한다.
  - 그래서 avatar를 저장하려면. avatar.save (name, ContentFile(request_result.content)) 하면 되는 것..

  - # 18.3 UserCreationForm.
  - 우리는 django를 거의 이용하지 않고, python 기능만 사용해서 유저등록 폼을 만들었는데..
  - UserCreationForm을 이용하면 더 쉽게 유저 등록을 시킬 수 있다.
  - view에서 그냥 UserCreationForm을 이용해도 되고 아니면, 만들어 놓은 폼클래스는 forms.ModelForm을 상속받았는데.. UserCreationForm을 상속받아서 하면 아주 간단하다.
    - django.contrib.auth.forms.UserCreationForm
    - 참고. django의 password validation 기능을 이용하고 싶다면, django.contrib.auth.password_validation을 사용하면 된다.
    - UserCreationForm에서 확인해서 코드를 보는 것도 좋다고 본다.

# 19. Tailwind CSS

- 대부분은 framework식으로 거진 다 만들어져있는 것들이 많은디..
  - Most CSS frameworks do too much
  - flask와 비슷한 말을.. 하지만 나는 쟝고를 사용하고... 뭔가 모순적이지만, 도움될듯..
  - 부트스트랩 같은 프레임워크를 사용하면 사이트들이 다 똑같아 보이는데, tailwind는 그렇지 않다.
    - builtwithtailwind.com
  - vscode 에서 사용하려면.
    - tailwind intellisense를 사용하도록.

* 테일윈드는 utility first
* 직관적으로 빠른데,
* 코드 재사용 문제에 대해 고찰할 필요가 있었는지..
  - css에서 @apply를 사용하는데, 나는 이걸 첨본다.
* Preflight ...?

  - tailwind color pallete

* tailwind는 PostCSS라는 것을 사용한다.

  - gulp를 setting 해줘야 하기 때문에 nodes를 사용 하여야 한다.
    - npm install -D gulp gulp-csso gulp-postcss gulp-sass node-sass autoprefixer
  - 그리고 나서 tailwind css install
    - npm install tailwindcss -D
    - npx tailwind init -> tailwind.config.js
  - gulpfile.js를 /에 만들어 놓자.

    - 위 라이브러리를 gulpfile.js에 세팅해서 export 해줘야 함. 파일 참고.
    - 라이브러리 사용방법이라 그냥 익히는 수 밖에 없다.
    - gulp 설정 이후 결과적으로 assets들을 static으로 optimize하는데...

      - 모든 수정은 assets에서 이뤄져야 하며, 컴파일된 결과를 서버에서 사용하는 것.
        - assets를 수정할 때마다, gulp 컴파일을 해줘야 한다.
      - static을 그냥 url에서 사용할 수 없기 때문에, django에게 static 사용하는 것을 알려줘야 한다.
        !!!!!!!!!!

        - static 설정방법

          - settings.py -> STATICFILES_DIR을 설정해준다.
          - UPLOAD 설정과 비슷하게 os.path.join을 이용한다.
          - template/base.html에 stylesheet를 링크 시켜 줘보자.
            - <link rel="stylesheet" href="http://127.0.0.1:8000/static/css/styles.css" />
            - 링크는 더러워 보이는데 추후에 간단하게 하는 방법이 있고, 적용하면 tailwindcss의 기본스타일이 적용된 것을 확인 가능하다.
            - load static 이후, static 태그를 사용하면 간단하게 볼 수 있다.
              - top에, {% load static %}, <link rel="stylesheet" href="{% static "css/styles.css" %}/>

- .gitignore에 node_modules 추가해주는 걸 잊지 말자.


## tailwind css
- 사이즈 단위
  - em, rem 많이 사용
    - em: fontsize, rem: root fontsize
    - tailwind default root font size는 16px
- container -> box 이지만, responsive.

