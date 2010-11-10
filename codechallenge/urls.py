from django.conf.urls.defaults import *
import tictactoe.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^codechallenge/', include('codechallenge.foo.urls')),
    (r'^tictactoe/$', 'tictactoe.views.index'),
    (r'^tictactoe/board/(?P<board_id>\d+)$', 'tictactoe.views.index'),
    (r'^tictactoe/board/(?P<board_id>\d+)/move/(?P<row>\d+)/(?P<col>\d+)$', 'tictactoe.views.move'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
