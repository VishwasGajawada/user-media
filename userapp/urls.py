from django.urls import path
from userapp import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('login/',auth_view.LoginView.as_view(template_name='userapp/login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('signup/',views.signup,name='signup'),
    path('profile/<str:pk>/',views.profile,name='profile'),
    path('add_post/',views.add_post,name='add_post'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('post_detail/<str:pk>/',views.post_detail,name='post_detail'),
    path('delete_post/<str:pk>/',views.delete_post,name='delete_post'),
    path('make_comment/<str:pk>/',views.make_comment,name='make_comment'),
    path('delete_comment/<str:pk>/',views.delete_comment,name='delete_comment'),
]
