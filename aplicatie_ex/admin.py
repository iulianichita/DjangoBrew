from django.contrib import admin
from .models import Prajitura, Organizator, Locatie, Ingredient_cafenea, Bautura, Mancare, Desert, Comanda, Vizualizari, Promotii, CustomUser

# laborator4
class PrajituraAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informații Generale', {
            'fields': ('nume', 'descriere', 'pret')
        }),
        ('Date ', {
            'fields': ('temperatura','calorii', 'categorie', 'pt_diabetici', 'ingrediente', 'ambalaje'),
            'classes': ('collapse',),  # secțiune pliabilă
        }),
    )
    
class OrganizatorAdmin(admin.ModelAdmin):
    list_display = ('email', 'nume', 'nr')  # afișează câmpurile în lista de obiecte
    #list_filter = ('nume', 'descriere')  # adaugă filtre laterale
    search_fields = ('nume', 'email')  # permite căutarea după anumite câmpuri
    
class locatieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'adresa', 'telefon')
    search_fields = ('nume', 'adresa', 'telefon')
    
class ingredientAdmin(admin.ModelAdmin):
    list_display = ('nume', 'furnizor')
    search_fields = ('nume', 'cantitate')
    
class BauturaAdmin(admin.ModelAdmin):
    list_display = ('pret', 'nume', 'disponibila')
    list_filter = ('nume', 'pret')  # adaugă filtre laterale
    search_fields = ('nume', 'pret')
    fieldsets = (
        ('Informații', {
            'fields': ('pret', 'nume', 'marime')
        }),
        ('Date preparare', {
            'fields': ('disponibila', 'ingrediente_bautura',),
            'classes': ('collapse',),  # secțiune pliabilă
        }),
    )
    
class MancareAdmin(admin.ModelAdmin):
    list_display = ('pret', 'nume', 'cantitate')
    search_fields = ('nume', 'pret')
    
class DesertAdmin(admin.ModelAdmin):
    list_display = ('pret', 'nume', 'cantitate', 'marime')
    
# class ComandaAdmin(admin.ModelAdmin):
#     list_display = ('datacreare', 'nume', 'prenume', 'telefon', 'metoda_livrare', 'status')
#     list_filter = ('metoda_livrare', 'status')
#     search_fields = ('datacreare', 'nume', 'adresa_livrare')
#     fieldsets = (
#         ('Informații cumparator', {
#             'fields': ('nume', 'prenume', 'telefon')
#         }),
#         ('Produse', {
#             'fields': ('bauturi', 'micdejuns','deserturi')
#         }),
#         ('Date comanda', {
#             'fields': ('metoda_livrare','adresa_livrare','metoda_plata')
#         }),
#     )
    
class VizualizariAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'object_id', 'datavizualizare')
    list_filter = ('id_user', 'object_id', 'datavizualizare')
    search_fields = ('id_user', 'object_id', 'datavizualizare')

class PromotiiAdmin(admin.ModelAdmin):
    list_display = ('nume', 'data_expirare', 'reducere', 'tip_promotie')
    list_filter = ('data_expirare', 'reducere', 'tip_promotie')
    search_fields = ('nume', 'data_expirare', 'reducere', 'tip_promotie')

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(admin.ModelAdmin):
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gen','telefon', 'adresa', 'datanasterii', 'locatie_fav', 'blocat')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.form
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if request.user.groups.filter(name='Moderatori').exists():
            readonly_fields += ['username', 'datanasterii', 'telefon', 'adresa', 'locatie_fav', 'gen','is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'password']
            
        return readonly_fields


admin.site.register(Prajitura, PrajituraAdmin)
admin.site.register(Organizator, OrganizatorAdmin)

admin.site.register(Locatie, locatieAdmin)
admin.site.register(Ingredient_cafenea, ingredientAdmin)
admin.site.register(Bautura, BauturaAdmin)
admin.site.register(Mancare, MancareAdmin)
admin.site.register(Desert, DesertAdmin)
# admin.site.register(Comanda, ComandaAdmin)
admin.site.register(Vizualizari, VizualizariAdmin)
admin.site.register(Promotii, PromotiiAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.site_header = "Panou de Administrare Cafenea"
admin.site.index_title = "Bine ai venit în panoul de administrare"
admin.site.site_title = "Admin Site"


# model
from .models import Elev, Nota
class ElevAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prenume', 'datanasterii')
    list_filter = ('nume', 'prenume', 'datanasterii')
    search_fields = ('nume', 'prenume', 'datanasterii')
    
class NotaAdmin(admin.ModelAdmin):
    list_display = ('valoare', 'data_adaugare', 'elev')
    list_filter = ('elev', 'valoare')
    search_fields = ('elev', 'data_adaugare')
    
admin.site.register(Elev, ElevAdmin)
admin.site.register(Nota, NotaAdmin)


#examen
from .models import Student, Curs
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prenume', 'email')
    list_filter = ('nume', 'prenume', 'email')
    search_fields = ('nume', 'prenume', 'email')
    
class CursAdmin(admin.ModelAdmin):
    list_display = ('denumire', 'numar_credite', 'student')
    list_filter = ('denumire', 'numar_credite', 'student')
    search_fields = ('denumire', 'numar_credite', 'student')
    
admin.site.register(Student, StudentAdmin)
admin.site.register(Curs, CursAdmin)