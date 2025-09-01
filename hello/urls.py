from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entry/<int:req_pk>', views.detail, name="detail"),
    path('entry_add', views.entry_add, name="entry_add"),
    path('entry/<int:req_pk>/delete', views.entry_delete, name="entry_delete"),
    path('entry/<int:req_pk>/edit', views.entry_edit, name="entry_edit"),

    path('login', views.login_page, name="login_page"),
    path('handle_login', views.handle_login, name="handle_login"),
    path('logout_page', views.logout_page, name="logout_page"),
    path('settings', views.settings_page, name="settings_page"),
    path('applysettings', views.applysettings, name="applysettings"),

    path('search', views.search_page, name="search_page"),
    path('signup', views.signup_page, name="signup_page"),
    path('finishsignup', views.finishsignup, name="finishsignup"),

    path('dataexport', views.dataexport, name="dataexport"),
]