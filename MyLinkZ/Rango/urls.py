from django.conf.urls import patterns, url
from Rango import views

urlpatterns = patterns('', 
	
	url(r'^$', views.index, name='index'),
	url(r'^about', views.about, name='about'),
	url(r'^secret', views.secret, name='secret'),
	url(r'^static', views.static, name='static'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	
)