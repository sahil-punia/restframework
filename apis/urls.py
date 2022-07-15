
from django.db import router
from django.urls import path,include
from .views import RegisterView,MyObtainTokenPairView , ProfileFunView,UpdateProfileView,ApiViewProfile,UpdateProfile,GenricApiProfileView,ViewsetsApi,GenricviewsetProfileView,ModelViewsetAPi
from rest_framework_simplejwt.views import TokenRefreshView
#create default router to viewsetapi
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('profile' ,ViewsetsApi ,basename='profile')
router.register('genericviewset',GenricviewsetProfileView ,basename='viewset')
router.register('modelview-api' ,ModelViewsetAPi ,basename='modelview')

urlpatterns = [
    path('viewset-api' ,include(router.urls)),
    path('viewset-api/<int:pk>' ,include(router.urls)),
    # path('viewset-api' ,include(router.urls)),
    path('register' , RegisterView.as_view()),
    path('login/',MyObtainTokenPairView.as_view()),
    path('login/refresh',TokenRefreshView.as_view()),
    path('functionbased-profile',ProfileFunView),   
    path('updatefun-profile/<int:pk>',UpdateProfileView),
    path('apiview-profile',ApiViewProfile.as_view()),  
    path('update-profile/<int:id>',UpdateProfile.as_view()), 
    path('generic-apiview-profile',GenricApiProfileView.as_view()), 
    path('generic-apiview-profile/<int:id>',GenricApiProfileView.as_view()),
    # path('genericviewset-apiview-profile',GenricviewsetProfileView),      
]
