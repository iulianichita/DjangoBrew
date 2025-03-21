import schedule
import time
import django
import os
from django.core.mail import send_mail

# se incarca setarile proiectului
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proiect1.settings')
django.setup()

from django.utils import timezone
from .models import CustomUser

def task1():
    print(f"Task executat la {timezone.now()}")
    # Mancare.objects.update(ultima_actulizare=timezone.now())

def task2():
    print(f"Alt task")


# laborator9
def stergeusers_mailneconfirmat():
    users = CustomUser.objects.filter(email_confirmat=False)
    print(f"Task stergeusers_mailneconfirmat executat la {timezone.now()}")
    print(f"Deleted users: {[user.username for user in users]}")
    
    for user in users:
        user.delete()
        
def sendemail_tousers():
    users = CustomUser.objects.filter(date_joined__lte=timezone.now()-timezone.timedelta(minutes=60))
    subject = 'Newsletter'
    message = 'Acesta este un newsletter pentru voi. Vă mulțumim că v-ați alăturat!'
    from_email = 'flavorcalifornia@gmail.com'
    
    print(f"Task sendemail_tousers executat la {timezone.now()}")
    print(f"Email trimis la {[user.email for user in users]}")
    
    for user in users:
        recipient_list = ['nichitaiulia48@gmail.com', 'flavorcalifornia@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
        
        
def newusers_email():
    users = CustomUser.objects.filter(date_joined__gte=timezone.now()-timezone.timedelta(days=3))
    subject = 'New users'
    message = f"In ultimele 3 zile s-au inregistrat {len(users)} utilizatori: {[user.username for user in users]}."
    from_email = 'flavorcalifornia@gmail.com'
    send_mail(subject, message, from_email, ['flavorcaliornia@gmail.com'])
    
    print(f"Task newusers_email executat la {timezone.now()}")
    print(f"Userii noi din ultimele 3 zile sunt {[user.username for user in users]}")
    

from aplicatie_ex.models import Vizualizari, Mancare
        
def most_viewed_lastweek():
    print(f"Task most_viewed_lastweek executat la {timezone.now()}")

    now = timezone.now()
    last_week = now - timezone.timedelta(days=7)

    objects = Vizualizari.objects.filter(datavizualizare__gte=last_week)
    d = {}
    for object in objects:
        d = {object.object_id: int(0)}
    for object in objects:
        if object.object_id not in d:
            d[object.object_id] = 0  
        d[object.object_id] += 1 
        # retin nr de vizualizari pentru fiecare obiect
        
    if d:
        top_object = max(d.items(), key=lambda x: x[1])
        print(f"Top object: {top_object[0]} cu {top_object[1]} vizualizari")

        try:
            mancare_item = Mancare.objects.get(id=top_object[0])
            subject = 'Cel mai vizualizat produs din ultima săptămână'
            message = f"Cel mai vizualizat produs este {mancare_item.nume} cu {top_object[1]} vizualizări."
            from_email = 'flavorcalifornia@gmail.com'
            recipient_list = ['flavorcalifornia@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            print(f"Email trimis: {message}")
        except Mancare.DoesNotExist:
            print(f"Produsul cu ID-ul {top_object[0]} nu există.")
    else:
        print("Nu există înregistrări în ultima săptămână.")
    
    