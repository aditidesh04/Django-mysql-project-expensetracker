from django.shortcuts import render,redirect
from .services import TrackerServices   #.services means from current directory
import pymysql

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


# def modify(request):
   
#         con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
#         curs=con.cursor()
        
#         curs.execute(f"select * from expenses where userid={uid}")
#         data=curs.fetchall()
#         con.commit()



#         return render(request,'ModifyExpense.html')

def modify(request):
    if request.session.get('authenticated'):
        uid = request.session.get("user")   # logged-in user
        obj = TrackerServices()
        expenses = obj.getAllExpenses(uid)

        return render(request, 'ModifyExpense.html', {
            'expdata': expenses
        })
    else:
        return redirect('/dashboard/')



def ModifyExpense(request):
    if request.method == "POST":
        uid = request.session.get('user')  # user who logged in
        sdt = request.POST.get("expense_date")  # date
        category = request.POST.get("category")
        desc = request.POST.get("description")
        amount = request.POST.get("amount")
        paymentmode = request.POST.get("paymentmode")

        obj = TrackerServices()
        status = obj.modification(uid, sdt, category, desc, amount, paymentmode)
        return render(request, "ExpenseStatus.html", {"status": status})

def generatereports(request):
    # Step 1: Check if user is logged in
    if request.session.get('authenticated'):
        # Step 2: Show the report form page
        return render(request, 'GenerateReports.html')
    else:
        # Step 3: If not logged in, go to dashboard
        return redirect('/dashboard/')

def viewreports(request):
    # Step 1: Check if user is logged in
    if not request.session.get('authenticated'):
        return redirect('/dashboard/')
    
    # Step 2: Check if form was submitted
    if request.method != 'POST':
        return redirect('/dashboard/')
    
    # Step 3: Get user ID
    uid = request.session.get('user')
    
    # Step 4: Get what user selected from form
    preset = request.POST.get("preset")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    category = request.POST.get("category")
    
    # Step 5: If user clicked a quick button, set the dates
    if preset:
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        if preset == 'all':
            start_date = None
            end_date = None
        elif preset == 'last7':
            days_ago = today - timedelta(days=7)
            start_date = days_ago.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif preset == 'last30':
            days_ago = today - timedelta(days=30)
            start_date = days_ago.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif preset == 'thismonth':
            first_day = today.replace(day=1)
            start_date = first_day.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif preset == 'lastmonth':
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            start_date = first_day_last_month.strftime('%Y-%m-%d')
            end_date = last_day_last_month.strftime('%Y-%m-%d')
        elif preset == 'thisyear':
            first_day_year = today.replace(month=1, day=1)
            start_date = first_day_year.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
    
    # Step 6: If no category selected, set to None
    if category == "":
        category = None
    
    # Step 7: Get the report data
    obj = TrackerServices()
    report_data = obj.generateReports(uid, start_date, end_date, category)
    
    # Step 8: Show the report page
    return render(request, 'ViewReports.html', {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'category': category
    })


def delete(request):
    # Check if user is authenticated
    if not request.session.get('authenticated'):
        return redirect('/dashboard/')
    
    # Get user ID from session (using 'user' key as in other functions)
    uid = request.session.get('user')
    
    if not uid:
        return redirect('/dashboard/')
    
    # Fetch expenses from database
    con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
    curs=con.cursor()
    curs.execute("SELECT expenseid,expense_date,category,description,amount,paymentmode FROM expenses WHERE userid=%s ORDER BY expense_date DESC", (uid,))
    expenses=curs.fetchall()
    con.close()
    
    return render(request,'DeleteExpense.html',{'expenses':expenses})

def deleteexpense(request):
    
    if not request.session.get('authenticated'):
        return redirect('/dashboard/')
    
    
    uid = request.session.get('user')
    
    if not uid:
        return redirect('/dashboard/')
    
  
    if request.method == 'POST':
        expenseid = request.POST.get('expenseid')
        if expenseid:
            obj = TrackerServices()
            status = obj.deleteExpense(uid, expenseid)
            # Redirect back to delete page to show updated list
            return redirect('/delete/')
        else:
            return redirect('/delete/')
    else:
        return redirect('/delete/')