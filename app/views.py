from django.shortcuts import render,redirect
from .models import *
import qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
import logging
import os
from django.conf import settings
import qrcode
logger=logging.getLogger('django')
#  Create your views here.
def bphoitel_home(request):
    return render(request, 'bphotel/bphotel.html')
def about(request):
    return render(request,'bphotel/about.html')

def contact(request):
    return render(request,'bphotel/contact.html')

@login_required(login_url="signin")
def gallery(request):
    image=gallery_img.objects.all()
    return render(request,'bphotel/gallery.html',{"image":image})

def home(request):
    return render(request,'bphotel/home.html')
def menu(request):
    
    q=qrcode.QRCode(version=1,box_size=8,border=5)
    q.add_data("https://bphotel.pythonanywhere.com/menu/")
    q.make(fit=True)
    qr=q.make_image(fill="black",back_color="white")
    qr.save("app/static/images/qr.png")
    
    title=MenuTitle.objects.all()
    cateid=request.GET.get("category")
    if cateid == str(1):
         item=menu_items.objects.all()
    elif cateid:
        item=menu_items.objects.filter(category=cateid)


    else:
        item=menu_items.objects.all()
    context={
        'title':title,
        'item':item,
    }
    return render(request,'bphotel/menu.html',context)
def reserved(request):
    try:
        if request.method=="POST":
            name=request.POST.get("name")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            number_of_people=request.POST.get("number_of_people")
            date=request.POST.get("date")
            time=request.POST.get("time")
            request1=request.POST.get("request1")
            user=Reserve(name=name,email=email,phone=phone,number_of_people=number_of_people,date=date,time=time,request1=request1)
            user.save()
            subject='thanks for connecting with us '
            message='we will update you soon. for  yout text '
            from_email= 'ksuyog697@gmail.com'
            recipient_list=[email]

            send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)
            messages.success(request,f"hi {name} your form is submitted please check your email!!!!")
            return redirect("reserved")
    except Exception as e:
        logger.error(e,exc_info=True)

    return render(request,'bphotel/reserved.html')
def review(request):
    testitonomial=review1.objects.all()
    return render(request,'bphotel/review.html',{"testitonomial":testitonomial})


"""
========================================================
Authentication and authorization 
========================================================
"""


def signin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        rememberme=request.POST.get("rememberme")

        if not User.objects.filter(username=username).exists():
            messages.error(request,"username not found")
            return redirect("signin")
            
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            if rememberme:
                request.session.set_expiry(120000)
            else:
                request.session.set_expiry(0)


            next=request.POST.get("next",'')
            return redirect( next if next else 'home')
        else:
            messages.error(request,"paassword doesnt match")
            return redirect('signin')    
    next=request.GET.get('next',"")
    return render(request,'signin.html')

def register(request):
     if request.method == "POST":
        first_name=request.POST['f_name']
        last_name=request.POST['l_name']
        email=request.POST['email']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"user name already exist try with other username")
                return redirect("register")
        
            if User.objects.filter(email=email).exists():
                messages.error(request," email already exist try with other email address")
                return redirect("register")
            try:
                validate_password(password1)
                User.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password1,username=username)
                messages.success(request,"account created succesfully")
                return redirect("signin")
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                return redirect("register")
            
        else:
            messages.error(request,"password and conform password doesnt match!")
            return redirect('register')

     return render(request,'register.html')

def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url="signin")
def renewpass(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        
    return render(request,'renewpass.html',{"form":form})
