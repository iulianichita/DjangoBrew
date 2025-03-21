from django.urls import path, re_path
from . import views

# laborator9
from django.contrib.sitemaps.views import sitemap
from .sitemaps import MancareSitemap, VederiStaticeSitemap

sitemaps = {
    'micdejun_view': MancareSitemap,
    'static': VederiStaticeSitemap,
}

urlpatterns = [
	path("", views.index, name="index"),
    path("pag1", views.pag1, name="f"),
    path("pag2", views.pag2, name="g"),
    path("mesaj", views.mesaj, name="buna ziua"),
    path("data", views.data, name="data si ora"),
    path("nr_accesari", views.nr_accesari, name="nr de accesari"),
    path("suma", views.suma, name="suma nr"),
    path("text", views.text, name="text"),
    path("nr_parametri", views.nr_parametri, name="nr. de parametri"),
    path("operatie", views.operatie, name='operatie'),
    path("tabel", views.tabel, name='tabel'),
    path("lista", views.lista, name='lista'),
    path("elev", views.elev, name="elev"),
    re_path(r'^pagina/a{2,4}\d+/$', views.afisare_pag),
    re_path(r'^pag_cod/(?P<id>\d{3})/$', views.afis_cod),
    path("pag/<str:sir>", views.aduna_numere),
    path("liste", views.afiseaza_liste),
    re_path(r'^nume_corect/(?P<prenume>[A-Z][a-z]+-?[A-Z]?[a-z]+)\+(?P<nume>[A-Z][a-z]*)/$', views.numara_nume),
    re_path(r'^subsir/(?P<subsir>\d+[ab]+\d+)/$', views.cauta_subsir),
    path("afis", views.afis_template),
    path("prajituri", views.afisare_prajituri),
    path('main', views.afisare_main, name='afisare_main'),
    path('menu', views.meniu),
    re_path(r'micdejun/(?P<no_page>\d+)/$', views.micdejun, name='micdejun'),
    # re_path(r'micdejun_view/(?P<item_id>\d+)/$', views.micdejun_view, name='micdejun_view'),
    path('micdejun_view/<int:item_id>/', views.micdejun_view, name='micdejun_view'),
    re_path(r'bauturi/(?P<no_page>\d+)/$', views.bauturi),
    re_path(r'desert/(?P<no_page>\d+)/$', views.desert),
    path('aboutus', views.aboutus, name='aboutus'),
    path('contact', views.contact_view, name="contact"),
    path("thankscontactform", views.contactform_trimis, name='contactform_trimis'),
    path('ordernow', views.plasare_comanda),
    path('add_micdejun', views.add_micdejun, name='add_micdejun'),
    path('register', views.register_view),
    path('login', views.custom_login_view, name='login'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('logout', views.logout_view, name='logout'),
    path('passwordchange', views.change_password_view, name='passwordchange'),
    # re_path(r'^confirma_mail/(?P<cod>\w+)/$', views.confirmare_mail, name='confirmare_mail'),
    path('confirma_mail/<str:cod>', views.confirmare_mail, name='confirmare_mail'),
    path('add_vizualizare/', views.add_vizualizare, name='add_vizualizare'),
    path('promotii', views.addPromotie, name='promotii'),
    path('oferta', views.aloca_oferta, name='oferta'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('cart', views.cart, name='cart'),
    path('proceseaza_date', views.proceseaza_date, name="proceseaza_date"),
    
    #model
    path('elevi', views.afisare_elevi, name='elevi'),
    path('elevi_view/<int:id>', views.elevi_view, name='elev'),
    path('elevi_add', views.elevi_add, name='elevi_add'),
    
    #examen
    path('studenti', views.afisare_studenti, name='student'),
    path('cursuri_view/<int:id>', views.cursuri_view, name='cursuri_view'),
    path('cursuri_add', views.add_curs, name='cursuri_add'),
]





