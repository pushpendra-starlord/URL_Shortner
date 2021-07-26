from django.urls import path
from shortner.views import  login_view, logout_user, HomeView, signup

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path("", HomeView.as_view(), name='index'),
    path('signup/', signup, name='signup'),
]