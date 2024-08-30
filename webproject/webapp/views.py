from datetime import datetime
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
# from django.contrib.auth import logout
from django.http import HttpResponse
# from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
import re

import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from xhtml2pdf import pisa
from django.template.loader import get_template
# from .utils import extract_request_variables


# ==============================================================================================================>
# =============================================== Homepage =====================================================>
# ==============================================================================================================>
def home(request): # ========== Homepage Display =========
    return render(request, 'webapp/home.html')


# ==============================================================================================================>
# ===============================================  Entry Form ==================================================>
# ==============================================================================================================>
def displayfunction(request):  # == Entry Form Display ===
    return render(request, 'webapp/form.html')


def entry_form(request):  # ================= Entry Form ==============
    name = request.POST.get('name')
    service_type = request.POST.get('service_type')
    service_name = request.POST.get('service_name')
    active_date = request.POST.get('active_date')
    renewal_date = request.POST.get('renewal_date')
    owner = request.POST.get('owner')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    days = request.POST.get('days')
    # status = request.POST.get('status')

    if not name:
        context = {'valid': "false"}
        return render(request, 'webapp/form.html', context)
    if not service_name:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not service_type:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not active_date:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not renewal_date:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not owner:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not email:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not contact:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if not days:
        context = {'valid': 'false'}
        return render(request, 'webapp/form.html', context)
    if renewal_date < active_date:
        context = {'valid': 'small'}
        return render(request, 'webapp/form.html', context)

    # For duplicate Service Name ======================================>
    user = User.objects.all()
    for x in user:
        if x.service_name == service_name:
            context = {'valid': 'service_name'}
            return render(request, 'webapp/form.html', context)
    # For contact validation ==============================================>
    pattern = re.compile("(0|01)?[0-9]{11}")
    if not (pattern.match(contact)):
        context = {'valid': 'contact'}
        return render(request, 'webapp/form.html', context)
    # For email validation ============================================>
    pattern = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
    if not (pattern.match(email)):
        context = {'valid': 'email'}
        return render(request, 'webapp/form.html', context)

    # Code for checking Duplicate Date ================================>
    user = User.objects.all()
    for x in user:
        if service_type == x.service_type:
            if x.active_date <= active_date <= x.renewal_date:
                context = {'valid': 'using'}
                return render(request, 'webapp/form.html', context)
            elif x.active_date <= renewal_date <= x.renewal_date:
                context = {'valid': 'using'}
                return render(request, 'webapp/form.html', context)
            if active_date <= x.active_date:
                if renewal_date >= x.active_date:
                    context = {'valid': 'using'}
                    return render(request, 'webapp/form.html', context)

    context = {'valid': 'true'}
    # Create a new User entry in the database using the User model
    user = User(name=name, service_type=service_type, service_name=service_name, active_date=active_date,
                renewal_date=renewal_date, owner=owner, email=email, contact=contact, days=days)
    user.save()
    return render(request, 'webapp/form.html', context)


# ==============================================================================================================>
# ==================================== Present Admin ===========================================================>
# ==============================================================================================================>

# ======= Present Admin Log-in, Log-out Part ========================================>
def signin(request):  # === Present Admin Signin-Display ===
    return render(request, 'webapp/login.html')


def log_in(request):  # ========= Present Admin Login =============
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            return render(request, 'webapp/error.html')
        if not password:
            return render(request, 'webapp/error.html')

        # For email validation =====================================>
        pattern = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
        if not (pattern.match(email)):
            return render(request, 'webapp/error.html')

        # db duplicate checking ====================================>
        account = Account.objects.all()
        for x in account:
            if email == x.email and password == x.password:
                check_user = authenticate(request, username=x.name, password=password)
                if check_user:
                    login(request, check_user)
                    userlist = User.objects.all()
                    context = {'userlist': userlist}
                    return render(request, 'webapp/collapse.html', context)
                else:
                    return HttpResponse("User doesn't exist in Django admin. Please request your admin to register your mail address...")
            else:
                HttpResponse("Wrong Username or Password")
    else:
        return render(request, 'webapp/login.html')


def log_out(request):  # ====== Present Admin Logout ======
    logout(request)
    return render(request, 'webapp/login.html')


# ========== Present Admin Registration Part ==================================>
def register(request):  # ====== Present Admin Registration display ==========
    return render(request, 'webapp/register.html')


def registration(request):  # ======== Present Admin Registration ============
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if password != repeat_password or len(password) < 6:
            return render(request, 'webapp/pass_verification.html')
        # For empty check =========================================>
        if not name:
            return render(request, 'webapp/error.html')
        if not email:
            return render(request, 'webapp/error.html')
        if not contact:
            return render(request, 'webapp/error.html')
        if not password:
            return render(request, 'webapp/error.html')

        # For contact validation ===================================>
        pattern = re.compile("(0|01)?[0-9]{11}")
        if not (pattern.match(contact)):
            return render(request, 'webapp/error.html')
        # For email validation =====================================>
        pattern = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
        if not (pattern.match(email)):
            return render(request, 'webapp/error.html')

        # db duplicate checking ====================================>
        account = Account.objects.all()
        for x in account:
            if email == x.email:
                return render(request, 'webapp/email_error.html')
        # End of db duplicate checking ======================================>

        # Create Edited User entry in the database using the User model
        account = Account(email=email, name=name, contact=contact, password=password)
        account.save()

        return HttpResponse("Registration Successful!")
    else:
        return HttpResponse("Invalid request method.")


@login_required(login_url='/signin/')
def collapsefunction(request):  # ============= Table View =============
    all_user = User.objects.all()
    context = {'userlist': all_user}
    return render(request, 'webapp/collapse.html', context)


# ====== For Table Edit & Delete ======================================================>
@login_required(login_url='/signin/')
def table(request):  # ======== Table value Search and Display =====================
        date_arr = []
        from_date = request.POST.get('domain_active')
        to_date = request.POST.get('domain_renewal')
        btn = request.POST.get('domain_btn')
        service = request.POST.get('service_type')
        search_value = request.POST.get('search_value')
        search = request.POST.get('search') # search Button
        user = User.objects.all()

        # ==== Search ================================================================>
        if search:
            for x in user:
                if x.name == search_value:
                    date_arr.extend(User.objects.filter(name=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.service_type == search_value:
                    date_arr.extend(User.objects.filter(service_type=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.service_name == search_value:
                    date_arr.extend(User.objects.filter(service_name=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.active_date == search_value:
                    date_arr.extend(User.objects.filter(active_date=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.renewal_date == search_value:
                    date_arr.extend(User.objects.filter(renewal_date=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.owner == search_value:
                    date_arr.extend(User.objects.filter(owner=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.email == search_value:
                    date_arr.extend(User.objects.filter(email=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.contact == search_value:
                    date_arr.extend(User.objects.filter(contact=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
                elif x.days == search_value:
                    date_arr.extend(User.objects.filter(days=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/collapse.html', context)
            context = {'userlist': date_arr}
            return render(request, 'webapp/collapse.html', context)

        # ==== Search based on Date and Service-type ===================================>
        if btn == "AFTER":
            if service != "All":
                for x in user:
                    if from_date <= x.active_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)
            elif service == "All":
                for x in user:
                    if from_date <= x.active_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)
        elif btn == "BEFORE":
            if service != "All":
                for x in user:
                    if from_date >= x.active_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)
            elif service == "All":
                for x in user:
                    if from_date >= x.active_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)

        elif btn == "BETWEEN":
            if service != "All":
                for x in user:
                    if from_date <= x.active_date <= to_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)
            elif service == "All":
                for x in user:
                    if from_date <= x.active_date <= to_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/collapse.html', context)
        elif service == "All":
            all_user = User.objects.all()
            context = {'userlist': all_user}
            return render(request, 'webapp/collapse.html', context)
        elif service == "":
            all_user = User.objects.all()
            context = {'userlist': all_user}
            return render(request, 'webapp/collapse.html', context)
        else:
            # return HttpResponse(service)
            all_user = User.objects.filter(service_type=service)
            context = {'userlist': all_user}
            return render(request, 'webapp/collapse.html', context)


@login_required(login_url='/signin/')
def table_edit(request):  # ================= Table Value Delete =============================
    delete_id = request.POST.get('delete_info')
    delete_button = request.POST.get('delete_button')
    service = request.POST.get('service_type')
    if delete_id:
        info = User.objects.filter(id=delete_id)
        for value in info:
            userinfo = DeletedUsers(id=value.id, name=value.name, service_type=value.service_type, service_name=value.service_name, active_date=value.active_date,
                        renewal_date=value.renewal_date, owner=value.owner, email=value.email, contact=value.contact, days=value.days, status='inactive')

            userinfo.save()
        User.objects.filter(id=delete_id).delete()
        userinfo = DeletedUsers.objects.filter(id=delete_id)
        print(userinfo)
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        return render(request, 'webapp/collapse.html', context)
    # edit_button = request.POST.get('edit_button')
    edit_id = request.POST.get('edit_info')
    if edit_id:
        user_info = User.objects.filter(id=edit_id)
        context = {'user': user_info}
        return render(request, 'webapp/edit.html', context)
    all_check = request.POST.get('all_check')
    if all_check == "true":
        if delete_button == "true":
            if service == "ALL":
                info = User.objects.all()
                for value in info:
                    userinfo = DeletedUsers(name=value.name, service_type=value.service_type,
                                            service_name=value.service_name, active_date=value.active_date,
                                            renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                            contact=value.contact, days=value.days, status='inactive')
                    userinfo.save()
                User.objects.all().delete()
                user_list = User.objects.all()
                context = {'userlist': user_list}
                return render(request, 'webapp/collapse.html', context)
            else:
                info = User.objects.filter(service_type=service)
                for value in info:
                    userinfo = DeletedUsers(name=value.name, service_type=value.service_type,
                                            service_name=value.service_name, active_date=value.active_date,
                                            renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                            contact=value.contact, days=value.days, status='inactive')
                    userinfo.save()
                User.objects.filter(service_type=service).delete()
                user_list = User.objects.all()
                context = {'userlist': user_list}
                return render(request, 'webapp/collapse.html', context)
    # for list of check ===============================================>
    if request.method == 'POST':
        id_list = request.POST.getlist("check[]")
        if id_list:
            if delete_button == "true":
                for y in id_list:
                    info = User.objects.filter(id=y)
                    for value in info:
                        userinfo = DeletedUsers(name=value.name, service_type=value.service_type,
                                                service_name=value.service_name, active_date=value.active_date,
                                                renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                                contact=value.contact, days=value.days, status='inactive')
                        userinfo.save()
                    User.objects.filter(id=y).delete()
                if service != "All":
                    user_list = User.objects.filter(service_type=service)
                    context = {'userlist': user_list}
                    return render(request, 'webapp/collapse.html', context)
                else:
                    user_list = User.objects.all()
                    context = {'userlist': user_list}
                    return render(request, 'webapp/collapse.html', context)

    user_list = User.objects.all()
    context = {'userlist': user_list}
    return render(request, 'webapp/collapse.html', context)


@login_required(login_url='/signin/')
def edit_value(request):  # ========== Table Value Edit ==================
    if request.method == 'POST':
        temp = request.POST.get('user_id')
        name = request.POST.get('name')
        service_name = request.POST.get('service_name')
        service_type = request.POST.get('service_type')
        active_date = request.POST.get('active_date')
        renewal_date = request.POST.get('renewal_date')
        owner = request.POST.get('owner')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        days = request.POST.get('days')
        unedited_value = User.objects.filter(id=temp)

        # For empty check =========================================>
        if not name:
            unedited_value.update(name = "Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif name == "Field can't be EMPTY!":
            unedited_value.update(name="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not service_name:
            unedited_value.update(service_name="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif service_name == "Field can't be EMPTY!":
            unedited_value.update(service_name="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not active_date:
            unedited_value.update(active_date="")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not renewal_date:
            unedited_value.update(renewal_date="")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not owner:
            unedited_value.update(owner="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif owner == "Field can't be EMPTY!":
            unedited_value.update(owner="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not email:
            unedited_value.update(email="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif email == "Field can't be EMPTY!":
            unedited_value.update(email="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif email == "Invalid Email Address!":
            unedited_value.update(email="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not contact:
            unedited_value.update(contact="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif contact == "Field can't be EMPTY!":
            unedited_value.update(contact="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif contact == "Invalid Contact!":
            unedited_value.update(contact="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if not days:
            unedited_value.update(days="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        elif days == "Field can't be EMPTY!":
            unedited_value.update(days="Field can't be EMPTY!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        if renewal_date < active_date:
            unedited_value.update(renewal_date="")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)

        # For contact validation ===================================>
        pattern = re.compile("(0|01)?[0-9]{11}")
        if not (pattern.match(contact)):
            unedited_value.update(contact="Invalid Contact!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)
        # For email validation =====================================>
        pattern = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
        if not (pattern.match(email)):
            unedited_value.update(email="Invalid Email Address!")
            context = {'user': unedited_value}
            return render(request, 'webapp/edit.html', context)

        # Code for checking Duplicate Service Name===========================>
        user = User.objects.exclude(id=temp)
        for x in user:
            if x.service_name == service_name:
                context = {'valid': 'service_name'}
                return render(request, 'webapp/edit.html', context)

        # Code for checking Duplicate DATE ===========================>
        other_users = User.objects.exclude(id=temp)
        for x in other_users:
            if service_type == x.service_type:
                if x.active_date <= active_date <= x.renewal_date:
                    unedited_value.update(active_date="")
                    context = {'user': unedited_value}
                    return render(request, 'webapp/edit.html', context)
                elif x.active_date <= renewal_date <= x.renewal_date:
                    unedited_value.update(renewal_date="")
                    context = {'user': unedited_value}
                    return render(request, 'webapp/edit.html', context)
                if active_date <= x.active_date:
                    if renewal_date >= x.active_date:
                        unedited_value.update(renewal_date="")
                        context = {'user': unedited_value}
                        return render(request, 'webapp/edit.html', context)
        # End of checking Duplicate =============================>

        # Create Edited User entry in the database using the User model
        User.objects.filter(id=temp).delete()
        user = User(id=temp, name=name, service_name=service_name, service_type=service_type, active_date=active_date,
                    renewal_date=renewal_date, owner=owner, email=email, contact=contact, days=days)
        user.save()
        user_list = User.objects.all()
        context = {'userlist': user_list}
        return render(request, 'webapp/collapse.html', context)
    else:
        return HttpResponse("Invalid request method.")


def csv_file(request):  # ============= For CSV ======================
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'
    writer = csv.writer(response)
    writer.writerow(
        ["Username", "Service Type", "Service Name", "Activation Date", "Renewal Date", "Owner", "Email", "Contact",
         "Days"])

    date_arr = []
    users = User.objects.all()
    from_date = request.POST.get('active_date')
    to_date = request.POST.get('renewal_date')
    btn = request.POST.get('btn')
    service = request.POST.get('service')

    # Start of CheckBox AFTER, BEFORE & BETWEEN ========================================================>
    if btn == "AFTER":
        if service != "All":
            for x in users:
                if from_date <= x.active_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
    elif btn == "BEFORE":
        if service != "All":
            for x in users:
                if from_date >= x.active_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
        elif service == "All":
            for x in users:
                if from_date >= x.active_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
    elif btn == "BETWEEN":
        if service != "All":
            for x in users:
                if from_date <= x.active_date <= to_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date <= to_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
            return response
    # END of CheckBox AFTER, BEFORE & BETWEEN ========================================================>

    elif service == "Domain":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
        return response
    elif service == "Hosting":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
        return response
    elif service == "AMC":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
        return response
    elif service == "License":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
        return response
    elif service == "Others":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days])
        return response
    elif service == "All":
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days])
        return response
    elif service == "":
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days])
        return response
    else:
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days])
        return response

    users = User.objects.all()
    for user in users:
        writer.writerow([user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner, user.email, user.contact, user.days])
    return response


def pdf(request):  # ======================= For PDF ======================
    template_path = 'webapp/pdf_table.html'

    date_arr = []
    users = User.objects.all()
    from_date = request.POST.get('active_date')
    to_date = request.POST.get('renewal_date')
    btn = request.POST.get('btn')
    service = request.POST.get('service')

    # Start of CheckBox AFTER, BEFORE & BETWEEN ========================================================>
    if btn == "AFTER":
        if service != "All":
            for x in users:
                if from_date <= x.active_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    elif btn == "BEFORE":
        if service != "All":
            for x in users:
                if from_date >= x.active_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in users:
                if from_date >= x.active_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    elif btn == "BETWEEN":
        if service != "All":
            for x in users:
                if from_date <= x.active_date <= to_date and service == x.service_type:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date and to_date >= x.active_date:
                    date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'userlist': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    # END of CheckBox AFTER, BEFORE & BETWEEN ========================================================>

    elif service == "Domain":
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "Hosting":
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "AMC":
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "License":
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "Others":
        user_list = User.objects.filter(service_type=service)
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        # response = open("report.pdf", "rb").read()
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "All":
        user_list = User.objects.all()
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # pisa.startViewer('report.pdf')
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        # return render(request, 'webapp/form.html', context)
    elif service == "":
        user_list = User.objects.all()
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        user_list = User.objects.all()
        context = {'userlist': user_list}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    context = {'userlist': date_arr}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')


# ==============================================================================================================>
# ============================ Ex. ADMIN =======================================================================>
# ==============================================================================================================>

# ======= Ex. Admin Log-in, Log-out Part ========================================>
def exadmin_signin(request):  # === Ex. Admin Signin-Display ===
    return render(request, 'webapp/exadmin_login.html')


def exadmin_login(request):  # ========= Ex. Admin Login ==============
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            return render(request, 'webapp/error.html')
        if not password:
            return render(request, 'webapp/error.html')

        # For email validation =====================================>
        pattern = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")
        if not (pattern.match(email)):
            return render(request, 'webapp/error.html')

        # db duplicate checking ====================================>
        account = Account.objects.all()
        for x in account:
            if email == x.email and password == x.password:
                check_user = authenticate(request, username=x.name, password=password)
                if check_user:
                    login(request, check_user)
                    userlist = User.objects.all()
                    context = {'userlist': userlist}
                    return render(request, 'webapp/exadmin_home.html', context)
                else:
                    return HttpResponse("User doesn't exist in Django admin. Please request your admin to register your mail address...")
            else:
                HttpResponse("Wrong Username or Password")
    else:
        return render(request, 'webapp/exadmin_login.html')


def exadmin_logout(request):  # ====== Ex. Admin Logout ========
    logout(request)
    return render(request, 'webapp/exadmin_login.html')


@login_required(login_url='/exadmin_signin/')
def exadmin_display(request):  # ============= Table View =============
    all_user = User.objects.all()
    context = {'userlist': all_user}
    return render(request, 'webapp/exadmin_home.html', context)


# ====== For Table Edit & Delete ======================================================>
@login_required(login_url='/exadmin_signin/')
def exadmin_table(request):  # ======== Table value Search and Display ================
        date_arr = []
        from_date = request.POST.get('domain_active')
        to_date = request.POST.get('domain_renewal')
        btn = request.POST.get('domain_btn')
        service = request.POST.get('service_type')
        search_value = request.POST.get('search_value')
        search = request.POST.get('search')  # search Button
        user = User.objects.all()

        # ==== Search ================================================================>
        if search:
            for x in user:
                if x.name == search_value:
                    date_arr.extend(User.objects.filter(name=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.service_type == search_value:
                    date_arr.extend(User.objects.filter(service_type=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.service_name == search_value:
                    date_arr.extend(User.objects.filter(service_name=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.active_date == search_value:
                    date_arr.extend(User.objects.filter(active_date=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.renewal_date == search_value:
                    date_arr.extend(User.objects.filter(renewal_date=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.owner == search_value:
                    date_arr.extend(User.objects.filter(owner=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.email == search_value:
                    date_arr.extend(User.objects.filter(email=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.contact == search_value:
                    date_arr.extend(User.objects.filter(contact=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
                elif x.days == search_value:
                    date_arr.extend(User.objects.filter(days=search_value))
                    context = {'userlist': date_arr}
                    return render(request, 'webapp/exadmin_home.html', context)
            context = {'userlist': date_arr}
            return render(request, 'webapp/exadmin_home.html', context)

        # ==== Search based on Date and Service-type ===================================>
        if btn == "AFTER":
            if service != "All":
                for x in user:
                    if from_date <= x.active_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)
            elif service == "All":
                for x in user:
                    if from_date <= x.active_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)
        elif btn == "BEFORE":
            if service != "All":
                for x in user:
                    if from_date >= x.active_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)
            elif service == "All":
                for x in user:
                    if from_date >= x.active_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)

        elif btn == "BETWEEN":
            if service != "All":
                for x in user:
                    if from_date <= x.active_date <= to_date and service == x.service_type:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)
            elif service == "All":
                for x in user:
                    if from_date <= x.active_date <= to_date:
                        date_arr.extend(User.objects.filter(active_date=x.active_date, service_type=x.service_type))
                context = {'userlist': date_arr}
                return render(request, 'webapp/exadmin_home.html', context)
        elif service == "All":
            all_user = User.objects.all()
            context = {'userlist': all_user}
            return render(request, 'webapp/exadmin_home.html', context)
        elif service == "":
            all_user = User.objects.all()
            context = {'userlist': all_user}
            return render(request, 'webapp/exadmin_home.html', context)
        else:
            # return HttpResponse(service)
            all_user = User.objects.filter(service_type=service)
            context = {'userlist': all_user}
            return render(request, 'webapp/exadmin_home.html', context)


# ==============================================================================================================>
# =================================== Recycle Bin ==============================================================>
# ==============================================================================================================>

# ========================= Recycle Log-in PART ======================>
def recycle_signin(request):  # ===== Recycle Sign-in Display ======
    return render(request, 'webapp/recycle_login.html')


def recycle_login(request):  # ======== Recycle Log-in ================
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        check_user = authenticate(request, username=uname, password=pwd)
        if check_user:
            login(request, check_user)
            deleted_data = DeletedUsers.objects.all()
            context = {'deleted_data': deleted_data}
            return render(request, 'webapp/recycle.html', context)
        else:
            return HttpResponse('Wrong Username or Password')


def recycle_logout(request):  # ======= Recycle Log-out ===========
    logout(request)
    return render(request, 'webapp/recycle_login.html')


# ================= Recycle Bin Table ==============================>
@login_required(login_url='/recycle_signin/')
def recycle(request):  # ========= Recycle Display ==========
    return render(request, 'webapp/recycle.html')


@login_required(login_url='/recycle_signin/')
def recycle_bin(request):  # ==== For recycle data Search ====
    date_arr = []
    from_date = request.POST.get('domain_active')
    to_date = request.POST.get('domain_renewal')
    btn = request.POST.get('domain_btn')
    service = request.POST.get('service_type')
    search_value = request.POST.get('search_value')
    search = request.POST.get('search')  # search Button
    deleted_user = DeletedUsers.objects.all()

    # ===== For Search ==============================================================>
    if search:
        for x in deleted_user:
            if x.name == search_value:
                date_arr.extend(DeletedUsers.objects.filter(name=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.service_type == search_value:
                date_arr.extend(DeletedUsers.objects.filter(service_type=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.service_name == search_value:
                date_arr.extend(DeletedUsers.objects.filter(service_name=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.active_date == search_value:
                date_arr.extend(DeletedUsers.objects.filter(active_date=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.renewal_date == search_value:
                date_arr.extend(DeletedUsers.objects.filter(renewal_date=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.owner == search_value:
                date_arr.extend(DeletedUsers.objects.filter(owner=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.email == search_value:
                date_arr.extend(DeletedUsers.objects.filter(email=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.contact == search_value:
                date_arr.extend(DeletedUsers.objects.filter(contact=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)
            elif x.days == search_value:
                date_arr.extend(DeletedUsers.objects.filter(days=search_value))
                context = {'deleted_data': date_arr}
                return render(request, 'webapp/recycle.html', context)

    # ========= Search based on Date and Service-type ============================>
    if btn == "AFTER":
        if service != "All":
            for x in deleted_user:
                if from_date <= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)
        elif service == "All":
            for x in deleted_user:
                if from_date <= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)
    elif btn == "BEFORE":
        if service != "All":
            for x in deleted_user:
                if from_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)
        elif service == "All":
            for x in deleted_user:
                if from_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)

    elif btn == "BETWEEN":
        if service != "All":
            for x in deleted_user:
                if from_date <= x.active_date and to_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)
        elif service == "All":
            for x in deleted_user:
                if from_date <= x.active_date and to_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            return render(request, 'webapp/recycle.html', context)
    elif service == "All":
        deleted_data = DeletedUsers.objects.all()
        context = {'deleted_data': deleted_data}
        return render(request, 'webapp/recycle.html', context)
    elif service == "":
        deleted_data = DeletedUsers.objects.all()
        context = {'deleted_data': deleted_data}
        return render(request, 'webapp/recycle.html', context)
    else:
        # return HttpResponse(service)
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        return render(request, 'webapp/recycle.html', context)

    deleted_data = DeletedUsers.objects.all()
    context = {'deleted_data': deleted_data}
    return render(request, 'webapp/recycle.html', context)


@login_required(login_url='/recycle_signin/')
def recycle_pdf(request):  # ====== DELETED Data's PDF =======
    template_path = 'webapp/recycle_pdf.html'
    date_arr = []
    deleted_user = User.objects.all()
    from_date = request.POST.get('active_date')
    to_date = request.POST.get('renewal_date')
    btn = request.POST.get('btn')
    service = request.POST.get('service')

    # Start of CheckBox AFTER, BEFORE & BETWEEN ========================================================>
    if btn == "AFTER":
        if service != "All":
            for x in deleted_user:
                if from_date <= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in deleted_user:
                if from_date <= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    elif btn == "BEFORE":
        if service != "All":
            for x in deleted_user:
                if from_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in deleted_user:
                if from_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    elif btn == "BETWEEN":
        if service != "All":
            for x in deleted_user:
                if from_date <= x.active_date and to_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        elif service == "All":
            for x in deleted_user:
                if from_date <= x.active_date and to_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            context = {'deleted_data': date_arr}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)
            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
    # END of CheckBox AFTER, BEFORE & BETWEEN ========================================================>

    elif service == "Domain":
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "Hosting":
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "AMC":
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "License":
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "Others":
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        # response = open("report.pdf", "rb").read()
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    elif service == "All":
        deleted_data = DeletedUsers.objects.all()
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # pisa.startViewer('report.pdf')
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        # return render(request, 'webapp/form.html', context)
    elif service == "":
        deleted_data = DeletedUsers.objects.all()
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        deleted_data = DeletedUsers.objects.all()
        context = {'deleted_data': deleted_data}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)
        # create a pdf
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    context = {'deleted_data': date_arr}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required(login_url='/recycle_signin/')
def recycle_csv(request):   # ================== DELETED Data's CSV ======================
    service = request.POST.get('service')
    response = HttpResponse(content_type='text/csv')
    if service == 'Domain':
        response['Content-Disposition'] = 'attachment; filename=Deleted users [Domain].csv'
    elif service == 'Hosting':
        response['Content-Disposition'] = 'attachment; filename=Deleted users [Hosting].csv'
    elif service == 'AMC':
        response['Content-Disposition'] = 'attachment; filename=Deleted users [AMC].csv'
    elif service == 'License':
        response['Content-Disposition'] = 'attachment; filename=Deleted users [License].csv'
    elif service == 'Others':
        response['Content-Disposition'] = 'attachment; filename=Deleted users [Others].csv'
    else:
        response['Content-Disposition'] = 'attachment; filename=Deleted users [ALL].csv'

    writer = csv.writer(response)
    writer.writerow(
        ["Username", "Service Type", "Service Name", "Activation Date", "Renewal Date", "Owner", "Email", "Contact",
         "Days", "Status"])

    date_arr = []
    users = DeletedUsers.objects.all()
    from_date = request.POST.get('active_date')
    to_date = request.POST.get('renewal_date')
    btn = request.POST.get('btn')

    # Start of CheckBox AFTER, BEFORE & BETWEEN ========================================================>
    if btn == "AFTER":
        if service != "All":
            for x in users:
                if from_date <= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
    elif btn == "BEFORE":
        if service != "All":
            for x in users:
                if from_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
        elif service == "All":
            for x in users:
                if from_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
    elif btn == "BETWEEN":
        if service != "All":
            for x in users:
                if from_date <= x.active_date and to_date >= x.active_date and service == x.service_type:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
        elif service == "All":
            for x in users:
                if from_date <= x.active_date and to_date >= x.active_date:
                    date_arr.extend(DeletedUsers.objects.filter(active_date=x.active_date, service_type=x.service_type))
            for user in date_arr:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
            return response
    # END of CheckBox AFTER, BEFORE & BETWEEN ========================================================>

    elif service == "Domain":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
        return response
    elif service == "Hosting":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
        return response
    elif service == "AMC":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
        return response
    elif service == "License":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
        return response
    elif service == "Others":
        for user in users:
            if service == user.service_type:
                writer.writerow(
                    [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                     user.email, user.contact, user.days, user.status])
        return response
    elif service == "All":
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days, user.status])
        return response
    elif service == "":
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days, user.status])
        return response
    else:
        for user in users:
            writer.writerow(
                [user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner,
                 user.email, user.contact, user.days, user.status])
        return response

    users = DeletedUsers.objects.all()
    for user in users:
        writer.writerow([user.name, user.service_type, user.service_name, user.active_date, user.renewal_date, user.owner, user.email, user.contact, user.days, user.status])
    return response


@login_required(login_url='/recycle_signin/')
def recycle_data(request):  # ================= Deleted DATA Restore and DELETE ===============
    restore_id = request.POST.get('restore_id')
    restore = request.POST.get('restore')
    delete = request.POST.get('delete')
    all_check = request.POST.get('all_check')
    id_list = request.POST.getlist("check[]")
    service = request.POST.get('service_type')

    if restore_id:
        info = DeletedUsers.objects.filter(id=restore_id)
        for value in info:
            userinfo = User(id=value.id, name=value.name, service_type=value.service_type, service_name=value.service_name, active_date=value.active_date,
                        renewal_date=value.renewal_date, owner=value.owner, email=value.email, contact=value.contact, days=value.days)

            userinfo.save()
        DeletedUsers.objects.filter(id=restore_id).delete()
        deleted_data = DeletedUsers.objects.filter(service_type=service)
        context = {'deleted_data': deleted_data}
        return render(request, 'webapp/recycle.html', context)

    if all_check == "true":
        if delete == "true":
            if service == "ALL":
                DeletedUsers.objects.all().delete()
                deleted_data = DeletedUsers.objects.all()
                context = {'deleted_data': deleted_data}
                return render(request, 'webapp/recycle.html', context)
            else:
                DeletedUsers.objects.filter(service_type=service).delete()
                deleted_data = DeletedUsers.objects.all()
                context = {'deleted_data': deleted_data}
                return render(request, 'webapp/recycle.html', context)
        elif restore == "true":
            if service == "ALL":
                info = DeletedUsers.objects.all()
                for value in info:
                    userinfo = User(name=value.name, service_type=value.service_type,
                                            service_name=value.service_name, active_date=value.active_date,
                                            renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                            contact=value.contact, days=value.days)
                    userinfo.save()
                DeletedUsers.objects.all().delete()
                deleted_data = DeletedUsers.objects.all()
                context = {'deleted_data': deleted_data}
                return render(request, 'webapp/recycle.html', context)
            else:
                info = DeletedUsers.objects.filter(service_type=service)
                for value in info:
                    userinfo = User(name=value.name, service_type=value.service_type,
                                            service_name=value.service_name, active_date=value.active_date,
                                            renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                            contact=value.contact, days=value.days)
                    userinfo.save()
                DeletedUsers.objects.filter(service_type=service).delete()
                deleted_data = DeletedUsers.objects.all()
                context = {'deleted_data': deleted_data}
                return render(request, 'webapp/recycle.html', context)

    # for list of check ===========================================================>
    if request.method == 'POST':
        id_list = request.POST.getlist("check[]")
        if id_list:
            if restore == "true":
                for y in id_list:
                    info = DeletedUsers.objects.filter(id=y)
                    for value in info:
                        userinfo = User(name=value.name, service_type=value.service_type,
                                                service_name=value.service_name, active_date=value.active_date,
                                                renewal_date=value.renewal_date, owner=value.owner, email=value.email,
                                                contact=value.contact, days=value.days)
                        userinfo.save()
                    DeletedUsers.objects.filter(id=y).delete()
                if service != "All":
                    deleted_data = DeletedUsers.objects.filter(service_type=service)
                    context = {'deleted_data': deleted_data}
                    return render(request, 'webapp/recycle.html', context)
                else:
                    deleted_data = DeletedUsers.objects.all()
                    context = {'deleted_data': deleted_data}
                    return render(request, 'webapp/recycle.html', context)
            elif delete == "true":
                for y in id_list:
                    DeletedUsers.objects.filter(id=y).delete()
                if service != "All":
                    deleted_data = DeletedUsers.objects.filter(service_type=service)
                    context = {'deleted_data': deleted_data}
                    return render(request, 'webapp/recycle.html', context)
                else:
                    deleted_data = DeletedUsers.objects.all()
                    context = {'deleted_data': deleted_data}
                    return render(request, 'webapp/recycle.html', context)

    deleted_data = DeletedUsers.objects.all()
    context = {'deleted_data': deleted_data}
    return render(request, 'webapp/recycle.html', context)

# END OF CODES ========================================================================================================>
