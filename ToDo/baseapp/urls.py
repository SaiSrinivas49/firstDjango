from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.TaskList.as_view(),name = 'TaskList'),
    path('task/<int:pk>/',views.TaskDetail.as_view(),name = 'TaskDetail'),
    path('create-task/',views.CreateTask.as_view(),name = 'CreateTask'),
    path('update-task/<int:pk>/',views.UpdateTask.as_view(),name = 'UpdateTask'),
    path('delete-task/<int:pk>/',views.DeleteTask.as_view(),name = 'DeleteTask'),
    path('login/',views.CustomLogin.as_view(),name = 'CustomLogin'),
    path('logout/',LogoutView.as_view(next_page = 'CustomLogin'),name = 'CustomLogout'),
    path('register/',views.Register.as_view(),name = 'Register'),
]