from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from sparta_webapp import views
from django.conf.urls import include, url

import django

if django.VERSION < (1, 10):
    from django.views.i18n import javascript_catalog
    jsi18n_url = url(r'^jsi18n/$', javascript_catalog, {'packages': ('scribbler',)}, name='jsi18n')
else:
    from django.views.i18n import JavaScriptCatalog
    jsi18n_url = url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['scribbler']), name='jsi18n')


sitemaps = {
	"static": StaticViewSitemap,
}

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about",),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("search/", views.SearchView.as_view(), name="search"),
    # API's
    path("api/", include("sparta_webapp.apis.urls", namespace="api"), name="api"),

    # Scribbler
    path("scribbler/", include("scribbler.urls"), name="scribbler"),
    jsi18n_url,

    # Jet Admin Site

    path("jet/", include("jet.urls", namespace="jet"), name="admin"),
    path("jet/dashboard/", include("jet.dashboard.urls", namespace="jet-dashboard"), name="jet-dashboard"),

    # Django Admin, use {% url 'admin:index' %}

    path(settings.ADMIN_URL, admin.site.urls, name="myadmin"),

    # User management

    path("users/", include("sparta_webapp.users.urls", namespace="users"), name="users"),
    path("accounts/", include("allauth.urls"), name="account"),
    path("accounts/sshkey", views.UserKeyListView.as_view(), name="userkey_list"),
    path("accounts/sshkey/add", views.userkey_add, name="userkey_add"),
    path("accounts/sshkey/(?P<int:pk>\d+)$", views.userkey_edit, name="userkey_edit"),
    path("accounts/sshkey/<int:pk>/delete", views.userkey_delete, name="userkey_delete"),

    # Your stuff: custom urls includes go here

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
