from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from back import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('new', views.new, name='new'),
    path('profile', views.profile, name='profile'),
    path('login', views.log_in, name='login'),
    path('ask', views.ask, name='ask'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('like/', views.like, name='like'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
