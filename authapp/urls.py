"""authapp namespace url configuration"""

from django.urls import re_path
import authapp.views as authapp

app_name = 'authapp'
urlpatterns = [
    re_path(r'^login/$', authapp.LoginListView.as_view(), name='login'),
    re_path(r'^register/$', authapp.RegisterListView.as_view(), name='register'),
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.RegisterListView.verify, name='verify'),

    re_path(r'^profile/$', authapp.ProfileFormView.as_view(), name='profile'),
    re_path(r'^logout/$', authapp.Logout.as_view(), name='logout'),
]
