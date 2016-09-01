from django.conf.urls import patterns, include, url

from django.contrib import admin

import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djforums.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/register/$', 'djforums.views.register'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),
	
	url(r'^test$', 'djforums.views.test'),
	
	
	
	
	url(r'^$', 'djforums.views.index',name='index'),
	url(r'^addcate$', 'djforums.views.addcate', name='addcate'),
	url(r'^cate/(\d+)$', 'djforums.views.cateshow',name='cateshow'),
	url(r'^topic/(\d+)/addtopic$', 'djforums.views.addtopic',name='addtopic'),
	url(r'^topic/(\d+)$', 'djforums.views.topicshow',name='topicshow'),
	url(r'^topic/(\d+)/replytopic$', 'djforums.views.replytopic', name="replytopic"),

	url(r'^useradmin$','djforums.views.userinfoadmin', name='userinfoadmin'),
	url(r'^useradmin/updatephoto$','djforums.views.updatephoto', name='updatephoto'),
	
	url(r'^useradmin/defaultimg$','djforums.views.defaultimg', name='defaultimg'),
	url(r'^useradmin/updateimg$','djforums.views.updateimg', name='updateimg'),
	url(r'^useradmin/deletedefaultimg$','djforums.views.deletedefaultimg', name='deletedefaultimg'),
	
	url(r'^mytopic$', 'djforums.views.mytopic', name="mytopic"),
	url(r'^edit/(\d+)$', 'djforums.views.edit', name="edit"),
	url(r'^deletetopic/(\d+)$', 'djforums.views.deletetopic', name="deletetopic"),
	
	url(r'^accounts/password/change/', 'django.contrib.auth.views.password_change', {'template_name':'password_change.html'}),

	url(r'^accounts/password/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name':'password_change_success.html'}),

	
)


















