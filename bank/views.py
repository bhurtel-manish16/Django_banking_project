import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from bank.models import Payment, Tranactions
from django.contrib.auth.models import User
import smtplib
from email.message import EmailMessage
import ssl
from django.contrib import messages
import datetime
import pyqrcode


#password for john: John213_1
#password for mannish: Manish@123, Himesh123!
# Create your views here.
def loginuser(request):
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html")
    return render(request, "login.html")


# @login_required
def user_dashboard(request):
    if  request.user.is_anonymous:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        return redirect("/")
    name = str(request.user)
    username = Payment.objects.filter(username=name)
    acc_no = str(username[0].account_number)
    trans_details = Tranactions.objects.filter(acc_no=acc_no).order_by('-date')
    dict_list = []
    for obj in trans_details:
         dict_list.append({
        'status': obj.status,
        'date': obj.date.strftime("%d/%m/%Y"),
        'amount': obj.amount,
        'discr': obj.description
    })
    trans = dict(enumerate(dict_list))
    # for i in trans:
    #     print(trans[i]["date"])
    
    if name != "admin":
        details = {
            "name":username[0].name,
            "acc_num":username[0].account_number,
            "current_balance":username[0].cureent_amount,
        }
        return render(request,"dashboard.html",{"details":details,"trans":trans})
    return render(request, "dashboard.html",{"a":details,"b":trans})


def logoutuser(request):
    logout(request)
    return redirect("login")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get('fname')
        lname = request.POST.get("lname")
        email = request.POST.get("useremail")
        passowrd = request.POST.get("userpassword")
        initial_amt = request.POST.get("initialamount")
        user = User.objects.create_user(username, email, passowrd)
        user.first_name = fname       
        user.last_name = lname
        user.save()
        name = str(fname)+" "+str(lname)
        acc_num = "1104"
        gen_random = str(random.randint(100000000,900000000000))
        for i in gen_random:
            if len(acc_num) < 12:
                acc_num += i
        payment_ins = Payment.objects.create(username=username, name=name,account_number=acc_num,cureent_amount=initial_amt)
        payment_ins.save()
        # data = "https://www.youtube.com/@thebhurtel/subscribe"
        # gen_qr = pyqrcode.create(data)
        # gen_qr.png("/static/img/"+acc_num+".png", scale=8)
        return redirect("login")
    return render(request, "signup.html")


def withdraw(request):
    if  request.user.is_anonymous:
        return redirect("/")
    if request.method == "POST":
        print("inside post")
        name = request.user
        amt = int(request.POST.get('amount'))
        paymentinst = Payment.objects.get(username=name)
        current_balance = int(paymentinst.cureent_amount.replace("$",""))
        balance_history = current_balance
        acc_no = paymentinst.account_number
        print(current_balance)
        if amt > current_balance:
            messages.add_message(request, messages.ERROR, 'Insufficient balance!')
            return redirect("dashboard")
            # return redirect(request, "/withdraw/")
        current_balance = current_balance-amt
        paymentinst.cureent_amount = current_balance
        paymentinst.save()
        name = str(request.user)
        username = Payment.objects.filter(username=name)
        if name != "admin":
            messages.add_message(request, messages.SUCCESS, 'Success!')

        # email = str(request.POST.get("email"))
        # send_email(email, amt)
        # return render(request, "dashboard.html", details)
        sender_desc = "Fund withdrawn"
        current_datetime = get_datetime()
        transaction_hisotry(acc_no, current_datetime,sender_desc,amt,"W",balance_history)
        return redirect("dashboard")
    return redirect("dashboard")


def send_email(address, amount):
    email_sender = "YOUR EMAIL"
    email_password = "YOUR PASSWORD"

    email_receiver = address
    man = "ho"
    subject="Fund withdrawn"
    body = "You have withdrawn "+str(amount)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def transfer_fund(request):
    if request.method == "POST":
        name = request.user
        paymentinst = Payment.objects.get(username=name)
        amt = int(request.POST.get('transfer_amount'))
        acc_no = request.POST.get('transfer_accno')
        sender_current_balance = int(paymentinst.cureent_amount.replace("$",""))
        sender_acc_no = paymentinst.account_number
        print(sender_current_balance)
        if amt > sender_current_balance:
            messages2 = messages.get_messages(request)
            messages2.add(messages.ERROR, 'Inssufficient balance!')
            return redirect("dashboard")
        try:
            transfer_payment = Payment.objects.get(account_number=acc_no)
            receiver_current_balance = int(transfer_payment.cureent_amount.replace("$",""))
            print("Receiver Old Balance: ",str(receiver_current_balance))
            receiver_name = transfer_payment.name
            update_sender_money = sender_current_balance-amt
            update_receiver_balance = receiver_current_balance+amt
            paymentinst.cureent_amount = update_sender_money
            transfer_payment.cureent_amount = update_receiver_balance

                #Mananing transaction hsitory for receiver
            current_datetime = get_datetime()
            receiver_desc = str(name)+" sent you fund!"
            transaction_hisotry(acc_no,current_datetime,receiver_desc,amt, "D",receiver_current_balance)

                #Manaing transaction history for sender
            sender_desc = "Transfered to "+receiver_name
            transaction_hisotry(sender_acc_no, current_datetime,sender_desc,amt,"W",sender_current_balance)
                    
            paymentinst.save()
            transfer_payment.save()
            messages2 = messages.get_messages(request)
            messages2.add(messages.SUCCESS, 'Successfully transfered!')
        except:
            messages2 = messages.get_messages(request)
            messages2.add(messages.ERROR, 'Error occur!')
            redirect("dashboard")
    return redirect("dashboard")


def transaction_hisotry(acc_no,date,description,amount,status,balance_history):
    print("working")
    trans_inst = Tranactions.objects.create(acc_no=acc_no, status=status, date=date,description = description,amount = amount,balance_history=balance_history)
    trans_inst.save()


def get_datetime():
    c_datetime = datetime.datetime.now()
    return c_datetime


def analytics(request):
    name = str(request.user)
    user = request.user
    username = Payment.objects.filter(username=name)
    acc_no = str(username[0].account_number)
    paymentinst = Payment.objects.get(username=name)
    current_balance = int(paymentinst.cureent_amount.replace("$",""))
    trans_details = Tranactions.objects.filter(acc_no=acc_no).order_by('-date')

    details = {
        "name":(str(user.first_name)+" "+str(user.last_name)).title()
    }
    dict_list = []
    for obj in trans_details:
        dict_list.append({
        'status': obj.status,
        'date': obj.date.strftime("%d"),
        'amount': obj.amount,
        'balance_history': obj.balance_history,
        'discr': obj.description
    })
    trans = dict(enumerate(dict_list))
    chart_data = transaction_chat(trans, current_balance) #Calling transaction_chat func with the trans dict value
    print(chart_data)
    context = {"trans":trans}
    total_money_spent = 0
    total_money_credit = 0
    for i in context["trans"]:
        if trans[i]["status"] == 'W':
            total_money_spent += int(trans[i]["amount"])
        else:
            total_money_credit += int(trans[i]["amount"])
    total_transaction=total_money_spent+ total_money_credit
   
    transaction = {
        "spent":total_money_spent,
        "credit":total_money_credit,
        "total_balance":current_balance+total_transaction
    }  
    return render(request, "analytics.html",{"trans":trans, "transaction":transaction, "details":details, "chart":chart_data})


def transaction_chat(data,current_balance):

    # Filter the data to only include W statuses
    filtered_data = {}
    for key, value in data.items():
        if value['status'] == 'W':
            filtered_data[key] = value

    # Get a list of dates and a list of amounts
    dates = []
    amounts = []
    cr_date = get_datetime().strftime("%d")
    for key, value in filtered_data.items():
        dates.append(value['date'])
        amounts.append(float(value['balance_history']))  # convert amount to float 
    dates.reverse()
    amounts.reverse()
    dates.append(cr_date)
    amounts.append(current_balance)

    context = {
        'dates': dates,
        'amounts': amounts
    }
    print(context["amounts"])
    return  context


def user(request):
    user = request.user
    user_details = {
        "name":str(str(user.first_name)+" "+str(user.last_name)).title(),
        "email":user.email
    }
    if request.method == "POST":
        print("Inside")
        info = User.objects.get(username=request.user)
        new_email = request.POST.get('new-email')
        info.email = new_email
        info.save()
        return redirect('user')
        
    return render(request, "user.html", user_details)



# Password
def chnage_password(request):
    if  request.user.is_anonymous:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        return redirect("/")
    if request.method == "POST":
        user_name = request.user
        current_password = request.POST.get("current-password")
        user = authenticate(username=user_name, password=current_password)
        if user != None:
            new_pasword1 = request.POST.get("new-password")
            new_pasword2 = request.POST.get("confirm-password")
            if new_pasword1 == new_pasword2:
                user_details = User.objects.get(username=user)
                user_details.set_password(new_pasword2)
                user_details.save()
                return redirect('logout')
            else:
                return HttpResponse("Password doesn't match")

        else:
            return HttpResponse("Invalid Password")
    else:
        return HttpResponse("POST doesn't work")