from django.conf.urls import patterns, url
from storyteller import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^story/(?P<story_slug>[\w\-]+)/$', views.story, name='story'),
    url(r'^search/$', views.search, name='search'),
    url(r'^story_room/(?P<storyid>[\w\-]+)/$', views.storyroom, name='storyroom'),
    url(r'^add_story/$', views.add_story, name='add_story'),
    # url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_profile/', views.register_profile, name = 'add_profile'),
    url(r'^profile/(?P<user_name>[\w\-]+)/$', views.profile, name = 'profile'),
    url(r'^rate_story/$', views.rate_story, name='rate_story'),
)
