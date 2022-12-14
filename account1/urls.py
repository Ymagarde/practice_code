#from django.conf.urls import url
from django.urls import path, include
from .api import RegisterApi
#from .api import SimpleApI
urlpatterns = [
      path('api/register', RegisterApi.as_view()),
      #path('api/hello', SimpleApI.as_view() ),
]