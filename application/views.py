from django.shortcuts import render, redirect
from . import logic
import mysql.connector as mysql
from django.contrib.auth.decorators import login_required
from .models import MedicineDet
from django.contrib.auth import logout

id = ''
license = ''
name = ''
username = ''
add = ''
owner = ''
contact = ''
password = ''

# For login action for Medicals
def loginaction(request):
    global username, password
    if request.method == 'POST':
        m = mysql.connect(host="localhost", user="root", password="Idevansh@22", database="medicals")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == 'Username':
                username = value
            if key == 'Password':
                password = value
        c = f"select * from owners where Username='{username}' and Password='{password}'"
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        request.session['logindetails'] = {'medshop': t[0][2], 'medadd': t[0][4], 'medowner': t[0][5], 'medcontact': t[0][6]}

        if t==():
            return render(request, 'application/index.html')
        else:
            return redirect('pharmafriend:addnames')
    return render(request, 'application/login_med.html')


# For signup action of Medicals
def signupaction(request):
    global id, license, name, username, add, owner, contact, password
    if request.method == 'POST':
        m = mysql.connect(host="localhost", user="root", password="Idevansh@22", database="medicals")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == 'ID':
                id = value
            if key == 'License':
                license = value
            if key == 'Name':
                name = value
            if key == 'Username':
                username = value
            if key == 'Address':
                add = value
            if key == 'Owner':
                owner = value
            if key == 'Contact':
                contact = value
            if key == 'Password':
                password = value
        c = f"insert into owners(ID, License, Name, Username, Adress, Owner, Contact, Password) Values('{id}','{license}','{name}','{username}','{add}','{owner}','{contact}','{password}')"
        cursor.execute(c)
        m.commit()
    return render(request, 'application/signup_med.html')

def logoutmeds(request):
    logout(request)
    return redirect('pharmafriend:homepage')

def Homepage(request):
    return render(request, 'application/index.html')

def Pharmacy(request):
    return render(request, 'application/pharmacy.html')

# For medicals to add medicines
def AddMeds(request):
    print("Login Done")
    if request.method == 'POST':
        print("Login done")
        # get user inputs
        medicalshop = request.POST.get('shopname')
        medicalowner = request.POST.get('medown')
        medicalcontact = request.POST.get('medcontact')
        medicaladdress = request.POST.get('medadd')
        medicinename = str(request.POST.get('medname')).lower()
        medicinepower = request.POST.get('medpow')
        medicinextra = request.POST.get('medext')
        medicinquant = request.POST.get('medquan')
        medicineexp = request.POST.get('medexp')

        # create objects for models
        m = MedicineDet(medadd=medicaladdress,medowner=medicalowner,medcontact=medicalcontact,medshop=medicalshop,medname=medicinename,medextra=medicinextra,medpow=medicinepower,medquan=medicinquant,medexp=medicineexp)
        m.save()

        return redirect('pharmafriend:addnames')

    return render(request, 'application/addmeds.html')


# To locate Pharmacies
def Locate(request):
    if request.method == 'POST':
        medicine_name1 = str(request.POST['medicine-name'])
        medicine_name1.lower()
        aquery = MedicineDet.objects.filter(medname__startswith = medicine_name1)
        a = aquery.values_list()
        
        pharma = []
        for i in range(len(a)):
            pharmatemp = {}
            pharmatemp.update({"No": i+1, "MedAdd": a[i][1], "Medown": a[i][2], "Medcontact": a[i][3]
            ,"MedName": a[i][4],"MedAbr": a[i][6] + ' ' + str(a[i][7]),"MedQuan": a[i][8]})
            pharma.append(pharmatemp)
        
        context = {'pharmalist': pharma}
        return render(request, 'application/medical.html', context=context)
    return render(request, 'application/medical.html')

# To search Medicine 
def Search(request):
    if request.method == 'POST':
        medicine_name = request.POST['contact-name']
        if len(medicine_name) == 0:
            return redirect('pharmafriend:searchpage')
    # request.session.medicine
        if len(medicine_name) != 0:
            Search.med_name_mrp, Search.med_name_link = logic.didyoumean(medicine_name)
            request.session['medicine'] = Search.med_name_mrp
            return redirect('pharmafriend:storepage')
        else:
            return render(request, 'application/search-med.html')
    return render(request, 'application/search-med.html')


# To get Medicine Info
def Store(request):
    if request.method == 'POST':
        Store.medicine_selected = request.POST['meddropdown']
        medlink = Search.med_name_link[Store.medicine_selected]
        meddetails = logic.getinfo_onemg(medlink)
        Store.apollo, apolloops, Store.netmeds, netmedsops, Store.pharm, pharmops = logic.combined(Store.medicine_selected)
        
        request.session['medicineinfo'] = meddetails
        request.session['compareapolloops'] = apolloops
        request.session['comparenetmedsops'] = netmedsops
        request.session['comparepharmops'] = pharmops

        return redirect('pharmafriend:medicinepage')
    else:
        return render(request, 'application/shop.html')
        
# For comparision
def Medicine(request):
    if request.method == 'POST':
        medicine_selected_apollo = request.POST['meddropdownapollo']
        medicine_selected_pharm = request.POST['meddropdownpharm']
        medicine_selected_netmeds = request.POST['meddropdownnetmeds']
        
        apollo_details = Store.apollo[medicine_selected_apollo]
        pharm_details = Store.pharm[medicine_selected_pharm]
        netmeds_details = Store.netmeds[medicine_selected_netmeds]

        context = {"apollodet": apollo_details, "pharmdet": pharm_details, "netmedsdet": netmeds_details}
        # context1 = {"apollodet": medicine_selected_apollo, "pharmdet": medicine_selected_pharm, "netmedsdet": medicine_selected_netmeds}
        return render(request, 'application/comparison.html', context=context)
    else:
        pass
    return render(request, 'application/comparison.html')

# To search for government Kendras
def GovMeds(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            #Handle Elements from first Form
            GovMeds.state_name_main = request.POST['govdropdownstate']
            dist_list = logic.getgovdist(GovMeds.state_name_main)
            context = {"districts": dist_list}
            return render(request, 'application/gov-vendor.html', context=context)

        if request.POST.get("form_type") == 'formTwo':
            dist_name = request.POST['govdropdowndistrict']
            govmeds = logic.getgovmeds(GovMeds.state_name_main, dist_name)
            govproducts, num = logic.getgovproducts()
            context1 = {"govmeds": govmeds, "govproducts": govproducts, "total": num}
            return render(request, 'application/gov-vendor.html', context=context1)


    return render(request, 'application/gov-vendor.html')

# To send email to doctor
@login_required(login_url = "accounts:loginuser")
def Doctor(request):
    user = request.user
    context = {
        'email': user.email
    }
    return render(request, 'application/doc-advice.html', context=context)

# About page
def About(request):
    return render(request, 'application/about.html')

# Contach us page
def Contact(request):
    return render(request, 'application/contact.html')

def error_400(request, exception):
    return render(request, 'application/errorpage.html')

def error_404(request, exception):
    return render(request, 'application/errorpage.html')

def error_500(request):
    return render(request, 'application/errorpage.html')