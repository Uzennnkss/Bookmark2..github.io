# Bookmark CRUD
CRUD : Create Read Update Delete

---
<!-- model -->
### 1. models.py 
```py
from django.db import models

# Create your models here.
# 모델 : 데이터베이스를 SQL 없이 다루기 위해 사용 
# 데이터를 '객체화'해서 다루기 위해 사용 
# 모델의 필드(변수) = 테이블의 컬럼 
# 인스턴스 = 테이블의 기록
# 필드의 값(인스턴스의 필드값) = 레코드의 컬럼 데이터 값 

# 사이트 이름, 주소

class Bookmark(models.Model): 
    site_name= models.CharField(max_length=100, blank=True, null =True)#필드의 종류 명시해야 함 
    url=models.URLField('Site URL') # 링크 자동 생성 (입력받을 때 이이름으로 필드명을 보여주겠다. )

    
    def __str__(self) : 
        return "이름 : "+ self.site_name +", 주소 : "+self.url

# 필드의 종류가 결정하는 것 
# 1. 데이터 베이스의 컬럼 종류 및 제약 사항 
# 2. Form 의 종류 및 제약사항
```

### 2. admin.py 
모델을 관리자 페이지에서 관리할 수 있도록 등록한다. 
```py
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Bookmark)

```
---
<!--Read-->
## Read
### 1. views.py 
views.py : 클래스형 뷰(라이브러리 제네릭 뷰), 함수형 

웹페이지 접속 : 'URL' 입력 > 웹서버가 뷰를 찾아서 동작시킨다. -> 응답 URL 설정해야 함

* Listview ( 조건에 맞는 여러 객체를 보여준다) 제네릭 뷰 
```py
# Create your views here.

from django.views.generic.list import ListView
from .models import Bookmark

# ListView : 조건에 맞는 여러 객체를 보여준다
class BookmarkListview(ListView) : 
    model= Bookmark # models.py 에서 class 불러오기
    template_name='bookmark_list.html' # 반드시 지정하자
```

### 2. urls.py 
* boomark.urls.py (2차 urls.py)
```py
from django.urls import path
from .views import BookmarkListview

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
]
```
* config.urls.py (1차 urls.py)
```py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('bookmark/', include('bookmark.urls')),
    path('admin/', admin.site.urls),
]

```
### 3. templates
* bookmark_list.html (views.py의 template_name='bookmark_list.html')
```html
<div class="btn-group">
    <a href="#" class= "btn btn-info">Add Bookmark</a>
</div>

<p></p>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Site</th>
            <th scope="col">URL</th>
            <th scope="col">Modify</th>
            <th scope="col">Delete</th>
        </tr>
    </thead>

    <tbody>
        {% for bookmark in object_list %} <!--object_list : 여러개를 보여줄 때 사용 (ex.list), object : 상세한 내용 보여줄때 사용 (ex. detail)-->
        <tr>
            <td>{{forloop.counter}}</td>
            <td><a href="#">{{bookmark.site_name}}</a></td>
            <td><a href="{{bookmark.url}}" target="_blank"> {{bookmark.url}}</a></td>
            <td><a href="#" class="btn btn-success btn-sm">Modify</a></td>
            <td><a href="#" class="btn btn-success btn-sm">Delete</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>

```
---
<!--Create-->
## Create
### 1. views.py 
* Createview : 객체를 생성하는 폼을 보여준다.
    * fields : CreateView, UpdqteView에서 사용/ 폼에 사용할 필드 지정/ ModleForm 클래스의 Meta, field 속성과 동일한 의미
    * success_url = reverse_lazy : add 버튼을 누르면 list 화면으로 가겠다. 
```py

# Create your views here.
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Bookmark

class BookmarkListview(ListView) : 
    model= Bookmark 
    template_name='bookmark_list.html'

# CreateView :  객체를 생성하는 폼을 보여준다.
class BookmarkCreateView(CreateView):
    model=Bookmark
    fields=['site_name','url'] 
    #fields : CreateView, UpdqteView에서 사용/ 폼에 사용할 필드 지정/ ModleForm 클래스의 Meta, field 속성과 동일한 의미
    template_name='bookmark_create.html'
    success_url=reverse_lazy('list') #add 버튼을 누르면 list 화면으로 가겠다. 

    # template_name_suffix='_create' # bookmark/bookmark_create.html
```
### 2. urls.py 
* boomark.urls.py 
    * BookmarkCreateView 추가 
```py
from django.urls import path
from .views import BookmarkListview, BookmarkCreateView

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
    path('add/',BookmarkCreateView.as_view(), name='add'),

]
```
### 3. templates
* bookmark_create.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="" method="post">
        {% csrf_token %}
        {{form.as_p}} <!--자동으로 폼형성-->
        <!--views.py 에서 fields=['site_name','url']을 작성했기 때문에 site_name, 과 url에 대한 폼이 models.py 에 맞춰서 생성됨-->
        <input type="submit" value="Add" class="bth btn-info btn-sm">
    </form>
</body>
</html>
```
* bookmark_list.html
    * {% url 'add %} 추가
```html
<div class="btn-group">
    <a href="{% url 'add' %}" class= "btn btn-info">Add Bookmark</a>
</div>

```
---
<!--Detail-->
## Detail
### 1. views.py 
* DetailView : 객체 하나에대한 상세한 정보를 보여준다.

```py
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.views.generic.detail import DetailView

from .models import Bookmark

# ListView : 조건에 맞는 여러 객체를 보여준다
class BookmarkListview(ListView) : 
    model= Bookmark # models.py 에서 class 불러오기
    template_name='bookmark_list.html' # 반드시 지정하자 시발...

# CreateView :  객체를 생성하는 폼을 보여준다.

class BookmarkCreateView(CreateView):
    model=Bookmark
    fields=['site_name','url'] #fields : CreateView, UpdqteView에서 사용/ 폼에 사용할 필드 지정/ ModleForm 클래스의 Meta, field 속성과 동일한 의미
    template_name='bookmark_create.html'
    success_url=reverse_lazy('list') #add 버튼을 누르면 list 화면으로 가겠다. 

    # template_name_suffix='_create' # bookmark/bookmark_create.html

# DetailView : 객체 하나에대한 상세한 정보를 보여준다.

class  BookmarkDetailView(DetailView) :
    model=Bookmark
    template_name='bookmark_detail.html'
```

### 2. urls.py 
* bookmark.urls.py 
```py
from django.urls import path
from .views import *

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
    path('add/',BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>',BookmarkDetailView.as_view(),name='detail'), 
    #<int:pk> : 해당 bookmark의 id를 정수형으로 (primary key)

]
```

### 3. templates
* bookmark_detail.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {{object.site_name}}<br>
    {{object.url}}
    <!--object : 상세한 내용 보여줄때 사용 (ex. detail)-->
</body>
</html>
```

* bookmark_list.html
    * `<td><a href="{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a></td>` a 태그 생성

```html
<div class="btn-group">
    <a href="{% url 'add' %}" class= "btn btn-info">Add Bookmark</a>
</div>

<p></p>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Site</th>
            <th scope="col">URL</th>
            <th scope="col">Modify</th>
            <th scope="col">Delete</th>
        </tr>
    </thead>

    <tbody>
        {% for bookmark in object_list %} <!--object_list : 여러개를 보여줄 때 사용 (ex.list), object : 상세한 내용 보여줄때 사용 (ex. detail)-->
        <tr>
            <td>{{forloop.counter}}</td>
            <td><a href="{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a></td>
            <td><a href="{{bookmark.url}}" target="_blank"> {{bookmark.url}}</a></td>
            <td><a href="#" class="btn btn-success btn-sm">Modify</a></td>
            <td><a href="#" class="btn btn-success btn-sm">Delete</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>

```
---
<!--Update-->
## Update

## 1. views.py 

* UpdateView : 기존 객체를 수정하는 폼을 보여준다.
```py
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

from .models import Bookmark

# ListView : 조건에 맞는 여러 객체를 보여준다
class BookmarkListview(ListView) : 
    model= Bookmark # models.py 에서 class 불러오기
    template_name='bookmark_list.html' # 반드시 지정하자 시발...

# CreateView :  객체를 생성하는 폼을 보여준다.
class BookmarkCreateView(CreateView):
    model=Bookmark
    fields=['site_name','url'] #fields : CreateView, UpdqteView에서 사용/ 폼에 사용할 필드 지정/ ModleForm 클래스의 Meta, field 속성과 동일한 의미
    template_name='bookmark_create.html'
    success_url=reverse_lazy('list') #add 버튼을 누르면 list 화면으로 가겠다. 

    # template_name_suffix='_create' # bookmark/bookmark_create.html

# DetailView : 객체 하나에대한 상세한 정보를 보여준다.
class  BookmarkDetailView(DetailView) :
    model=Bookmark
    template_name='bookmark_detail.html'

#UpdateView : 기존 객체를 수정하는 폼을 보여준다.
class BookmarkCreateView(UpdateView):
    model=Bookmark
    fields=['site_name','url']
    template_name='bookmark_update.html'
    # models.py 에서 get_absolue_url() 함수를 이용해 다음화면으로 넘긴다. 
```

### 2. urls.py 
* bookmark.urls.py 
```py
from django.urls import path
from .views import *

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
    path('add/',BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>',BookmarkDetailView.as_view(),name='detail'), 
    #<int:pk> : 해당 bookmark의 id를 정수형으로 (primary key)
    path('update/<int:pk>', BookmarkCreateView.as_view(), name='update'),

]
```

### 3. templates
* bookmark_update.html
```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="" method="post"> <!--action : 데이터를 보내는 장소/  걍 화면에 보여줄 것이기 때문에 blank 처리한다. -->
        {% csrf_token %}
        {{form.as_p}} <!--자동으로 폼형성-->
        <!--views.py 에서 fields=['site_name','url']을 작성했기 때문에 site_name, 과 url에 대한 폼이 models.py 에 맞춰서 생성됨-->
        <input type="submit" value="Update" class="bth btn-info btn-sm">
    </form>
</body>
</html>
```

### 4. models.py 
* def get_absolute_url() 
```py 
from django.db import models
# return reverse
from django.urls import reverse

class Bookmark(models.Model): 
    site_name= models.CharField(max_length=100, blank=True, null =True)#필드의 종류 명시해야 함 
    url=models.URLField('Site URL') # 링크 자동 생성 (입력받을 때 이이름으로 필드명을 보여주겠다. )

    def __str__(self) : 
        return "이름 : "+ self.site_name +", 주소 : "+self.url


    def get_absolute_url(self) : 
        return reverse('detail', args=[(self.id)])

```
--- 
<!--Delete-->
## Delete

### 1. views.py 
* DeleteView : 기존 객체를 삭제하는 폼을 보여준다.

```py 
from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

from .models import Bookmark

# ListView : 조건에 맞는 여러 객체를 보여준다
class BookmarkListview(ListView) : 
    model= Bookmark # models.py 에서 class 불러오기
    template_name='bookmark_list.html' # 반드시 지정하자 시발...

# Create
# CreateView :  객체를 생성하는 폼을 보여준다.
class BookmarkCreateView(CreateView):
    model=Bookmark
    fields=['site_name','url'] #fields : CreateView, UpdqteView에서 사용/ 폼에 사용할 필드 지정/ ModleForm 클래스의 Meta, field 속성과 동일한 의미
    template_name='bookmark_create.html'
    success_url=reverse_lazy('list') #add 버튼을 누르면 list 화면으로 가겠다. 

    # template_name_suffix='_create' # bookmark/bookmark_create.html

# Detail
# DetailView : 객체 하나에대한 상세한 정보를 보여준다.
class  BookmarkDetailView(DetailView) :
    model=Bookmark
    template_name='bookmark_detail.html'

# Update
# UpdateView : 기존 객체를 수정하는 폼을 보여준다.
class BookmarkCreateView(UpdateView):
    model=Bookmark
    fields=['site_name','url']
    template_name='bookmark_update.html'
    # models.py 에서 get_absolue_url() 함수를 이용해 다음화면으로 넘긴다. 

# Delete
# DeleteView : 기존 객체를 삭제하는 폼을 보여준다.
class BookmarkDeleteview(DeleteView):
    model=Bookmark
    success_url=reverse_lazy('list') # Delete 버튼 누르면 삭제되고 list 화면으로 넘어감
    template_name='bookmark_comfirm_delete.html'
```

### 2. urls.py 
* bookmark.urls.py 
```py 
from django.urls import path
from .views import *

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
    path('add/',BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>',BookmarkDetailView.as_view(),name='detail'), 
    #<int:pk> : 해당 bookmark의 id를 정수형으로 (primary key)
    path('update/<int:pk>/', BookmarkCreateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookmarkDeleteview.as_view(), name='delete'),
]
```
### 3. templates
* bookmark_comfirm_delete.html
```html <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="" method="post"> <!--action : 데이터를 보내는 장소/  걍 화면에 보여줄 것이기 때문에 blank 처리한다. -->
        {% csrf_token %}
        {{form.as_p}} <!--자동으로 폼형성-->
        <!--views.py 에서 fields=['site_name','url']을 작성했기 때문에 site_name, 과 url에 대한 폼이 models.py 에 맞춰서 생성됨-->
        <input type="submit" value="Update" class="bth btn-info btn-sm">
    </form>
</body>
</html>
```
---
<!--templates 확장-->
1. base.html
{% block 이름 %} {% endblock %}: 다른 template에서 붙여쓰기를 할 수 있다.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title> 
</head>
<body>
    {% block content %}
    
    {% endblock %}
</body>
</html>
```
* bookmark_list.html
```html
{% extends 'base.html' %}
{% block title %} Bookmark List{% endblock %}}
{% block content %}
<div class="btn-group">
    <a href="{% url 'add' %}" class= "btn btn-info">Add Bookmark</a>
</div>

<p></p>
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Site</th>
            <th scope="col">URL</th>
            <th scope="col">Modify</th>
            <th scope="col">Delete</th>
        </tr>
    </thead>

    <tbody>
        {% for bookmark in object_list %} <!--object_list : 여러개를 보여줄 때 사용 (ex.list), object : 상세한 내용 보여줄때 사용 (ex. detail)-->
        <tr>
            <td>{{forloop.counter}}</td>
            <td><a href="{% url 'detail' pk=bookmark.id %}">{{bookmark.site_name}}</a></td>
            <td><a href="{{bookmark.url}}" target="_blank"> {{bookmark.url}}</a></td>
            <td><a href="{% url 'update' pk=bookmark.id %}" class="btn btn-success btn-sm">Modify</a></td>
            <td><a href="{% url 'delete' pk=bookmark.id %}" class="btn btn-success btn-sm">Delete</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

* bookmark_detail.html
```html
{% extends 'base.html' %}
{% block title %} Detail {% endblock %}}
{% block content %}

    {{object.site_name}}<br>
    {{object.url}}
    <!--object : 상세한 내용 보여줄때 사용 (ex. detail)-->

{% endblock %}
```

* bookmark_create.html
```html
{% extends 'base.html' %}
{% block title %} Create {% endblock %}}
{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{form.as_p}} <!--자동으로 폼형성-->
        <!--views.py 에서 fields=['site_name','url']을 작성했기 때문에 site_name, 과 url에 대한 폼이 models.py 에 맞춰서 생성됨-->
        <input type="submit" value="Add" class="bth btn-info btn-sm">
    </form>

{% endblock %}
```

* bookmark_update
```html
{% extends 'base.html' %}
{% block title %} Update{% endblock %}}
{% block content %}

    <form action="" method="post"> <!--action : 데이터를 보내는 장소/  걍 화면에 보여줄 것이기 때문에 blank 처리한다. -->
        {% csrf_token %}
        {{form.as_p}} <!--자동으로 폼형성-->
        <!--views.py 에서 fields=['site_name','url']을 작성했기 때문에 site_name, 과 url에 대한 폼이 models.py 에 맞춰서 생성됨-->
        <input type="submit" value="Update" class="bth btn-info btn-sm">
    </form>

{% endblock %}
```

* bookmark_comfirm_delete
```html
{% extends 'base.html' %}
{% block title %} Confrim Delete {% endblock %}}
{% block content %}
    <form action="" method="post">
        {% csrf_token%}
        <div class="aler alert-danger"> Do you want to delete Bookmark "{{object}}"? </div>
        <input type="submit" value="Delete" class  ="btn btn-danger">
    </form>

{% endblock %}
```

>> settings.py 에 DIRS 설정을 바꿔서 config 프로젝트내에 templates에 'base.html'을 생성했지만, 오류가 났다. 
>> 그래서 app 내에 'base.html'을 추가하였더니 잘 작동했다. 왜 그럴까?
```py
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')], # 앱 이외의 탬플릿 추가, BASE_DIR : 프로젝트의 루트 폴더 => BASE_DIR 하위에 있는 'templates' 폴더를 추가한다. 
        'APP_DIRS': True,  # 앱 하위에 있는 템플릿을 자동으로 읽는다. 
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
