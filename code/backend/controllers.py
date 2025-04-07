from flask import Flask, render_template, request,redirect
from flask import current_app as app
from .models import *
from jinja2 import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

@app.route("/")
def home():
    return "<h1>Hello</h1>"

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    if request.method == "POST":
        password = request.form.get("password")
        passwordcorrect = admin.query.filter_by(password = password).first()
        if passwordcorrect:
            return redirect("/admindashboard")
        else:
            return render_template("adminlogin.html",msg="Wrong Password!")
    return render_template("adminlogin.html",msg='')

@app.route("/login",methods=["GET","POST"])
def userlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        customerpasswordcorrect = customer.query.filter_by(username=username,password=password).first()
        professionalpasswordcorrect = professional.query.filter_by(username=username,password=password).first()
        if customerpasswordcorrect:
            return redirect("/customerdashboard/"+str(customerpasswordcorrect.id))
        elif professionalpasswordcorrect:
            return redirect("/profdashboard/"+str(professionalpasswordcorrect.id))
        else:
            return render_template("login.html",msg="Invalid Credentials!")
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def user_register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        phone = request.form.get("phone")
        userpresent = (customer.query.filter_by(username=username).first()) or (professional.query.filter_by(username=username).first())
        if not userpresent:
            new_user = customer(username=username,password=password,full_name=fullname,address=address,pincode=pincode,phone=phone)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="")
        else:
            return render_template("register.html",msg="User already registered")
    return render_template("register.html",msg="")

@app.route("/registerprofessional",methods=["GET","POST"])
def prof_register():
    servicesbytype = fetch_servicesbytype()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        serviceprovided = request.form.get("serviceprovided")
        experience = request.form.get("experience")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        phone = request.form.get("phone")
        userpresent = (customer.query.filter_by(username=username).first()) or (professional.query.filter_by(username=username).first())
        if not userpresent:
            new_user = professional(username=username,password=password,full_name=fullname,address=address,pincode=pincode,phone=phone,service_provided=serviceprovided,experience=experience)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",msg="")
        else:
            return render_template("registerprofessional.html",msg="User already registered",services=servicesbytype)
    return render_template("registerprofessional.html",msg="",services=servicesbytype)

@app.route("/admindashboard", methods=["GET","POST"])
def admindash():
    plot = adminplot()
    plot.savefig("./static/images/admin.jpeg")
    plot.clf()
    plot = adminplot1()
    plot.savefig("./static/images/adminblock.jpeg")
    plot.clf()
    service_summary = fetch_services()
    prof_summary = fetch_professionals()
    requests_summary = fetch_requests()
    if request.method == "POST":
        servicetype = request.form.get("servicetype")
        servicename = request.form.get("servicename")
        price = request.form.get("price")
        if servicetype != None and servicename != None and price != None:
            services_obj = services(service_type=servicetype,service_name=servicename,price=price)
            db.session.add(services_obj)
            db.session.commit()
        editid = request.form.get("editid")
        stype = request.form.get("stype")
        sname = request.form.get("sname")
        eprice = request.form.get("eprice")
        if editid != None and stype!= None and sname != None and eprice != None:
            toedit = services.query.filter_by(id = editid).first()
            toedit.service_type = stype
            toedit.service_name = sname
            toedit.price = eprice
            db.session.commit()
        delid = request.form.get("delid")
        if delid != None:
            todelete = services.query.filter_by(id = delid).first()
            db.session.delete(todelete)
            deletebooked = booked_services.query.filter_by(service_id = delid).all()
            for i in deletebooked:
                db.session.delete(i)
            db.session.commit()
        aid = request.form.get("aid")
        if aid != None:
            toaccept = professional.query.filter_by(id = aid).first()
            toaccept.status = "normal"
            db.session.commit()
        ubid = request.form.get("ubid")
        if ubid != None:
            toaccept = professional.query.filter_by(id = ubid).first()
            toaccept.status = "normal"
            db.session.commit()
        bid = request.form.get("bid")
        if bid != None:
            toaccept = professional.query.filter_by(id = bid).first()
            toaccept.status = "blocked"
            db.session.commit()
        searchtxt = request.form.get("searchtxt")
        if searchtxt != None:
            byname = searchbyname(searchtxt)
            bystatus = searchbystatus(searchtxt)
            print(bystatus)
            if byname != {}:
                prof_summary = byname
                return render_template("admindashboard.html",services=service_summary,professionals=prof_summary,requests=requests_summary)
            elif bystatus != {}:
                prof_summary = bystatus
                return render_template("admindashboard.html",services=service_summary,professionals=prof_summary,requests=requests_summary)
            else:
                prof_summary = {}
                return render_template("admindashboard.html",services=service_summary,professionals=prof_summary,requests=requests_summary)
        return redirect("/admindashboard")
    return render_template("admindashboard.html",services=service_summary,professionals=prof_summary,requests=requests_summary)

@app.route("/customerdashboard/<int:cust_id>", methods=["GET","POST"])
def custdash(cust_id):
    plot = custplot(cust_id)
    plot.savefig("./static/images/cust"+str(cust_id)+".jpeg")
    plot.clf()
    cust_info = fetch_customer_info(cust_id)
    bookedreqs = fetch_requestsbycustomer(cust_id)
    servicesbytype = fetch_servicesbytype()
    if request.method == "POST":
        dateclose = request.form.get("dateclose")
        idfetched = request.form.get("id")
        ratingfetched = request.form.get("rating")
        remarksfetched = request.form.get("remarks")
        if ratingfetched != None:
            service = booked_services.query.filter_by(id=idfetched).first()
            service.date_completed = str(dateclose)
            service.rating_by_customer = int(ratingfetched)
            if remarksfetched:
                service.remarks_by_customer = remarksfetched
            service.status = 'closed'
            db.session.commit()
        sid = request.form.get("id")
        cid = request.form.get("cid")
        datereq = request.form.get("datereq")
        if sid != None and cid != None:
            addservice = booked_services(service_id=sid,customer_id=cid,date_requested=datereq)
            db.session.add(addservice)
            db.session.commit()
        searchtxt = request.form.get("searchtxt")
        if searchtxt != None:
            byservicename = searchbyservicename(cust_id,searchtxt)
            byservicestatus = searchbyservicestatus(cust_id,searchtxt)
            if byservicename != {}:
                bookedreqs = byservicename
                return render_template("customerdashboard.html",id=cust_info.id,name = cust_info.full_name.split()[0],service_history=bookedreqs,offered=servicesbytype)
            elif byservicestatus != {}:
                bookedreqs = byservicestatus
                return render_template("customerdashboard.html",id=cust_info.id,name = cust_info.full_name.split()[0],service_history=bookedreqs,offered=servicesbytype)
            else:
                bookedreqs = {}
                return render_template("customerdashboard.html",id=cust_info.id,name = cust_info.full_name.split()[0],service_history=bookedreqs,offered=servicesbytype)
        return redirect("/customerdashboard/"+str(cust_id))
    return render_template("customerdashboard.html",id=cust_info.id,name = cust_info.full_name.split()[0],service_history=bookedreqs,offered=servicesbytype)

@app.route("/profdashboard/<int:prof_id>", methods=["GET","POST"])
def profdash(prof_id):
    plot = plotprof(prof_id)
    plot.savefig("./static/images/prof"+str(prof_id)+".jpeg")
    plot.clf()
    if request.method == "POST":
        aid = request.form.get("aid")
        if aid != None:
            toaccept = booked_services.query.filter_by(id=aid).first()
            toaccept.prof_id = prof_id
            toaccept.status = 'accepted'
            db.session.commit()
        return redirect("/profdashboard/"+str(prof_id))
    thisprof = professional.query.filter_by(id=prof_id).first()
    servicesbytype = fetch_servicesbytype()
    servicesfetched = fetch_services()
    thisprofservicetype = servicesbytype[thisprof.service_provided]
    serviceidlist = []
    fetchbooked = []
    senddict = {}
    for i in thisprofservicetype:
        serviceidlist.append(i[2])
    for i in serviceidlist:
        x = booked_services.query.filter_by(service_id=i).all()
        for j in x:
            fetchbooked.append(j)
    for i in fetchbooked:
        senddict[i.id] = [fetch_customer_info(i.customer_id).full_name,fetch_customer_info(i.customer_id).phone,servicesfetched[i.service_id][0]+"-"+servicesfetched[i.service_id][1],fetch_customer_info(i.customer_id).address,i.date_requested,i.status,i.prof_id==prof_id,i.date_completed,i.rating_by_customer,i.remarks_by_customer,fetch_customer_info(i.customer_id).pincode]
    if fetch_professionals()[prof_id][4] == "waiting":
        return ("<h1>Please wait for approval</h1>")
    if fetch_professionals()[prof_id][4] == "blocked":
        return ("<h1>You have been blocked</h1>")
    return render_template("professionaldashboard.html",name=thisprof.full_name.split(" ")[0],servicesent=senddict,profid=prof_id,avgrate=avgrating(prof_id))



def fetch_services():
    servicesfetched = services.query.filter_by().all()
    servicelist= {}
    for service in servicesfetched:
        if service.id not in servicelist.keys():
            servicelist[service.id] = [service.service_type,service.service_name,service.price]
    return servicelist

def fetch_customer_info(id):
    custinfo = customer.query.filter_by(id=id).first()
    return custinfo


def fetch_professionals():
    professionalsfetched = professional.query.filter_by().all()
    proflist = {}
    for prof in professionalsfetched:
        if prof.id not in proflist.keys():
            proflist[prof.id] = [prof.full_name,prof.experience,prof.service_provided,prof.phone,prof.status,avgrating(prof.id),count_services_completed(prof.id)]
    return proflist

def fetch_requests():
    requestsfetched = booked_services.query.filter_by().all()
    reqlist = {}
    profs = fetch_professionals()
    for request in requestsfetched:
        if request.id not in reqlist.keys():
            if request.prof_id:
                reqlist[request.id] = [profs[request.prof_id][0],request.date_requested,request.status]
            else:
                reqlist[request.id] = ["-",request.date_requested,request.status]
    return reqlist

def fetch_requestsbycustomer(cust_id):
    requestsfetched = booked_services.query.filter_by(customer_id=cust_id).all()
    reqlist = {}
    profs = fetch_professionals()
    service = fetch_services()
    for request in requestsfetched:
        if request.id not in reqlist.keys():
            if request.prof_id:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],profs[request.prof_id][0],profs[request.prof_id][3],request.status]
            else:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],"-","-",request.status]
    return reqlist

def fetch_servicesbytype():
    servicesfetched = services.query.filter_by().all()
    servicedic = {}
    for service in servicesfetched:
        if service.service_type not in servicedic.keys():
            servicedic[service.service_type] = [[service.service_name,service.price,service.id]]
        else:
            servicedic[service.service_type].append([service.service_name,service.price,service.id])
    return servicedic

def count_services_completed(profid):
    return booked_services.query.filter_by(prof_id=profid,status="closed").count()

def avgrating(profid):
    fetch = booked_services.query.filter_by(prof_id=profid,status="closed").all()
    sum = 0
    for i in fetch:
        sum = sum + i.rating_by_customer
    if count_services_completed(profid)>0:
        return round((sum/count_services_completed(profid)),2)
    else:
        return 0
    
def searchbyservicename(cid,text):
    service = fetch_services()
    requestsfetched = requestsfetched = booked_services.query.filter(booked_services.id.ilike(f"%{text}%")).all()
    reqlist = {}
    profs = fetch_professionals()
    service = fetch_services()
    for request in requestsfetched:
        if request.id not in reqlist.keys():
            if request.prof_id:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],profs[request.prof_id][0],profs[request.prof_id][3],request.status,request.customer_id]
            else:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],"-","-",request.status,request.customer_id]
    toremove = []
    for key in reqlist.keys():
        if reqlist[key][4] != cid:
            toremove.append(key)

    for i in toremove:
        reqlist.pop(i)
    return reqlist

def searchbyservicestatus(cid,text):
    service = fetch_services()
    requestsfetched = requestsfetched = booked_services.query.filter(booked_services.status.ilike(f"%{text}%")).all()
    reqlist = {}
    profs = fetch_professionals()
    service = fetch_services()
    for request in requestsfetched:
        if request.id not in reqlist.keys():
            if request.prof_id:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],profs[request.prof_id][0],profs[request.prof_id][3],request.status,request.customer_id]
            else:
                reqlist[request.id] = [service[request.service_id][0]+" - "+service[request.service_id][1],"-","-",request.status,request.customer_id]
    toremove = []
    for key in reqlist.keys():
        if reqlist[key][4] != cid:
            toremove.append(key)

    for i in toremove:
        reqlist.pop(i)
    return reqlist

def searchbyname(text):
    professionalsfetched = professional.query.filter(professional.full_name.ilike(f"%{text}%")).all()
    proflist = {}
    for prof in professionalsfetched:
        if prof.id not in proflist.keys():
            proflist[prof.id] = [prof.full_name,prof.experience,prof.service_provided,prof.phone,prof.status,avgrating(prof.id),count_services_completed(prof.id)]
    return proflist

def searchbystatus(text):
    professionalsfetched = professional.query.filter(professional.status.ilike(f"%{text}%")).all()
    proflist = {}
    for prof in professionalsfetched:
        if prof.id not in proflist.keys():
            proflist[prof.id] = [prof.full_name,prof.experience,prof.service_provided,prof.phone,prof.status,avgrating(prof.id),count_services_completed(prof.id)]
    return proflist

def profchart(profid):
    closed = booked_services.query.filter_by(prof_id=profid,status="closed").count()
    accepted = booked_services.query.filter_by(prof_id=profid,status="accepted").count()

    return [accepted,closed]

def plotprof(prof_id):
    yaxis = profchart(prof_id)
    xaxis = ["Accepted","Completed"]
    plt.bar(xaxis, yaxis,color=['orange','green'])
    plt.title("Services Accepted/Completed")
    plt.ylabel("No. of services")
    return plt

def custchart(custid):
    req = booked_services.query.filter_by(customer_id=custid,status="requested").count()
    closed = booked_services.query.filter_by(customer_id=custid,status="closed").count()
    accepted = booked_services.query.filter_by(customer_id=custid,status="accepted").count()
    return [req,accepted,closed]

def custplot(custid):
    yaxis = custchart(custid)
    xaxis = ["Reqested","Accepted","Completed"]
    plt.bar(xaxis, yaxis,color=['orange','blue','green'])
    plt.title("Services Requested/Accepted/Completed")
    plt.ylabel("No. of services")
    return plt

def adminchart():
    req = booked_services.query.filter_by(status="requested").count()
    closed = booked_services.query.filter_by(status="closed").count()
    accepted = booked_services.query.filter_by(status="accepted").count()
    return [req,accepted,closed]

def adminplot():
    yaxis = adminchart()
    xaxis = ["Reqested","Accepted","Completed"]
    plt.bar(xaxis, yaxis)
    plt.title("Services Requested/Accepted/Completed")
    plt.ylabel("No. of services")
    return plt

def adminchart1():
    waiting = professional.query.filter_by(status="waiting").count()
    blocked = professional.query.filter_by(status="blocked").count()
    normal = professional.query.filter_by(status="normal").count()
    return [waiting,blocked,normal]

def adminplot1():
    yaxis = adminchart1()
    xaxis = ["Waiting","Blocked","Normal"]
    plt.bar(xaxis, yaxis,color=['orange','red','green'])
    plt.title("Professional Status")
    plt.ylabel("No. of Accounts")
    return plt