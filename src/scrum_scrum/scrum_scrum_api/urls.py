from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

from . import views

router = DefaultRouter()
router.register('user', views.ScrumScrumUserViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('logout', views.LogoutViewSet, base_name='logout')

urlpatterns = [
    url(r'^activate/(?P<user_id>[a-zA-Z0-9]*)/(?P<activation_key>[a-zA-Z0-9]*)',
        views.activate),
    url(r'', include(router.urls)),
]
