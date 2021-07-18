
# Create your views here.

# CRUD : Create Read Update Delete

# views.py : 클래스형 뷰(라이브러리 제네릭 뷰), 함수형 뷰

# 웹페이지 접속 : 'URL' 입력 > 웹서버가 뷰를 찾아서 동작시킨다. -> 응답  
# URL 설정해야 함

from django.views.generic.list import ListView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

from .models import Bookmark

# ListView : 조건에 맞는 여러 객체를 보여준다
class BookmarkListview(ListView) : 
    model= Bookmark # models.py 에서 class 불러오기
    template_name='bookmark_list.html' # 반드시 지정하자

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