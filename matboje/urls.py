from django.conf.urls import patterns, url

from matboje import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.MatbojDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/SubmitMatch/$', views.SubmitMatch, name='submit_match'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),    
)
