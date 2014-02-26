from django.conf.urls import patterns, include, url
from cerebro.views import home, dash,add,dele,train,trainupdate,test

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', home),
	url(r'^dash$', dash),
	url(r'^add$', add),
	url(r'^delete$', dele),
	url(r'^train$', train),
	url(r'^trainupdate$',trainupdate),
	url(r'^test$',test),

    # Examples:
    # url(r'^$', 'cerebro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
