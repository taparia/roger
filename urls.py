from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'roger.views.home', name='home'),
    # url(r'^roger/', include('roger.foo.urls')),
   # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
	(r'^tinymce/',include('tinymce.urls')),
	(r'^$','pages.views.MainHomePage'),
	(r'^$',direct_to_template,{'template':'index.html'}),
	(r'^beers/$','beer.views.BeersAll'),
	(r'^beers/(?P<beerslug>.*)/$','beer.views.SpecificBeer'),
	(r'^brewerys/(?P<breweryslug>.*)/$','beer.views.SpecificBrewery'),
	(r'^register/$','drinker.views.DrinkerRegistration'),
)

urlpatterns += staticfiles_urlpatterns()
