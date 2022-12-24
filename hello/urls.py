from django.urls import path
from hello.views import*


urlpatterns = [
      path('register/',RegisterAPIView.as_view()),
      path('login/',LoginView.as_view(), name='login'),
      #path('logout/',logout_view, name='logout'),
      path('changepassword/',UserchangePassword.as_view(), name='changepassword'),
      path('SendPasswordResetEmail/',ResetPasswordSendEmailView.as_view(), name='sendpasswordresetemail'),
      path('reset-pasword/<uid>/<token>/',SetNewPasswordView.as_view(),name='reset-password'),
      
      path('pdata/',ProfiledataView.as_view(), name='profiledata'),
      path('ppik/',ProfilepikView.as_view(), name='profilepik'),
      path('uppik/<int:pk>/',uProfilepikView.as_view(), name='uprofilepik'),
      path('blog/',blogView.as_view(), name='blog'),
      path('blogfilter/',blogList.as_view(),),
      path('searchfilter/',SblogListView.as_view()),
      
      
]