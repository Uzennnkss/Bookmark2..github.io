from django.urls import path
from .views import *

urlpatterns=[
    path('',BookmarkListview.as_view(), name='list'),
    path('add/',BookmarkCreateView.as_view(), name='add'),
    path('detail/<int:pk>/',BookmarkDetailView.as_view(),name='detail'), 
    #<int:pk> : 해당 bookmark의 id를 정수형으로 (primary key)
    path('update/<int:pk>/', BookmarkCreateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookmarkDeleteview.as_view(), name='delete'),
]