from django.db import models
from django.urls import reverse

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


    def get_absolute_url(self) : 
        return reverse('detail', args=[(self.id)])

# 필드의 종류가 결정하는 것 
# 1. 데이터 베이스의 컬럼 종류 및 제약 사항 
# 2. Form 의 종류 및 제약사항
