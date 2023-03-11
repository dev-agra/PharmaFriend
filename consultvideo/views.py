from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse, HttpResponse
import random
import time
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.models import Account
from twilio.rest import Client
from decouple import config

TWILIOAPI_SID = config('TWILIOAPI_SID')
TWILIOAPI_KEY = config('TWILIOAPI_KEY')
Phonenumber = config('Phonenumber')

client = Client(TWILIOAPI_SID, TWILIOAPI_KEY)

def gettoken(request):
    # Hidden Values below 
    appId = config('appId')
    appCertificate = config('appCertificate')
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeSeconds = 3600*24 # In seconds
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeSeconds
    role = 1 #1->host, 2->user

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid},safe=False)

def Consult(request):
    return render(request, 'consultvideo/consultstream.html')

@login_required(login_url = "accounts:loginuser")
def CreateRoom(request):
    return render(request, 'consultvideo/createconsultroom.html')

def RequestConsult(request):
    current_user = request.user
    current_user.consult_pending = True
    current_user.save()
    user = Account.object.filter(is_staff=True).first()
    url = 'http://127.0.0.1:8000/Consult/'
    mail_subject = "Request for Consultation"
    message = render_to_string('consultvideo/newrequest_email.html',{
           'current_user': current_user,
           'admin_user': user,
           'site_url': url,
    })
    to_email = user.email
    send_mail = EmailMessage(mail_subject, message, to=[to_email] )
    send_mail.send()
    return render(request, 'consultvideo/newrequest.html')

def SendConsult(request):
    room = request.GET.get('room_name')
    print(room)
    current_user = request.user
    user = Account.object.filter(consult_pending=True).first()
    url = 'http://127.0.0.1:8000/Consult/'
    mail_subject = "Room Details for Consultation Request"
    message_mail = render_to_string('consultvideo/fulfillrequest_email.html',{
           'request_user': user,
           'admin_user': current_user,
           'site_url': url,
           'room_name': room
    })
    to_email = user.email
    send_mail = EmailMessage(mail_subject, message_mail, to=[to_email] )
    send_mail.send()

    message_sent = f"Your Request for consultations services has been accepted by {current_user.first_name} {current_user.last_name}\nThe name of the consulting room is: {room}\nRequest to kindly join the room within 15 minutes"
    message_phone = client.messages.create(
    body=message_sent,
    from_=Phonenumber,
    to=f'+91{user.phone_no}'
    )

    user.consult_pending = False
    user.save()
    # Do something with the data, such as saving it to the database
    return JsonResponse({'success': True})