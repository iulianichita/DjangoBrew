from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import Prajitura, Mancare, Bautura, Desert, Locatie, CustomUser, Comanda, ComandaDetaliu
from django.db.models import Q
from .forms import ContactForm, MancareForm, MicdejunForm, CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from time import time
import re, json

import logging
logger = logging.getLogger('django')

# laborator1
def index(request):
	return HttpResponse("primul raspuns")
def pag1(request):
    return HttpResponse(2+3)
l=[]
def pag2(request):
    global l
    a=request.GET.get("a",10)
    print(request.GET)
    l.append(a)
    return HttpResponse(f"<b>Am primit</b>: {l}")
def mesaj(request):
    return HttpResponse("Buna ziua!")
def data(request):
    data_curenta = datetime.now()
    data_curenta_scurta = data_curenta.date()
    #return HttpResponse(data_curenta_scurta)
    
    my_date = datetime(1996, 12, 30)
    my_date = my_date.date()

    return HttpResponse(int((data_curenta_scurta - my_date).days / 365.25))
v=[]
def nr_accesari(request):
    v.append(1)
    return HttpResponse(f"Nr. de accesari din sesiunea curenta este : {len(v)}")
def suma(request):
    a=request.GET.get("a", 0)
    b=request.GET.get("b", 0)
    
    rez=int(a)+int(b)
    
    return HttpResponse(f"Suma lui {a} si {b} este {rez}")
cuvinte=[]
def text(request):
    ok=0
    t=request.GET.get("t", "")
    
    for i in t:
        if not i.isalpha():
            ok += 1 
            break

    if ok==0:
        cuvinte.append(t+" ")
        return HttpResponse(cuvinte)
        
    
    return HttpResponse("textul poate contine doar litere")
def nr_parametri(request):
    nr_parametri = len(request.GET)
    
    return HttpResponse(f"Am primit {nr_parametri} parametri.")
def operatie(request):
    a=request.GET.get("a", 0)
    b=request.GET.get("b", 0)
    op=request.GET.get("op")
    
    if not a.isnumeric() or not b.isnumeric():
        return HttpResponse("Parametrii primiti nu sunt numerici.")
    
    a=int(a)
    b=int(b)
    if op=='sum':
        rez=a+b
    elif op=='dif':
        rez=a-b
    elif op=='mul':
        rez=a*b
    elif op=='div':
        rez=a/b
    elif op=='mod':
        rez=a%b
    else:
        return HttpResponse("Operatia specificata nu e valida.")
    
    return HttpResponse(f'Suma numerelor {a} si {b} este {rez}.')
def tabel(request):
    matrice = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4]
    ]
    
    html = '<h1>Matrice 3x4</h1>'
    html += "<table border='1'>"
    
    for i in matrice:
        html += "<tr>"
        for el in i:
            html += f"<td style='padding: 10px; text-align: center;'>{el}</td>"
        html += "<tr>"
            
    html += "</table>"
    
    return HttpResponse(html)
def lista(request):
    lst=["mere", "pere", "cirese", "portocale", "banane"]
    
    cuvinte_parametru = request.GET.get("cuvinte", "")
    if len(request.GET)==0:
        html = "<h2>Lista de cuvinte</h2>"
        html += "<ul>"
        
        for cuvant in lst:
            html += f"<li> {cuvant} </li>"
                
        html += "</ul>"
        return HttpResponse(html)
    
    cuvinte_marcate = cuvinte_parametru.split(",") if cuvinte_parametru else []
    
    
    for i in cuvinte_marcate:
        if i not in lst:
            return HttpResponse("Cuvant invalid")
    
    html = "<h2>Lista de cuvinte</h2>"
    html += "<ul>"
    
    for cuvant in lst:
        if cuvant in cuvinte_marcate:
            html += f"<li style='color: red;'> {cuvant} </li>"
        else:
            if cuvant in lst:
                html += f"<li> {cuvant} </li>"
            
    html += "</ul>"
    
    return HttpResponse(html)
d={}
def elev(request):
    nume=request.GET.get("nume")
    prenume=request.GET.get("prenume")
    clasa=request.GET.get("clasa")
    
    if not nume or not prenume or not clasa:
        return HttpResponse("Te rog sa furnizezi numele, prenume si clasa")
    
    nume_complet=nume+" "+prenume
    
    if clasa not in d:
        d[clasa]=[nume_complet]
    else:   
        d[clasa].append(nume_complet)
    
    html = "<h3>Elevii pe clase:</h3>"
    for clasa, elevi in d.items():
        html += f"<h4>Clasa {clasa}</h4>"
        html += "<ul>"
        for elev in elevi:
            html += f"<li>{elev}</li>"
        html += "</ul>"
    
    return HttpResponse(html)
def afisare_pag(request):
    return HttpResponse("Am raspuns")
def afis_cod(request,id):
    return HttpResponse(f"<b>Am primit codul:</b> {id}")

# laborator2
nr_cereri=[]
def aduna_numere(request, sir):
    nr_cereri.append(1)
    
    # nr=0
    # for i in sir:
    #     if i.isdigit():
    #         i = int(i)
    #         nr = nr*10 + i
            
    nr = re.search(r'\d+(?=[^\d]*)$', sir)
    nr = int(nr.group())
    
    if 'total' not in request.session:
        request.session['total'] = 0

    request.session['total'] += nr
    
    return HttpResponse(f"numar cereri : { len(nr_cereri) }, suma numere: {request.session['total']}")
def afiseaza_liste(request):
    a=request.GET.getlist('a')
    b=request.GET.getlist('b')
    
    html = "<b>a:</b>"
    html += "<ul>"
    
    for i in a:
        html += f"<li>{i}</li>"
    
    html += "</ul>"
    
    html += "<b>b:</b>"
    html += "<ul>"
    
    for i in b:
        html += f"<li>{i}</li>"
    
    html += "</ul>"
    
    return HttpResponse(html)
nr_nume=[]
def numara_nume(request,prenume,nume):
    nume_complet = f"{prenume} {nume}"
    nr_nume.append(nume_complet)
    return HttpResponse(f'Numărul de nume primite: {len(nr_nume)}')
def cauta_subsir(request,subsir):
    return HttpResponse(len(subsir))
def afis_template(request):
    d={
            "lista":[
                {
                    "a":10,
                    "b":20,
                    "operatie":"suma"
                },
                {
                    "a":40,
                    "b":20,
                    "operatie":"diferenta"
                },
                {
                    "a":25,
                    "b":30,
                    "operatie":"suma"
                },
                {
                    "a":40,
                    "b":30,
                    "operatie":"diferenta"
                },
                {
                    "a":100,
                    "b":50,
                    "operatie":"diferenta"
                }
            ]
    }
    
    for element in d["lista"]:
        if element["operatie"] == "suma":
            element["rezultat"] = element["a"] + element["b"]
        elif element["operatie"] == "diferenta":
            element["rezultat"] = element["a"] - element["b"]
    
    
    return render(request,"index.html", d)

# laborator3
def afisare_prajituri(request):
    return render(request, 'afisare.html',
            {
                "prajituri": Prajitura.objects.filter(gramaj__lte = 60)
            }
    )

# laborator4
def afisare_main(request):
    messages.info(request, "Bun venit! ")
    messages.success(request, "Te afli acum pe pagina principala. ")

    logger.debug('a fost accesata pagina de main')
    logger.info('s-a incarcat pagina de main')
    
    username = request.session.get('username', '')
    return render( request, 'main.html', {'username': username})

def meniu(request):
    return render( request, 'meniu.html')

# laborator5
def micdejun(request, no_page):
    username = request.session.get('username', '')
    
    no_page = int(no_page)
    nrelem = no_page * 8

    if no_page == 1:
        prev = 0
    else:
        prev = no_page - 1

    nume = min_price = max_price = cantitate = None
    
    obiecte = Mancare.objects.all()
    total_produse = obiecte.count()

    if request.method == 'POST':
        form = MancareForm(request.POST)
        if form.is_valid():
            nume = form.cleaned_data['nume']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            cantitate = form.cleaned_data['cantitate']
            print(f"nume: {nume}, min_price: {min_price}, max_price: {max_price}, cantitate: {cantitate}")
            messages.debug(request, "Debug: datele au fost primite.")
            messages.success(request, "Acestea sunt rezultatele filtrarii. ")
    else:
        form = MancareForm()

    if nume == 'toast':
        obiecte = obiecte.filter(Q(nume__exact='Avocado toast') | Q(nume__exact='Banana toast'))
    elif nume == 'sandwiches':
        obiecte = obiecte.filter(Q(nume__exact='Sandvisuri') | Q(nume__exact='Sandvisuri cu ou'))
    elif nume == 'eggs':
        obiecte = obiecte.filter(
            Q(nume__exact='Egg benedict') | Q(nume__exact='Sandvisuri cu ou') | Q(nume__exact='Egg speciality')
        )

    if cantitate:
        obiecte = obiecte.filter(cantitate__lte=cantitate)

    if not min_price and max_price:
        obiecte = obiecte.filter(pret__lte=max_price)[nrelem-8:nrelem]
    elif min_price and max_price:
        obiecte = obiecte.filter(pret__gte=min_price, pret__lte=max_price)[nrelem-8:nrelem]
    else:
        obiecte = obiecte[nrelem-8:nrelem]

    total_pagini = (total_produse // 8) + (1 if total_produse % 8 != 0 else 0)

    if no_page == total_pagini:
        next = 0
    else:
        next = no_page + 1
    if total_pagini == 0:
        prev = 0
        next = 0
    is_empty = not obiecte.exists()
    
    if is_empty:
        messages.warning(request, "Warning: niciun produs gasit pentru datele de filtrare.")

    return render(request, 'micdejun.html', {
        'obiecte': obiecte,
        'prev': prev, 'next': next,
        'no_page': no_page,
        'total_pagini': total_pagini,
        'is_empty': is_empty,
        'form': form,
        'username': username
    })

def bauturi(request, no_page):
    
    no_page = int (no_page)
    nrelem = no_page*6
    
    if no_page == 1:
        prev = 0
    else:
        prev = no_page - 1
    
    obiecte = Bautura.objects.all()
    
    max_price = request.GET.get('max_price')
    nume = request.GET.get('nume')
    agree = request.GET.get('agree')
    
    if nume == 'green-drinks':
        obiecte = obiecte.filter(Q(nume__exact = 'Go green') | Q(nume__exact = 'Suc de portocale')| Q(nume__exact = 'Mango&Matcha'))
    elif nume == 'cafea':
        obiecte = obiecte.filter(
            Q(nume__exact="Espresso") | 
            Q(nume__exact="Double espresso") | 
            Q(nume__exact="Macchiato") | 
            Q(nume__exact="Capuccino") | 
            Q(nume__exact="Flat white") | 
            Q(nume__exact="Latte") | 
            Q(nume__exact="Matcha iced latte") | 
            Q(nume__exact="Cold brew") | 
            Q(nume__exact="Mango&matcha")
        )

        
    if agree:
        obiecte = obiecte.filter(disponibila__exact = 'True')
    
    if max_price:
        obiecte = obiecte.filter(pret__lte = max_price)[nrelem-6:nrelem]
        total_produse = obiecte.count()
    else:
        total_produse = obiecte.count()
        obiecte = obiecte[nrelem-6:nrelem]
    
    total_pagini = (total_produse // 6) + (1 if total_produse % 6 != 0 else 0)
    
    if no_page == total_pagini:
        next = 0
    else:
        next = no_page + 1
        
    if total_pagini == 0:
        prev = 0
        next = 0
        
    is_empty = not obiecte.exists()
    
    return render( request, 'bauturi.html',{'obiecte': obiecte, 'prev': prev, 'next': next, 'no_page': no_page, 'total_pagini': total_pagini, 'is_empty': is_empty})

def desert(request, no_page):
    
    no_page = int (no_page)
    nrelem = no_page*6
    
    if no_page == 1:
        prev = 0
    else:
        prev = no_page - 1
    
    obiecte = Desert.objects.all()
    
    max_price = request.GET.get('max_price')
    nume = request.GET.get('nume')
    gramaj = request.GET.get('gramaj')
    
    if nume == 'cu fructe':
        obiecte = obiecte.filter(Q(nume__exact = 'Tarta cu fructe') | Q(nume__exact = 'Tarta cu zmeura') | Q(nume__exact = 'Placinta cu mere'))
        
    if gramaj:
        obiecte = obiecte.filter(cantitate__lte=gramaj)
    
    if max_price:
        obiecte = obiecte.filter(pret__lte = max_price)[nrelem-6:nrelem]
        total_produse = obiecte.count()
    else:
        total_produse = obiecte.count()
        obiecte = obiecte[nrelem-6:nrelem]
    
    total_pagini = (total_produse // 6) + (1 if total_produse % 6 != 0 else 0)
    #pagini=range(1,total_pagini+1)
    
    if no_page == total_pagini:
        next = 0
    else:
        next = no_page + 1
        
    if total_pagini == 0:
        prev = 0
        next = 0
        
    is_empty = not obiecte.exists()
    
    return render( request, 'desert.html',{'obiecte': obiecte, 'prev': prev, 'next': next, 'no_page': no_page, 'total_pagini': total_pagini, 'is_empty': is_empty} )

def aboutus(request):
    messages.info(request, "Te afli acum pe pagina de about us! ")
    
    username = request.session.get('username', '')
    obiecte = Locatie.objects.all()
    return render( request, 'aboutus.html',{'obiecte': obiecte, 'username': username} )

def contactform_trimis(request):
    messages.debug(request, "Debug: dstele au fost procesate cu succes.")
    username = request.session.get('username', '')
    return render(request, 'thankscontactform.html', {'username': username})

def contact_view(request):
    username = request.session.get('username', '')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            save_message(form.cleaned_data)
            return redirect('contactform_trimis')
        else:
            print(form.errors)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'username': username})

def save_message(cleaned_data):
    cleaned_data.pop("confirm_email", None)
    
    if 'datanasterii' in cleaned_data and cleaned_data['datanasterii']:
        cleaned_data['datanasterii'] = cleaned_data['datanasterii'].strftime('%Y-%m-%d')
    
    timestamp = int(time())

    with open(f"mesaje/mesaj_{timestamp}.json", "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


def add_micdejun(request):
    
    # laborator8
    produs =  ContentType.objects.get_for_model(Mancare)

    if not request.user.has_perm('aplicatie_ex.add_mancare'):
        return HttpResponseForbidden(render(request, '403.html', {'titlu': 'Eroare adaugare produse', 'mesaj_personalizat': f'Nu ai voie să adaugi in modelul {produs}', 'username': request.user.username}))
    if request.method == 'POST':
        form = MicdejunForm(request.POST, request.FILES)
        if form.is_valid():
            micdejun = form.save(commit=False)
            
            if not form.cleaned_data.get('add_timp_preparare', False):
                micdejun.timp_preparare = 8

            if not form.cleaned_data.get('default_marime', False): 
                micdejun.marime = 'regular'
                
            print(form.cleaned_data.get('ingrediente_mancare'))    
            micdejun.save()
            form.save_m2m()


            return redirect('afisare_main')
        else:
            print(form.errors)
    else:
        form = MicdejunForm()
    return render(request, 'add_micdejun.html', {'form': form, 'username': request.user.username})

# def plasare_comanda(request):
#     username = request.session.get('username', '')
#     desert = Desert.objects.all()
#     bautura = Bautura.objects.all()
#     micdejun = Mancare.objects.all()
    
#     if request.method == 'POST':
#         form = ComandaForm(request.POST)
#         if form.is_valid():
#             comanda = form.save(commit=False)
            
#             nume = form.cleaned_data['nume']
#             prenume = form.cleaned_data['prenume']
#             telefon = form.cleaned_data['telefon']
#             metoda_plata = form.cleaned_data['metoda_plata']
#             metoda_livrare = form.cleaned_data['metoda_livrare']
#             adresa_livrare = form.cleaned_data['adresa_livrare']
#             bacsisSuma = form.cleaned_data['bacsisSuma']
#             confirmare = form.cleaned_data['confirmare']
            
#             comanda.total = comanda.calculate_total() + bacsisSuma
            
#             if confirmare:
#                 comanda.status = 'confirmata'
#             else:
#                 comanda.status = 'anulata'
            
            
#             print(f"nume: {nume}, prenume: {prenume}, telefon: {telefon}, metoda_plata: {metoda_plata}, metoda_livrare: {metoda_livrare}, adresa_livrare: {adresa_livrare}")
            
#             comanda.save()

#             return redirect('afisare_main')
#     else:
#         form = ComandaForm()

#     return render(request, 'ordernow.html', {'form': form, 'micdejun': micdejun, 'desert': desert, 'bautura': bautura, 'username': username})

# laborator6
def loginpage(request):
    username = request.session.get('username', '')
    first_name = request.session.get('first_name', '')
    last_name = request.session.get('last_name', '')
    email = request.session.get('email', '')
    email_confirmat = request.session.get('email_confirmat', '')
    datanasterii = request.session.get('datanasterii', '')
    adresa = request.session.get('adresa', '')
    telefon = request.session.get('telefon', '')
    gen = request.session.get('gen', '')
    
    if gen == 'M':
        gen = 'masculin'
    elif gen == 'F':
        gen = 'feminin'
    
    return render(request, 'login_page.html', {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'email_confirmat': email_confirmat,
        'datanasterii': datanasterii,
        'adresa': adresa,
        'telefon': telefon,
        'gen': gen
    })

from django.core.exceptions import ObjectDoesNotExist

def logout_view(request):
    logout(request)
    request.session.clear()
    
    try:
        permission = Permission.objects.get(codename='vizualizare_oferta')
        permission.delete()
        print("Permisiunea a fost stearsa")
    except ObjectDoesNotExist:
        print("Permisiunea 'vizualizare_oferta' nu a fost găsită")

    return redirect('afisare_main')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.core.mail import mail_admins

# laborator7
from datetime import timedelta

def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] 
    else:
        ip = request.META.get('REMOTE_ADDR') 
    return ip

def custom_login_view(request):
    logger.debug('este accesata pagina de login')
    logger.info('a fost accesata pagina de login')
    if 'logari_istoric' not in request.session:
        request.session['logari_istoric'] = []

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        try:
            if request.POST.get('username') == 'admin':
                logger.error('cineva incearca sa se conecteze cu user-ul admin')
                logger.critical('cineva incearca sa se conecteze cu user-ul admin')
                
                messages.error(request, "Error: nu va puteti conecta cu user-ul admin.")
                raise Exception("Login cu user-ul admin")
            
            acum = datetime.now()
            logari_istoric = [
                datetime.strptime(logare, "%Y-%m-%d %H:%M:%S")
                for logare in request.session['logari_istoric']
            ]
            logari_istoric = [logare for logare in logari_istoric if acum - logare <= timedelta(minutes=2)]
            
            logari_istoric.append(acum)
            request.session['logari_istoric'] = [logare.strftime("%Y-%m-%d %H:%M:%S") for logare in logari_istoric]
            
            print(request.session['logari_istoric'])

            if len(logari_istoric) == 3:
                logger.error('un user a avut mai mult de 3 logari esuate in mai putin de 2 minute')
                logger.critical('un user a avut mai mult de 3 logari esuate in mai putin de 2 minute')
                
                messages.error(request, "Error: prea multe incercari esuate.")
                raise Exception("Prea multe logari esuate in mai putin de 2 minute")
            
            if form.is_valid():
                user = form.get_user()
                if not user.email_confirmat:
                    email_confirmation_message = 'Email-ul dumneavoastra necesita confirmare. Verificati-va mail-ul.'
                    messages.warning(request, "Warning: Email-ul dumneavoastra necesita confirmare. Verificati-va mail-ul.")
                    logger.warning('cineva incearca sa se conecteze inainte sa isi fi confirmat mail-ul')
                    return render(request, 'login.html', {'form': form, 'email_confirmation_message': email_confirmation_message})
                
                request.session['logari_istoric'] = []
                if user.blocat == True:
                    email_confirmation_message = 'Ne pare rau, contul dumneavoastra este blocat.'
                    return render(request, 'login.html', {'form': form, 'email_confirmation_message': email_confirmation_message})
                login(request, user)
                
                request.session['username'] = user.username
                request.session['cod'] = user.cod
                request.session['email_confirmat'] = user.email_confirmat
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.email
                request.session['datanasterii'] = str(user.datanasterii)
                request.session['adresa'] = user.adresa
                request.session['telefon'] = user.telefon
                request.session['gen'] = user.gen
                
                if not form.cleaned_data.get('ramane_logat'):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(24*60*60)

                return redirect('loginpage')
                    

        except Exception as e:
            print (e)
            ip_address = get_client_ip(request)
            if str(e) == "Prea multe logari esuate in mai putin de 2 minute":
                mail_admins(
                    subject='Logari suspecte',
                    message=f"Au fost detectate logari esuate.\n"
                            f"IP: {ip_address}",
                    html_message=render_to_string('email_admin.html', {
                        'subiect': 'Logari suspecte',
                        'username': request.POST.get('username', 'necunoscut'),
                        'ip': ip_address,
                    }),
                    fail_silently=False,
                )
            if request.user.is_authenticated:
                email = request.user.email
            else:
                email = None
            if str(e) == "Login cu user-ul admin":
                mail_admins(
                    subject='Logari suspecte',
                    message=f"Cineva incearca sa ne preia site-ul.\n",
                    html_message=render_to_string('email_admin.html', {
                        'subiect': 'Cineva incearca sa ne preia site-ul',
                        'email': email
                    }),
                    fail_silently=False,
                )
            return render(request, 'login.html', {'form': form, 'log_error_message': 'Incercare esuata. Contactati administratorul.'})
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def change_password_view(request):
    username = request.session.get('username', '')
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Parola a fost actualizata')
            return redirect('afisare_main')
        else:
            messages.error(request, 'Exista erori.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'passwordchange.html', {'form': form, 'username': username})

#slide uri necesare lab 6: 31 (custom user), 27, 19, 21, 9+10, 13, 24+25, 37

# laborator7
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
def trimite_email():
    obj_site = Site.objects.get_current()
    domeniu = obj_site.domain
    url_imagine = f"https://{domeniu}{settings.STATIC_URL}images/logo.jpg"
    url = "https://localhost:8000/aplicatie_ex/main"
    html_message = f"""
    <html>
        <body>
            <p>Un e-mail care include o imagine:</p>
            <img src="{url_imagine}" alt="Logo">
        </body>
    </html>
    """

    # html_content = render_to_string('emailtemplate.html', {'nume': 'Florin', 'prenume': 'Calin', 'username': 'florincalin', 'url_imagine': url_imagine, 'url': url})
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message=html_message,
        from_email='flavorcalifornia@gmail.com',
        recipient_list=['flavorcalifornia@gmail.com'],
        fail_silently=False,
    )

def index(request):
    trimite_email()
    return HttpResponse('Email trimis cu succes!')

def confirmare_mail(request, cod):
    print(f"Codul primit este: {cod}")
    users = CustomUser.objects.all()
    
    for user in users:
        if user.cod == cod:
            user.email_confirmat = True
            user.save()
            break

    return render(request, 'confirmare_mail.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from .models import Vizualizari

@csrf_exempt
def add_vizualizare(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            product_type = data.get('product_type')

            if product_type == 'mancare':
                content_type = ContentType.objects.get_for_model(Mancare)
            elif product_type == 'bautura':
                content_type = ContentType.objects.get_for_model(Bautura)
            elif product_type == 'desert':
                content_type = ContentType.objects.get_for_model(Desert)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid product type'})

            Vizualizari.objects.create(
                id_user=request.user,
                content_type=content_type,
                object_id=product_id,
                datavizualizare=datetime.now()
            )
            clean_vizualizari()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'User not authenticated or invalid request method'})

def clean_vizualizari():
    vizualizari = Vizualizari.objects.all().order_by('datavizualizare')
    for v in vizualizari:
        vizualizari_user = Vizualizari.objects.filter(id_user=v.id_user).order_by('datavizualizare')
        if vizualizari_user.count() > 6:
            for viz in vizualizari_user[:vizualizari_user.count() - 6]:
                viz.delete()

from .forms import PromotieForm
from django.core.mail import send_mass_mail
from django.db.models import Count

def addPromotie(request):
    username = request.session.get('username', '')
    
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            promotie = form.save()
            categorii_mancare = form.cleaned_data['mancare']
            categorii_bautura = form.cleaned_data['bautura']
            categorii_desert = form.cleaned_data['desert']
            categorii = categorii_mancare + categorii_bautura + categorii_desert
            
            print(categorii)
            
            # retinem id-ul unic al tabelei ce este retinut in contentType in modelul Promotii
            MancareModelType = ContentType.objects.get_for_model(Mancare)
            BauturaModelType = ContentType.objects.get_for_model(Bautura)
            DesertModelType = ContentType.objects.get_for_model(Desert)

            subiect = form.cleaned_data['subiect']
            mesaj = form.cleaned_data['mesaj']
            data_expirare = form.cleaned_data['data_expirare']
            reducere = form.cleaned_data['reducere']
            
            email_subjects = {
                'Toast': 'Promotie la toast',
                'Eggs': 'Promotie la specialitatile noastre cu oua',
                'Sandwiches': 'Promotie la sandvisuri',
                'Juice': 'Promotie la sucurile noastre',
                'Coffee': 'Promotie la cafele',
                'Fursecuri': 'Promotie la fursecuri',
                'Cu fructe': 'Promotie la deserturile cu fructe'
            }
            users_emails = {
                'Toast': ["flavorcalifornia@gmail.com"],
                'Eggs': ["flavorcalifornia@gmail.com"],
                'Sandwiches': ["flavorcalifornia@gmail.com"],
                'Juice': ["flavorcalifornia@gmail.com"],
                'Coffee': ["flavorcalifornia@gmail.com"],
                'Fursecuri': ["flavorcalifornia@gmail.com"],
                'Cu fructe': ["flavorcalifornia@gmail.com"]
            }
            
            templates = {}
            for categorie in categorii:
                templates[categorie.capitalize()] = ''

            idContentType = None
            for categorie in categorii:
                if categorie.lower() in ['toast', 'eggs', 'sandwiches']:
                    idContentType = MancareModelType
                elif categorie.lower() in ['juice', 'coffee']:
                    idContentType = BauturaModelType
                elif categorie.lower() in ['fursecuri', 'cu fructe']:
                    idContentType = DesertModelType


                for v in Vizualizari.objects.all():
                    id_produs = v.object_id # id-ul produsului vizualizat
                    
                    id_user = v.id_user # id-ul userului care a vizualizat produsul
                    
                    c=0
                    for viz in Vizualizari.objects.all():
                        if viz.id_user == id_user and viz.object_id == id_produs:
                            c+=1
                        if c == 2:
                            break
                            
                    if c >= 2: # daca userul a vizualizat de cel putin 2 ori produsul
                    
                        user = CustomUser.objects.get(username=id_user)
                        
                        # daca produsul vizualizat este de tip mancare
                        if idContentType == MancareModelType and v.content_type_id == MancareModelType.id:
                            email_user = user.email
                            # print (email_user, user.username, id_produs)
                            
                            produs = Mancare.objects.get(id=id_produs)
                            # print(produs.nume, produs.categorie)
                            
                            #si este in categoria specificata
                            if produs.categorie is not None:
                                if categorie.lower() in produs.categorie.lower():
                                    templates[categorie.capitalize()] = f"""    {mesaj}
    Vrem sa va anuntam ca avem o nouă promoție in valoare de {reducere}% la {categorie}!
    Promoția este valabilă până pe {data_expirare}.

    Mulțumim!"""

                                    # if users_emails[categorie.capitalize()].count(email_user) == 0:
                                    #     users_emails[categorie.capitalize()].append(str(email_user))
                                    print(f"Produsul vizualizat de {user.username} este: {produs.nume}")
                                
                        # elif idContentType == BauturaModelType:
                        #     produs = Bautura.objects.get(id=id_produs)
                        # else:
                        #     produs = Desert.objects.get(id=id_produs)


            for categorie in categorii:
                if templates[categorie.capitalize()]:
                    print(f"Promotie la {categorie} pt {users_emails[categorie.capitalize()]}")


            datatuple = []
            for categorie in categorii:
                if templates[categorie.capitalize()]:
                    datatuple.append( (email_subjects[categorie.capitalize()], templates[categorie.capitalize()], "flavorcalifornia@gmail.com", users_emails[categorie.capitalize()]) )
            
            send_mass_mail(datatuple, fail_silently=False)

            return redirect('afisare_main')
        else:
            print(form.errors)
    else:
        form = PromotieForm()

    return render(request, 'promotii.html', {'form': form, 'username': username})


# laborator8
from django.contrib.auth.models import Permission
content_type = ContentType.objects.get_for_model(Mancare)

def aloca_oferta(request):
    username = request.user.username
    print(username)
    
    if request.user.has_perm('aplicatie_ex.vizualizare_oferta'):
        return render(request, 'oferta.html', {'username': username})
    
    banner_click = request.GET.get('banner_click', 'false') == 'true'

    if not banner_click:
        return render(request, '403.html', {
            'titlu': 'Eroare acces oferta',
            'mesaj_personalizat': 'Nu ai voie să vizualizezi oferta!',
            'username': username
        })
    
    content_type = ContentType.objects.get_for_model(Mancare)

    Permission.objects.create(
        codename='vizualizare_oferta',
        name='Vizualizarea ofertei la micdejun',
        content_type=content_type,
    )

    try:
        if request.user:
            permisiune = Permission.objects.get(codename='vizualizare_oferta')
            request.user.user_permissions.add(permisiune) # adaugam permisiunea user ului
            return render(request, 'oferta.html', {'username': username})
        else:
            logger.warning('Un user neautentificat a incercat sa acceseze oferta')
            raise Exception("User-ul nu este autentificat")
    except Exception as e:
        return render(request, '403.html', {'titlu': 'Eroare afisare oferta', 'mesaj_personalizat': 'Nu ai voie să vizualizezi oferta', 'username': username})


# laborator9
from django.shortcuts import get_object_or_404

def micdejun_view(request, item_id):
    print(id)
    item = get_object_or_404(Mancare, id=item_id)
    print(item.id)
    return render(request, 'micdejun_view.html', {'mancare_item': item})


from django.contrib.auth.models import Group, Permission

# moderatori_group = Group.objects.get(name='Moderatori')
# drept_block = Permission.objects.get(codename='can_change_data')
# moderatori_group.permissions.add(drept_block)


# laborator10
def cart(request):
    username = request.session.get('username', '')

    return render(request, 'cart.html', {'username': username})


# laborator11
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
def fisier_pdf(cart_products, total, user_data):
    
    print(cart_products)
    
    facturi_folder = os.path.join(settings.BASE_DIR, 'temporar-facturi', str(user_data['id']))
    
    if not os.path.exists(facturi_folder):
        os.makedirs(facturi_folder)

    timestamp = int(time())
    file_name = f"factura-{timestamp}.pdf"
    file_path = os.path.join(facturi_folder, file_name)
    
    
    facturi_folder = os.path.join(settings.BASE_DIR, 'temporar-facturi', str(user_data['id']))
    
    if not os.path.exists(facturi_folder):
        os.makedirs(facturi_folder)

    timestamp = int(time()) 
    file_name = f"factura-{timestamp}.pdf"
    file_path = os.path.join(facturi_folder, file_name)
    
    # file_path = "comanda.pdf"

    p = canvas.Canvas(file_path, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Factura Comanda")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Nume: {user_data.get('nume', 'Anonim')}")
    p.drawString(50, 680, f"Email: {user_data.get('email', 'N/A')}")
    p.drawString(50, 660, f"Contact administrator: flavorcalifornia@gmail.com")
    p.drawString(50, 640, f"Data Comenzii: {user_data.get('data_curenta', 'N/A')}")

    p.line(50, 620, 550, 620)

    p.drawString(50, 600, "Produse:")
    y = 580
    
    for product in cart_products:
        p.drawString(60, y, f"- {product['quantity']} x {product['product']} {product['price']} RON/buc")
        p.drawString(500, y, f"{product['pret_total']} RON")
        y -= 20
        
        ingrediente_linie = ", ".join([str(ingredient).split()[-1] for ingredient in product['ingrediente']])
        p.drawString(60, y, f"Ingrediente: {ingrediente_linie}")
        y -= 20
        
        p.drawString(60, y, f"Link vizualizare produs: ")
        p.setFillColorRGB(0, 0, 1) 
        y -= 20
        link = f"http://127.0.0.1:8000/aplicatie_ex/micdejun_view/{product['id']}"
        p.drawString(60, y, link)
        p.setFillColorRGB(0, 0, 0)  
        y -= 40

    p.line(50, y, 550, y)
    y -= 20
    p.drawString(50, y, f"Total Produse: {total} RON")
    
    p.save()

    return file_path


from django.core.mail import EmailMessage
def proceseaza_date(request):
    if request.method=="POST":
        try:
            data_curenta = datetime.now().date()
            user = request.user
            id = user.id
            nume_user = user.first_name + " " + user.last_name
            email_user = user.email
            
            data = json.loads(request.body.decode("utf-8"))
            products = data.get('products', [])
            total = data.get('total', 0)
            
            produs = None
            cart_products = []
            
            comanda = Comanda.objects.create(
                user=user,
                data_comenzii=datetime.now()
            )

            for product in products:
                produs = Mancare.objects.get(nume = product['name'])
                produs_ingrediente = list(produs.ingrediente_mancare.all())
                produs_id = produs.id
                cart_products.append({
                    'id': produs_id,
                    'product': produs, 
                    'ingrediente': produs_ingrediente,
                    'quantity': product['quantity'], 
                    'price': product['price'],
                    'pret_total': product['quantity']*product['price']
                })
                
                ComandaDetaliu.objects.create(
                    comanda=comanda,
                    produs=produs,
                    cantitate=product['quantity'],
                    pret_per_unitate=product['price']
                )
                
            
            # print(cart_products)
                
            
            email = EmailMessage(
                subject='Comanda',
                body='Mai jos aveti un atasament in care veti gasi factura comenzii dumneavoastra.',
                to=['flavorcalifornia@gmail.com']
            )
            file_path = fisier_pdf(cart_products=cart_products, total=total, user_data={'id': id, 'data_curenta': str(data_curenta), 'nume': nume_user, 'email': email_user})
            email.attach_file(file_path)
            email.send()
            
            
            
            return JsonResponse({"message": "Datele au fost procesate cu succes!"}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Eroare la decodarea datelor JSON."}, status=400)
    return HttpResponse("ok")



# model
from .models import Elev
def afisare_elevi(request):
    elevi = Elev.objects.all()
    return render(request, 'elevi.html', {'elevi': elevi})

def elevi_view(request, id):
    elev = get_object_or_404(Elev, id=id)
    return render(request, 'elevi_view.html', {'elev': elev, 'id': id})

from .forms import ElevForm
def elevi_add(request):
    if request.method == 'POST':
        form = ElevForm(request.POST)
        if form.is_valid():
            elev = form.save(commit=False)
            
            nume_elev = form.cleaned_data['nume']
            prenume_elev = form.cleaned_data['prenume']
            
            if Elev.objects.all().count() == 4:
                print('Al 4-lea elev')
        
                html_message = f"""
                <html>
                    <body>
                        <p>{nume_elev} {prenume_elev} a fost adaugat.</p>
                    </body>
                </html>
                """
                send_mail(
                subject='Nichita Iulia-Nicoleta, 241',
                message='Un nou elev inregistrat!',
                html_message=html_message,
                from_email='flavorcalifornia@gmail.com',
                recipient_list=['flavorcalifornia@gmail.com'],
                fail_silently=False,
                )    
            
            elev.save()
            print('Elevul a fost adaugat cu succes!')
    else:
        form = ElevForm()
    return render(request, 'elevi_add.html', {'form': form})


#examen

from .models import Student, Curs
def afisare_studenti(request):
    studenti = Student.objects.all()
    return render(request, 'studenti.html', {'studenti': studenti})

def cursuri_view(request, id):
    cursuri = Curs.objects.filter(student=id)
    return render(request, 'cursuri_view.html', {'cursuri': cursuri, 'id': id})

from .forms import CursForm
def add_curs(request):
    if request.method == 'POST':
        form = CursForm(request.POST)
        if form.is_valid():
            curs = form.save(commit=False)
            
            nume_curs = form.cleaned_data['denumire']
            nr_credite = form.cleaned_data['numar_credite']
            nume_student = form.cleaned_data['student']
            id = nume_student.id
            
            student = Student.objects.get(id=id)
            nr_cursuri = Curs.objects.filter(student=id).count() + 1
        
            html_message = f"""
            <html>
                <body>
                    <p>Ai fost inregistrat la cursul {nume_curs}. Ai in total {nr_cursuri} cursuri.</p>
                </body>
            </html>
            """
            send_mail(
            subject='info cursuri',
            message='Un nou curs inregistrat!',
            html_message=html_message,
            from_email='flavorcalifornia@gmail.com',
            recipient_list=['flavorcalifornia@gmail.com', 
                            # student.email
                            ],
            fail_silently=False,
            )    
            
            curs.save()
            print('Cursul a fost adaugat cu succes!')
    else:
        form = CursForm()
    return render(request, 'cursuri_add.html', {'form': form})