from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hedgehog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', 'summer.views.main_page'),
    url(r'^lessons/([0-9]+)/$', 'summer.views.video_lesson_page'),
    url(r'^lectures/all/$', 'summer.views.video_lectures_all'),
    url(r'^lectures/(.+)/$', 'summer.views.specific_course'),
    url(r'^teachers/$', 'summer.views.teachers'),
    url(r'^contacts/$', 'summer.views.contact_us'),
    url(r'^register/$', 'summer.views.registration_view'),
    url(r'^users/([0-9]+)/$', 'summer.views.user_view'),
    url(r'^login/$', 'summer.views.login_view'),
    url(r'^logout/$', 'summer.views.logout_view'),



)
