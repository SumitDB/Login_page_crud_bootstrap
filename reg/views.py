
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm , CustomerReg
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from reg.models import Customer
# Create your views here.
def Sign_up(request):
    if request.method == 'POST':
        fm= SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully !!!')
            fm.save()
    else:
        fm = SignUpForm()
    return render (request, 'reg/signup.html',{'form':fm})


#Login View
def User_login(request):
    if  not request.user.is_authenticated:
        if request.method == "POST":
            fm=AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,'You have Logged in successfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request,'reg/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')
        
def User_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fmm = CustomerReg(request.POST)
            if fmm.is_valid():
                nm = fmm.cleaned_data['name']
                em = fmm.cleaned_data['email']
                ct = fmm.cleaned_data['city']
                reg = Customer( name=nm,email=em,city=ct)
                reg.save()
                messages.success(request,'You have successfully added the customer !!')
                fmm = CustomerReg()
        else:
            fmm = CustomerReg()
        return render(request, 'reg/profile.html',{'name':request.user, 'formm':fmm})
    else:
        return HttpResponseRedirect('/login/')

def Customers(request):
    if request.user.is_authenticated:
        cust = Customer.objects.all()
        return render(request, 'reg/customer.html',{'name':request.user, 'stu':cust})
    else:
        return HttpResponseRedirect('/login/')

def User_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# This function will delete
def Delete_data(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        messages.success(request,'You have successfully deleted the customer !!')
        return HttpResponseRedirect('/customer/')

# This function will update
def Update_data(request, id):
    # context ={}
    # # fetch the object related to passed id
    # obj = get_object_or_404(Customer, id = id)
    # # pass the object as instance in form
    # formm = CustomerReg(request.POST or None, instance = obj)
    # # save the data from the form and
    # # redirect to detail_view
    # if formm.is_valid():
    #     formm.save()
    #     return HttpResponseRedirect("reg/updatecustomer.html/",{'id':id})
    # # add form dictionary to context
    # context["formm"] = formm
    # return render(request, "reg/updatecustomer.html", context)
    if request.method == 'POST':
        pi = Customer.objects.get(pk = id)
        fmm = CustomerReg(request.POST, instance=pi)
        if fmm.is_valid():
            fmm.save()
            messages.success(request,'You have successfully edited the customer !!')
            return render(request, 'reg/updatecustomer.html',{'formm':fmm, 'id':id})
    else:
        pi = Customer.objects.get(pk=id)
        fmm = CustomerReg(instance=pi)        
    return render(request, 'reg/updatecustomer.html',{'formm':fmm, 'id':id})




