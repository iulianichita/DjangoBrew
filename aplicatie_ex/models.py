from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# laborator4 (ex models)
class Organizator(models.Model):
    nume = models.CharField(max_length=100)
    email = models.EmailField()
    nr = models.IntegerField(null = True)
class Locatie_exemplu(models.Model):
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)
class Ambalaj(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    TIPURI_MATERIAL = [
        ('plastic', 'Plastic'), ('hartie', 'Hartie'), ('carton', 'Carton')
    ]
    material = models.CharField(choices=TIPURI_MATERIAL)
    pret = models.DecimalField(max_digits=5, decimal_places=5)
class Ingredient(models.Model):
    nume = models.CharField(max_length=30, unique=True)
    calorii = models.PositiveIntegerField(null=True)
    unitate = models.CharField(max_length=10, null=True)
class Prajitura(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    descriere = models.TextField(null=True)
    pret = models.DecimalField(max_digits=8, decimal_places=2)
    gramaj = models.PositiveIntegerField()
    temperatura = models.IntegerField()
    TIPURI_PRODUS = [
        ('comanda speciala', 'Comanda speciala'), ('aniversara', 'Aniversara'), ('editie limitata', 'Editie limitata'), ('pentru copii', 'Pentru copii'), ('dietetica', 'Dietetica'),('comuna', 'Comuna')
    ]
    tip_produs = models.CharField(choices=TIPURI_PRODUS)
    calorii = models.IntegerField()
    TIPURI_CATEGORII = [
        ('cofetarie', 'Cofetarie'), ('patiserie', 'Patiserie'), ('gelaterie', 'Gelaterie')
    ]
    categorie = models.CharField(choices=TIPURI_CATEGORII, default = 'comuna')
    pt_diabetici = models.BooleanField()
    ingrediente = models.ManyToManyField(Ingredient)
    ambalaje = models.ForeignKey(Ambalaj, on_delete=models.CASCADE, null=True)

# laborator4 (models cafenea)
class Locatie(models.Model):
    nume = models.CharField(max_length=20, unique=True, null=True)
    adresa = models.TextField(null=True)
    nr_angajati = models.IntegerField(null=True)
    phone_regex = RegexValidator(
        regex=r'^\+34\d{9}$',
        message="Numărul de telefon trebuie să înceapă cu +34 și să fie urmat de 9 cifre."
    )
    telefon = models.CharField(
        validators=[phone_regex], 
        max_length=12,
        unique=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.adresa}"

class Ingredient_cafenea(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=20, unique=True)
    furnizor = models.CharField(max_length=20)
    micdejuns = models.ManyToManyField(related_name='micdejuns', to='Mancare', blank=True)
    
    def __str__(self):
        return f"{self.nume}"

class Bautura(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    pret = models.FloatField()
    disponibila = models.BooleanField()
    marime = models.CharField(choices=[('regular', 'regular'), ('large', 'large')], default='regular', max_length=10)
    timp_preparare = models.PositiveIntegerField(default = 2)
    ingrediente_bautura = models.ManyToManyField(Ingredient_cafenea)
    #id_angajat = models.foreignKey(Angajat, null = True)
    
    @property
    def calculated_pret(self):
        if self.marime == 'large':
            return self.pret + 3
        return self.pret
    
    def __str__(self):
        return f"{self.nume} ({self.marime})"

from django.urls import reverse

class Mancare(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=20, unique=True)
    pret = models.FloatField()
    cantitate = models.PositiveIntegerField()
    marime_choices = [
        ('regular', 'regular'),
        ('large', 'large')
    ]
    marime = models.CharField(choices=marime_choices, max_length=10, null=True)
    timp_preparare = models.PositiveIntegerField(null=True)
    ingrediente_mancare = models.ManyToManyField(Ingredient_cafenea)
    categorie = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def save_model(self, request, obj, form, change):
        # print(dir(obj))
    
        form.cleaned_data['ingrediente_mancare'] = Ingredient_cafenea.objects.filter(micdejuns__id=dict(request.POST).get('ingrediente_mancare'))

        super(Mancare, self).save_model(request, obj, form, change)
        
    # laborator9
    actualizat_la = models.DateField(auto_now=True)
    def get_absolute_url(self):
        return reverse('micdejun_view', kwargs={'item_id': self.id})   
    
    def __str__(self):
        return f"{self.nume} ({self.marime}) "

class Desert(models.Model):
    nume = models.CharField(max_length=20, unique=True)
    pret = models.FloatField()
    cantitate = models.PositiveIntegerField()
    marime = models.CharField(choices=[('regular', 'regular'), ('large', 'large')], default='regular', max_length=10)
    timp_preparare = models.PositiveIntegerField(default = 1)
    ingrediente_desert = models.ManyToManyField(Ingredient_cafenea)
    #id_angajat = models.foreignKey(Angajat, null = True)
    
    def __str__(self):
        return f"{self.nume} ({self.marime})"

# laborator6
class CustomUser(AbstractUser):
    comenzi = models.ManyToManyField(related_name='comenzi', to='Comanda', blank=True)
    
    cod = models.CharField(max_length=100, null=True, blank=True)
    email_confirmat = models.BooleanField(default=False, null=False, blank=True)
    blocat = models.BooleanField(default=False, null=False, blank=True)

    gen_choices= [
        ('M', 'M'),
        ('F', 'F')
    ]
    gen = models.CharField(choices=gen_choices)
    telefon = models.CharField(max_length=15, blank=True)
    adresa = models.TextField(null=True, blank=True)
    datanasterii = models.DateField(null=True, blank=True)
    nr_puncte = models.PositiveIntegerField(blank=True, null=True, default=0)
    locatie_fav = models.ForeignKey(Locatie, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_block_users", "Can block or unblock users"),
            ("can_change_data", "Can change data users"),
        ]
        
    # def save(self, *args, **kwargs):
    #     if self.groups.filter(name='Moderatori').exists():
    #         self.is_staff = True
    #     super().save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        
        if self.id is not None:
            super().save(*args, **kwargs)
            if self.groups.filter(name='Moderatori').exists():
                self.is_staff = True
            else:
                self.is_staff = False
        
        super().save(*args, **kwargs)

# laborator7
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Vizualizari(models.Model):
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    id_product = GenericForeignKey('content_type', 'object_id')
    
    datavizualizare = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.id_user} ({self.id_product})"

class Promotii(models.Model):
    nume = models.CharField(max_length=20, default='Promotie', blank=True)
    data_creare = models.DateField(null=True, default='2021-01-01', blank=True)
    data_expirare = models.DateField(null=True, default='2021-01-01', blank=True)
    reducere = models.FloatField(default=0, blank=True)
    tip_promotie = models.CharField(max_length=20, choices=[('discount', 'Discount'), ('cadou', 'Cadou'), ('aniversare', 'Aniversare')])
    
    def __str__(self):
        return f"{self.nume} - ({self.reducere})"

# laborator11
class Comanda(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # produse = models.ManyToManyField(Mancare, through='ComandaDetaliu', null=True) 
    data_comenzii = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Comanda {self.id} pentru {self.user.username}"

class ComandaDetaliu(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE)
    produs = models.ForeignKey(Mancare, on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField()
    pret_per_unitate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantitate} x {self.produs.nume} la {self.pret_per_unitate} RON"



# model

class Elev(models.Model):
    nume = models.CharField(max_length=30)
    prenume = models.CharField(max_length=30)
    datanasterii = models.DateField()
    
    def __str__(self):
        return f"{self.nume} {self.prenume}"
    

class Nota(models.Model):
    valoare = models.IntegerField()
    data_adaugare = models.DateField()
    elev = models.ForeignKey(Elev, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.elev.nume} - {self.valoare}"
    
    

# examen

class Student(models.Model):
    nume = models.CharField(max_length=30)
    prenume = models.CharField(max_length=30)
    email = models.EmailField()
    anul_inscrierii = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.nume} {self.prenume}"
    
class Curs(models.Model):
    denumire = models.CharField(max_length=30)
    numar_credite = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.denumire}"