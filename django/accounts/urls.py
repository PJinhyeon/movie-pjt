from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('profile/', views.profile_list, name='profile-list'),
    path('profile/<int:person_id>/', views.profile, name='profile'),

]