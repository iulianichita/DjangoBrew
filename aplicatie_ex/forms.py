from django import forms
from django.core.exceptions import ValidationError
from .models import Bautura, Mancare, Desert, Comanda, Locatie, CustomUser, Elev
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
import re, string, random

def validate_phonenumber(value):
    if not (value.startswith('07') or value.startswith('+407')):
        raise ValidationError("Nr. de telefon trebuie sa inceapa cu 07")
    if value.startswith('07') and len(value) != 10:
        raise ValidationError("Nr. de telefon trebuie sa aiba minim 10 cifre")
    if value.startswith('+407') and len(value) != 12:
        raise ValidationError("Nr. de telefon trebuie sa aiba minim 12 cifre")

def validate_names(value):
    if value and value != value.capitalize():
        raise ValidationError("Textul acestui camp trebuie sa inceapa cu litera mare.")
    if value:
        for c in value:
            if not (c.isalpha() or c.isspace()):
                raise ValidationError("Textul acestui camp trebuie sa contina doar spatii si litere.")

def validate_initcap(value):
    if value != value.capitalize():
        raise ValidationError("Textul acestui camp trebuie sa inceapa cu litera mare.")


# laborator5 -- validarea la sf mesajului trebuie sa existe nume
class ContactForm(forms.Form):
    nume = forms.CharField(validators=[validate_names], 
                            max_length=10, label='Nume', 
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'styled-input','placeholder': 'Introdu numele'}))
    prenume = forms.CharField(validators=[validate_names], label='Prenume', required=False, widget=forms.TextInput(attrs={'class': 'styled-input','placeholder': 'Introdu prenumele'}))
    datanasterii = forms.DateField(label="Data nasterii", required=False, widget=forms.DateInput(attrs={'class': 'styled-date', 'type': 'date', 'placeholder': 'Introdu data nasterii'}))
    
    email = forms.EmailField(label='Email', required=True,
                            widget=forms.EmailInput(attrs={'class': 'styled-emailinput',
                                                            'cols': 40,
                                                            'rows': 1,
                                                            'placeholder': 'Introdu email'}))
    confirm_email = forms.EmailField(label='Confirmare Email',
                                    required=True,
                                    widget=forms.TextInput
                                        (attrs={'class': 'styled-emailinput',
                                                'cols': 40,
                                                'rows': 1,
                                                'placeholder': 'Reintrodu email'}))
    
    TIPURI_MESAJ = [
        ('Select', 'Select'),
        ('reclamatie', 'reclamatie'),
        ('intrebare', 'intrebare'),
        ('review', 'review'),
        ('cerere', 'cerere'),
        ('programare', 'programare')
    ]
    
    tip_mesaj = forms.ChoiceField(choices=TIPURI_MESAJ, label='Tip mesaj', required=False, widget=forms.Select(attrs={'class': 'styled-choicefield', 'placeholder': 'Alege subiect'}))
    subiect = forms.CharField(validators=[validate_names], label='Subiect', required=True, widget=forms.TextInput(attrs={'class': 'styled-input','placeholder': 'Introdu subiectul'}))
    min_zile = forms.IntegerField(label='Minim zile asteptate',
                                    min_value=1, 
                                    required=True, 
                                    widget=forms.NumberInput(attrs={
                                        'class': 'styled-minzile',
                                        'placeholder': 'Introdu nr. de zile'
                                        }))
    mesaj = forms.CharField(widget=forms.Textarea(attrs={
                'class': 'styled-textare',
                'rows': 5,
                'cols': 40,
                'placeholder': 'Scrie-ne un mesaj!'
            }), label='Mesaj(va rugam sa va si semnati)', required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@domeniu.com'):
            raise forms.ValidationError("Adresa de email trebuie să fie de la domeniu.com")
        return email
    
    def clean_datanasterii(self):
        datanasterii = self.cleaned_data["datanasterii"]
        
        if datanasterii is not None:
            current_date = datetime.now().date()
            varsta = int((current_date - datanasterii).days / 365.25)
            
            if datanasterii is not None and varsta < 18 :
                raise forms.ValidationError('Expeditorul trebuie sa fie major.')
        
        return datanasterii
    
    def clean_mesaj(self):
        mesaj = self.cleaned_data["mesaj"]
        mesaj_verificat = re.split(r'\W+', mesaj)
        
        if len(mesaj_verificat) < 5 or len(mesaj_verificat) > 100:
            raise forms.ValidationError('Mesajul nu poate sa contina mai putin de 5 si mai mult de 100 de cuvinte.')
        
        for cuvant in mesaj_verificat:
            if cuvant.startswith('http://') or cuvant.startswith('https://'):
                raise forms.ValidationError('Mesajul nu poate contine linkuri.')
            
        if mesaj_verificat[len(mesaj_verificat)-1] != self.cleaned_data["nume"]:
            raise forms.ValidationError('Este necesara semnatura la finalul mesajului.')
        
        return mesaj
    
    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Adresele de email nu coincid.")
        
        datanasterii = cleaned_data.get("datanasterii")
        if datanasterii:
            today = datetime.now().date()
            delta = today - datanasterii
            years = delta.days // 365
            months = (delta.days % 365) // 30
            cleaned_data["varsta"] = f"{years} ani și {months} luni"

        mesaj = cleaned_data.get("mesaj")
        if mesaj:
            mesaj = " ".join(mesaj.split())
            cleaned_data["mesaj"] = str(mesaj)


        return cleaned_data

class MancareForm(forms.Form):
    NUME_CHOICES = [
        ('select', 'Select'),
        ('toast', 'Toast'),
        ('eggs', 'Eggs'),
        ('sandwiches', 'Sandwiches')
    ]

    nume = forms.ChoiceField(choices=NUME_CHOICES, label='Nume')
    min_price = forms.IntegerField(label='min_price', required=False)
    max_price = forms.IntegerField(label='max_price', required=False)
    cantitate = forms.IntegerField(label='cantitate', required=False)

    def clean_min_price(self):
        min_price = self.cleaned_data.get('min_price')
        if min_price is not None and min_price < 0:
            raise forms.ValidationError("Pretul minim trebuie sa fie o valoare pozitiva.")
        return min_price
    
    def clean_max_price(self):
        max_price = self.cleaned_data.get('max_price')
        if max_price is not None and max_price < 0:
            raise forms.ValidationError("Pretul maxim trebuie sa fie o valoare pozitiva.")
        return max_price
    
    def clean_cantitate(self):
        cantitate = self.cleaned_data.get('cantitate')
        if cantitate is not None and cantitate < 0:
            raise forms.ValidationError("Cantitatea trebuie sa fie o valoare pozitiva.")
        return cantitate

# class ComandaForm(forms.ModelForm):
#     class Meta:
#         model = Comanda
#         fields = ['nume', 'prenume', 'telefon', 'metoda_livrare', 'adresa_livrare', 'locatie_livrare', 'metoda_plata']
#         widgets = {
#             'metoda_livrare': forms.Select(attrs={
#                 'class': 'styled-select'
#             }),
#             'metoda_plata': forms.Select(attrs={
#                 'class': 'styled-select'
#             }),
#             'adresa_livrare': forms.TextInput(attrs={
#                 'class': 'styled-input',
#                 'placeholder': 'Introdu adresa'
#             }),
#             'locatie_livrare': forms.Select(attrs={
#                 'class': 'styled-select'
#             })
#         }
#         help_text = {
#             'telefon': 'ex: 0712345678'
#         }
        
#     metoda_livrare = forms.ChoiceField(choices=[('', 'select')] + Comanda.LIVRARE_CHOICES, widget=forms.Select(attrs={'class': 'styled-select'}))
#     metoda_plata = forms.ChoiceField(choices=[('', 'select')] + Comanda.PLATA_CHOICES, widget=forms.Select(attrs={'class': 'styled-select'}))
        
#     nume = forms.CharField(validators=[validate_names], widget=forms.TextInput(attrs={
#                 'class': 'styled-input',
#                 'placeholder': 'Introdu numele'
#             }))
#     prenume = forms.CharField(validators=[validate_names], widget=forms.TextInput(attrs={
#                 'class': 'styled-input',
#                 'placeholder': 'Introdu prenumele'
#             }))
#     telefon = forms.CharField(validators=[validate_phonenumber], widget=forms.TextInput(attrs={
#                 'class': 'styled-input',
#                 'placeholder': 'Introdu telefon'
#             }))
    
#     PLATA_CHOICES = [
#         ('numerar', 'Numerar'),
#         ('card', 'Card Online'),
#     ]
#     bauturi = forms.ModelMultipleChoiceField(queryset=Bautura.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'styled-select'}), required=False)
#     deserturi = forms.ModelMultipleChoiceField(queryset=Desert.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'styled-select',}), required=False)
    
#     micdejuns = forms.ModelMultipleChoiceField(queryset=Mancare.objects.all(), widget=forms.NumberInput(attrs={'class': 'styled-cb', 'placeholder': '0', 'min': '0'}), required=False)
#     MARIME_CHOICES = [
#         ('regular', 'Regular'),
#         ('large', 'Large'),
#     ]
#     marime_micdejuns = forms.ChoiceField(choices=MARIME_CHOICES, widget=forms.Select(attrs={'class': 'styled-selectMarime'}), required=False)
    
#     bacsis = forms.BooleanField(label="bacsis", widget=forms.CheckboxInput(attrs={'class': 'styled-checkbox'}), required=False)
#     bacsisSuma = forms.IntegerField(label="bacsisSuma", required=False, help_text='bacsisul nu este inclus in totalul afisat', widget=forms.NumberInput(attrs={'class': 'styled-inputBacsis', 'placeholder': 'Introdu suma'}))
#     confimare = forms.BooleanField(label='confirmare', required=False, widget=forms.CheckboxInput(attrs={
#                 'class': 'styled-checkbox'
#             }))

#     def clean_confirmare(self):
#         data = self.cleaned_data["confirmare"]
        
#         if data is False:
#             raise forms.ValidationError("Trebuie sa confirmati comanda.")
        
#         return data
    

#     def clean(self):
#         cleaned_data = super().clean()
#         bacsis = cleaned_data.get('bacsis')
#         bacsisSuma = cleaned_data.get('bacsisSuma')
        
#         if bacsis == True and not bacsisSuma:
#             raise ValidationError("Este necesara adaugarea sumei de bacsis.")
        
#         metoda_livrare = cleaned_data.get('metoda_livrare')
#         adresa_livrare = cleaned_data.get('adresa_livrare')
        
#         if metoda_livrare == 'livrare la domiciliu' and not adresa_livrare:
#             raise ValidationError("Este necesara completarea casutei de adresa")
        
#         return cleaned_data
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     for mic_dejun in Mancare.objects.all():
    #         self.fields[f'micdejun_{mic_dejun.id}'] = forms.IntegerField(
    #             widget=forms.NumberInput(attrs={
    #                 'class': 'styled-cb',
    #                 'placeholder': '0',
    #                 'min': '0',
    #             }),
    #             required=False
    #         )

def no_digits(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Acest camp nu poate contine cifre.")

class MicdejunForm(forms.ModelForm):
    class Meta:
        model = Mancare
        fields = ['nume', 'pret', 'cantitate', 'categorie', 'marime', 'timp_preparare', 'ingrediente_mancare', 'image']
        validators = {
            'nume': [no_digits],
            'categorie': [no_digits]
        }
        widgets = {
            'nume': forms.TextInput(attrs={'class': 'styled-input', 'placeholder': 'Introdu numele'}),
            'pret': forms.NumberInput(attrs={'class': 'styled-input', 'placeholder': 'Introdu pretul'}),
            'cantitate': forms.NumberInput(attrs={'class': 'styled-input', 'placeholder': 'Introdu cantitatea'}),
            'timp_preparare': forms.NumberInput(attrs={'class': 'styled-inputTimp'}),
            'categorie': forms.TextInput(attrs={'class': 'styled-input', 'placeholder': 'Introdu categoria'}),
            'marime': forms.Select(attrs={'class': 'styled-selectMarime'}),
            'ingrediente_mancare': forms.CheckboxSelectMultiple(attrs={'class': 'styled-ingrediente'}),
        }
        error_messages = {
            'ingrediente_mancare': {
                'required': 'Este necesara alegerea ingredientelor.',
            },
        }
    default_marime = forms.BooleanField(label='Setare marime = default', required=False, widget=forms.CheckboxInput(attrs={'class': 'styled-cb'}), help_text="(daca nu e bifata casuta, se va considera marimea default regular)")
    marime = forms.ChoiceField(choices=[('', 'Select')] + Mancare.marime_choices, widget=forms.Select(attrs={'class': 'styled-selectMarime'}), required=False)
    
    add_timp_preparare = forms.BooleanField(label='Adaugare timp preparare', required=False, widget=forms.CheckboxInput(attrs={'class': 'styled-cb'}), help_text="(daca nu e bifata casuta, se va considera timpul default 8 min)")
    timp_preparare = forms.IntegerField(label='Timp preparare', required=False, widget=forms.NumberInput(attrs={'class': 'styled-inputTimp', 'placeholder': '-'}))
    
    def clean_nume(self):
        data = self.cleaned_data["nume"]
        
        if data != data.capitalize():
            raise ValidationError("Numele trebuie sa inceapa cu litera mare.")
        for ch in data:
            if not ch.isalpha() and not ch.isspace():
                raise ValidationError("Numele poate contine doar litere si spatii.")
        if len(data) < 3:
            raise ValidationError("Numele trebuie sa aiba cel putin 3 caractere.")

        return data

    def clean_pret(self):
        data = self.cleaned_data["pret"]
        
        if data < 8:
            raise ValidationError("Prețul trebuie să fie mai mare decât 8.")
        if data > 300:
            raise ValidationError("Prețul nu poate depăși 300.")
        if data != round(data, 2):
            raise ValidationError("Prețul trebuie să aibă maxim 2 zecimale.")

        return data
    
    def clean_cantitate(self):
        data = self.cleaned_data["cantitate"]
        
        if data == 0:
            raise ValidationError("Cantitatea nu poate fi 0.")
        if data > 500:
            raise ValidationError("Cantitatea nu poate depăși 500g.")
        if data < 30:
            raise ValidationError("Cantitatea trebuie să fie de minim 30g.")

        return data
    
    def clean_categorie(self):
        data = self.cleaned_data["categorie"]
        
        if data is not None:
            if len(data) < 3:
                raise ValidationError("Categoria trebuie sa aiba cel putin 3 caractere.")
            if data != data.capitalize():
                raise ValidationError("Categoria trebuie sa inceapa cu litera mare.")
            if not data.isalpha():
                raise ValidationError("Categoria poate conține doar litere.")
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        
        default_marime = cleaned_data.get('default_marime', '')
        marime = cleaned_data.get('marime', '')
        if default_marime and not marime:
            raise ValidationError("Este necesara specificarea marimii portiei.")
        
        add_timp_preparare = cleaned_data.get('add_timp_preparare', '')
        timp_preparare = cleaned_data.get('timp_preparare', '')
        if add_timp_preparare and not timp_preparare:
            raise ValidationError("Este necesara specificarea tipului de preparare.")
        
        return cleaned_data


# laborator6
class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 10:
            raise forms.ValidationError("Parola trebuie sa aiba macar 10 caractere.")
        return password1

class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat',
        widget=forms.CheckboxInput(attrs={'class':'styled-choicefield'})
    )

    def clean(self):
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data

def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "gen", "telefon", "adresa", "datanasterii", "locatie_fav", "password1", "password2")
        widgets = {
            'adresa': forms.Textarea(attrs={
                'class': 'styled-textare'
            }),
            'locatie_fav': forms.Select(attrs={
                'class': 'styled-class'
            })
        }  

    gen = forms.ChoiceField(choices=CustomUser.gen_choices, widget=forms.Select(attrs={'class': 'styled-class'}))
    telefon = forms.CharField(validators=[validate_phonenumber])
    datanasterii =forms.DateField(widget=forms.DateInput(attrs={'class': 'styled-class', 'type': 'date'}))
    
    def clean_adresa(self):
        adresa = self.cleaned_data.get('adresa')
        if len(adresa) < 10:
            raise ValidationError('Adresa trebuie să conțină minimum 10 caractere')
        if not any(char.isdigit() for char in adresa):
            raise ValidationError('Adresa trebuie să conțină cel puțin un număr')
        if 'str' not in adresa.lower() and 'strada' not in adresa.lower() and 'bd.' not in adresa.lower() and 'stradă' not in adresa.lower() and 'b-dul' not in adresa.lower() and 'bulevardul' not in adresa.lower():
            raise ValidationError('Adresa trebuie să conțină strada sau bulevardul.')

        return adresa

    def clean_datanasterii(self):
        datanasterii = self.cleaned_data["datanasterii"]
        
        if datanasterii is not None:
            current_date = datetime.now().date()
            varsta = int((current_date - datanasterii).days / 365.25)
        
        if datanasterii is not None and varsta < 16 :
            raise forms.ValidationError('Expeditorul trebuie sa aiba peste 16 ani.')
        
        return datanasterii

    def save(self, commit=True):
        user = super().save(commit=False)
        
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.gen = self.cleaned_data["gen"]
        user.telefon = self.cleaned_data["telefon"]
        user.adresa = self.cleaned_data["adresa"]
        user.datanasterii = self.cleaned_data["datanasterii"]
        user.locatie_fav = self.cleaned_data["locatie_fav"]
        user.cod = generate_random_string(length=15)  # Cod unic generat automat
        user.email_confirmat = False

        if commit:
            trimite_mail(user.last_name, user.first_name, user.username, user.cod, user.email)
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 10:
            raise forms.ValidationError("Parola trebuie sa aiba macar 10 caractere.")
        return password1


# laborator7
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

def trimite_mail(nume, prenume, username, cod, email):
    obj_site = Site.objects.get_current()
    domeniu = obj_site.domain
    context = {'nume': nume, 'prenume': prenume, 'username': username, 'cod': cod, 'url_imagine' : f"http://127.0.0.1:8000/static/images/logo-flavor.png", 'url': f"http://{domeniu}/confirma_mail/{cod}"}
    html_content = render_to_string('emailtemplate.html', context)

    email = EmailMessage(
        subject='Bun venit pe site-ul nostru!',
        body=html_content,
        from_email='flavorcalifornia@gmail.com',
        to=['flavorcalifornia@gmail.com'
            #email
            ],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)

from .models import Promotii
class PromotieForm(forms.ModelForm):
    class Meta:
        model = Promotii
        fields = ['nume', 'data_creare', 'data_expirare', 'reducere', 'tip_promotie']
        widgets = {
            'tip_promotie': forms.Select(attrs={'class': 'styled-select'}),
            'data_creare': forms.DateInput(attrs={'class': 'styled-date', 'type': 'date'}),
            'data_expirare': forms.DateInput(attrs={'class': 'styled-date', 'type': 'date'}),
        }
        
    subiect = forms.CharField(validators=[validate_initcap], label='Subiect', required=True, widget=forms.TextInput(attrs={'class': 'styled-input','placeholder': 'Introdu subiectul'}))
    mesaj = forms.CharField(widget=forms.Textarea(attrs={'class': 'styled-textare', 'rows': 5, 'cols': 40, 'placeholder': 'Scrie un mesaj corespunzator'}), label='Mesaj', required=True)

    mancare_choices = [
        ('toast', 'Toast'),
        ('eggs', 'Eggs'),
        ('sandwiches', 'Sandwiches')
    ]
    mancare = forms.MultipleChoiceField(
        choices=mancare_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'styled-checkbox'}),
        initial=[choice[0] for choice in mancare_choices],
        label='Mancare',
        required=False
    )
    bautura_choices = [
        ('juice', 'Juice'),
        ('coffee', 'Coffee')
    ]
    bautura = forms.MultipleChoiceField(
        choices=bautura_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'styled-checkbox'}),
        initial=[choice[0] for choice in bautura_choices],
        label='Bautura',
        required=False
    )
    desert_choices = [
        ('fursecuri', 'Fursecuri'),
        ('cu fructe', 'Cu fructe')
    ]
    desert = forms.MultipleChoiceField(
        choices=desert_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'styled-checkbox'}),
        initial=[choice[0] for choice in desert_choices],
        label='Desert',
        required=False
    )


# laborator9
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', "first_name", "last_name", 'email', 'is_staff', 'is_active', 'groups', 'user_permissions',  "gen", "telefon", "adresa", "datanasterii", "locatie_fav", "blocat"]

    # for user in CustomUser.objects.all(): 
    #     if user.groups.filter(name='Moderatori').exists():
    #         user.is_staff = True

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
    
        # if self.current_user and self.current_user.groups.filter(name='Moderatori').exists():
        #     self.fields['email'].widget.attrs['readonly'] = True
        #     self.fields['first_name'].widget.attrs['readonly'] = True
        #     self.fields['last_name'].widget.attrs['readonly'] = True
        #     self.fields['blocat'].widget.attrs['readonly'] = True



# model

class ElevForm(forms.ModelForm):
    class Meta:
        model= Elev
        fields = ['nume', 'prenume', 'datanasterii']
    
    def clean_nume(self):
        nume = self.cleaned_data.get('nume')
        validate_names(nume)
        return nume

    def clean_prenume(self):
        prenume = self.cleaned_data.get('prenume')
        if prenume and prenume != prenume.capitalize():
            raise ValidationError('Prenumele trebuie sa inceapa cu litera mare.')
        return prenume
    
    def clean(self):
        cleaned_data = super().clean()
        
        nume = cleaned_data.get('nume')
        prenume = cleaned_data.get('prenume')
        if nume == prenume:
            raise ValidationError('Numele si prenumele nu pot fi identice.')
        
        return cleaned_data
    

# examen
from .models import Curs
class CursForm(forms.ModelForm):
    class Meta:
        model = Curs
        fields = ['denumire', 'numar_credite', 'student']
        widgets = {
            'denumire': forms.TextInput(attrs={'class': 'styled-input', 'placeholder': 'Introdu numele'}),
            'numar_credite': forms.NumberInput(attrs={'class': 'styled-textare', 'placeholder': 'Introdu nr. de credite'}),
            'student': forms.Select(attrs={'class': 'styled-select'}),
        }
        
    def clean_numar_credite(self):
        data = self.cleaned_data["numar_credite"]
        
        if data < 1 or data > 10:
            raise ValidationError("Numarul de credite trebuie sa fie intre 1 si 10.")
        
        credite = Curs.objects.filter(numar_credite=data)
        if credite:
            raise ValidationError("Exista deja un curs cu acest numar de credite.")
        
        return data
    