from django.contrib import admin

# Register your models here.
# 모델을 관리자 페이지에서 관리할 수 있도록 등록한다. 

from .models import *

admin.site.register(Bookmark)

