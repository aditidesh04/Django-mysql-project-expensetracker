from django.shortcuts import render,redirect
from .services import TrackerServices   #.services means from current directory

def homepage(request):
    return render(request, 'index.html')

def registerform(request):
    return render(request, 'UserRegistration.html')

def adduser(request):
    if request.method=='POST':
        uid=request.POST.get("userid")
        ps=request.POST.get("password")
        nm=request.POST.get("username")
        mob=request.POST.get("mobile")
        age=int(request.POST.get("age"))
        gen=request.POST.get("gender")
        occ=request.POST.get("occupation")
        ct=request.POST.get("city")
        obj=TrackerServices()
        msg=obj.addnewuser(uid,ps,nm,mob,age,gen,occ,ct)

    return render(request,"RegisterStatus.html",{'status':msg,'name':nm})

def change(request):
    
    return render(request,'change.html')

def login( request):
    if request.method=='POST':
        uid=request.POST.get("userid")
        ps=request.POST.get("password")
        obj = TrackerServices()
        status=obj.checkuser(uid,ps)

        if status=='success':
            request.session['authenticated']=True
            request.session['user']=uid
            return redirect('/dashboard/')
        else:
            request.session['authenticated']=False
            return render(request,"loginfailed.html")
        

        
def dashboard(request):
    if request.session.get('authenticated'):
        uid=request.session.get('user')
        return render(request,'dashboard.html',{'userid':uid})
    else:
        return render(request,"index.html")

def newexpense(request):
   return render(request,"NewExpense.html")
        


    
def addexpense(request):
    msg=''
    if request.method=="POST":
        uid=request.session.get("user")
        dt=request.POST.get("expense_date")
        cat=request.POST.get("category")
        des=request.POST.get("description")
        amt=float(request.POST.get("amount"))
        pay=request.POST.get("paymentmode")
        obj=TrackerServices()
        msg=obj.addnewexpense(uid,dt,cat,des,amt,pay)
    
    return render(request,"ExpenseStatus.html",{'status':msg})


def changepass(request):
    if request.method=='POST':
        uid=request.session.get("user")
        opass=request.POST.get("old_password")
        npass1=request.POST.get('new_password1')
        npass2=request.POST.get('new_password2')
        obj=TrackerServices()
        status=obj.changeuserpassword(uid,opass,npass1,npass2)
    return render(request,"ChangePassStatus.html",{'status':status})


def search(request):
    return render(request,"searchexpense.html")

def searchexpenses(request):
    if request.method=='POST':
                uid=request.session.get('user')
                sdt=request.POST.get("expense_date")
                obj=TrackerServices()
                data=obj.searchexpondate(uid,sdt)
    
    return render(request,"SearchResult.html",{"expdt":sdt,"expdata":data})


def modify(request):
    return render(request,'ModifyExpense.html')


def ModifyExpense(request):
    if request.method == "POST":
        uid = request.session['uid']  # user who logged in
        sdt = request.POST.get("t1")  # date
        category = request.POST.get("t2")
        desc = request.POST.get("t3")
        amount = request.POST.get("t4")
        paymentmode = request.POST.get("t5")

        obj = TrackerServices()
        status = obj.modification(uid, sdt, category, desc, amount, paymentmode)
        return render(request, "ExpenseStatus.html", {"msg": status})
