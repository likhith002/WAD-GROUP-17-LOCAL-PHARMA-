from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from localpharma.models import pharmacyowner
from localpharma.models import customer
from localpharma.models import contactus
from localpharma.models import pharmacymedicine
from localpharma.models import medicine
from django.contrib.auth.models import User, auth
from django.http import JsonResponse


# Create your views here.

# function to check whether user is customer or pharmacy owner

def check_query(request):
    if request.user.is_authenticated:

        if customer.objects.filter(email=request.user.email):  # checking whether email is registered or not
            c = customer.objects.get(email=request.user.email)  # retrieving objects from database
            name = c.firstname
            return render(request, 'customer_query.html',
                          {'Name': name})  # passing name to customer query page and going to it

        else:
            po = pharmacyowner.objects.get(email=request.user.email)  # retrieving objects from database
            name = po.firstname
            return render(request, 'pharmacy_query.html', {
                'Name': name})  # Combines the given pharmacy_query.html with name returns HttpResponse object.
    else:
        return render(request, 'homepage.html')  # rendering to home page

#-----------------------------------------------------------------------------------------------------------------------

def homepage(request):
    return render(request, 'homepage.html')  # rendering to home page


#-----------------------------------------------------------------------------------------------------------------------




def pharmacy_query(request):
    return render(request, 'pharmacy_query.html')  # rendering to pharmacy query page


#-----------------------------------------------------------------------------------------------------------------------



def customer_login(request):
    if request.method == "POST":  # post method is used for security
        username = request.POST['username']   # takes username and password from user
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)  # authenticating using username and password

        if user is not None:
            auth.login(request, user)
            U = User.objects.get(username=username)  # retrieving objects from database

            if customer.objects.filter(email=U.email):      # to get the object having that username
                c = customer.objects.get(email=U.email)
                name = c.firstname
                request.session['ceid'] = U.email  # Using session to access the variable in other functions

                return render(request, 'customer_query.html', {
                    'Name': name})  # Combines the given customer_query.html with name returns HttpResponse object.

            else:
                messages.info(request, "INVALID CREDENTIALS")  # shows messages in html page
                return render(request, 'customer_login.html')  # Renders to customer_login.html page

        else:
            messages.info(request, "INVALID CREDENTIALS")  # shows messages in html page
            return render(request, 'customer_login.html')  # Renders to customer_login.html page

    else:
        return render(request, 'customer_login.html')  # Renders to customer_login.html page



#-----------------------------------------------------------------------------------------------------------------------





def pharmacy_login(request):
    if request.method == "POST":  # post method is used for security
        username = request.POST['username']
        password = request.POST['password']             # takes username and password from user
        user = auth.authenticate(username=username,
                                 password=password)  # authentication is done using username and password

        if user is not None:
            auth.login(request, user)
            U = User.objects.get(username=username)  # retrieving objects from database

            if pharmacyowner.objects.filter(email=U.email):  # checking whether email is registered or not
                po = pharmacyowner.objects.get(email=U.email)
                name = po.firstname
                request.session['peid'] = U.email
                return render(request, 'pharmacy_query.html', {
                    'Name': name})  # Combines the given customer_query.html with name returns HttpResponse object.

            else:
                messages.info(request, "INVALID CREDENTIALS")  # shows messages in html page
                return redirect('/pharmacy_login.html')


        else:
            messages.info(request, "INVALID CREDENTIALS")  # shows messages in html page
            return redirect('/pharmacy_login.html')  # Redirects to pharmacy login page
    else:

        return render(request, 'pharmacy_login.html')  # Redirects to Pharmacy login page




#-----------------------------------------------------------------------------------------------------------------------


def commonloginpage(request):
    return render(request, 'commonloginpage.html')  # Renders to Common login page






#-----------------------------------------------------------------------------------------------------------------------

def services(request):
    return render(request, 'services.html')  # Renders to services page




#-----------------------------------------------------------------------------------------------------------------------



def contact(request):
    if request.method == "POST":  # Post method is used for security
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        query = request.POST['query']
        obj = contactus(name=name, phone=phone, email=email, query=query)
        obj.save()  # Save() helps to store the data in the database
        print("data have been written to DB successfully")
        return redirect('/contact.html')  # Redirects to contact page

    else:
        return render(request, 'contact.html')  # Renders to contacts page

    # -----------------------------------------------------------------------------------------------------------------------


def reegister_pharmacy(request):
    if request.method == "POST":  # Post method is used for security

        username = request.POST['username']
        firstname = request.POST['firstname']
        middlename = request.POST['middlename']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST.get('gender', "Male")

        DOB = request.POST['DOB']
        phone1 = request.POST['phone1']
        phone2 = request.POST['phone2']
        password = request.POST['password']
        city = request.POST['city']
        streetno = request.POST['streetno']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        shopname = request.POST['shopname']

        if pharmacyowner.objects.filter(email=email).exists():  # checking whether email is registered or not
            messages.info(request, "Email alredy exists please provide another Email")  # shows messages in html page
            print("Email alredy exists please provide another Email")  # Redirects to pharmacy register page
            return redirect('/reegister_pharmacy.html')

        if User.objects.filter(username=username).exists():  # checking whether email is registered or not
            messages.info(request, "Username already exists please provide another")  # shows messages in html page
            return redirect('/reegister_pharmacy.html')  # Redirects to pharmacy register page

        if User.objects.filter(email=email).exists():  # checking whether email is registered or not
            messages.info(request, "Email already exists please provide another")  # shows messages in html page
            return redirect('/reegister_pharmacy.html')  # Redirects to pharmacy register page



        else:

            obj = pharmacyowner(firstname=firstname, gender=gender, middlename=middlename, lastname=lastname,
                                email=email, DOB=DOB, phone1=phone1, phone2=phone2, city=city, streetno=streetno,
                                state=state, country=country, pincode=pincode, shopname=shopname)
            obj.save()  # Save() helps to store the data in the database
            User.objects.create_user(username=username, password=password,
                                     email=email).save()  # Save() helps to store the data in the database
            print("data has been written to DB Successfully")
            return redirect('/pharmacy_login.html')  # Redirects to pharmacy login page
    else:
        return render(request, 'reegister_pharmacy.html')  # Renders to pharmacy register page




#-----------------------------------------------------------------------------------------------------------------------


def register_customer(request):
    if request.method == "POST":  # Post method is used for security

        username = request.POST['username']
        firstname = request.POST['firstname']
        middlename = request.POST['middlename']
        lastname = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST.get('gender', "Male")

        DOB = request.POST['DOB']
        phone1 = request.POST['phone1']
        phone2 = request.POST['phone2']
        password = request.POST['password']
        city = request.POST['city']
        streetno = request.POST['streetno']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']

        if customer.objects.filter(email=email).exists():  # checking whether email is registered or not
            messages.info(request, "Email already exists please provide another Email")  # shows messages in html page
            return redirect('/register_customer.html')  # Redirects to customer registration page

        if User.objects.filter(username=username).exists():  # checking whether email is registered or not
            messages.info(request, "Username already exists please provide another")  # shows messages in html page
            return redirect('/register_customer.html')  # Redirects to customer registration page

        if User.objects.filter(email=email).exists():  # checking whether email is registered or not
            messages.info(request, "Email already exists please provide another")  # shows messages in html page
            return redirect('/register_customer.html')  # Redirects to customer registration page

        else:
            obj = customer(firstname=firstname, gender=gender, middlename=middlename, lastname=lastname, email=email,
                           DOB=DOB, phone1=phone1, phone2=phone2, city=city, streetno=streetno, state=state,
                           country=country, pincode=pincode)
            obj.save()  # Save() helps to store the data in the database
            User.objects.create_user(username=username, password=password,
                                     email=email).save()  # Save() helps to store the data in the database
            print("data has been written to DB Successfully")
            return redirect('/customer_login.html')  # Redirects to customer login page
    else:
        return render(request, 'register_customer.html')  # Renders to customer registration page




#-----------------------------------------------------------------------------------------------------------------------
# function to add medicines into DB

def add(request):
    if request.method == "POST":  # Post method for security

        price = request.POST['price']
        quantity = request.POST['quantity']
        mn = request.POST['mid']
        peid = request.session['peid']  # retrieveing variable using session

        obj2 = pharmacyowner.objects.get(email=peid)

        if pharmacymedicine.objects.filter(eid=peid, mid=mn):  # checking whether medicine,email is registered or not
            messages.error(request, "medicine you are adding is already present",
                           extra_tags='add_error')  # shows messages in html page

        else:

            obj = pharmacymedicine(eid=peid, price=price, quantity=quantity, mid=mn, pin=obj2.pincode,
                                   firstname=obj2.firstname, middlename=obj2.middlename, lastname=obj2.lastname,
                                   phone1=obj2.phone1, streetno=obj2.streetno, city=obj2.city, state=obj2.state,
                                   shopname=obj2.shopname)
            obj.save()  # Save() helps to store the data in the database
            messages.success(request, "Medicine added successfully",
                             extra_tags='add_success')  # shows messages in html page
            print("data written to database successfully")

        if pharmacyowner.objects.filter(email=peid):  # checking whether email is registered or not
            po = pharmacyowner.objects.get(email=peid)
            name = po.firstname

            return render(request, 'pharmacy_query.html', {
                'Name': name})  # Combines the given pharmacy_query.html with name returns and HttpResponse object.



#-----------------------------------------------------------------------------------------------------------------------



def edit(request):
    if request.method == "POST":  # Post method is used for security
        price = request.POST['price']
        quantity = request.POST['quantity']
        mid = request.POST['mid']
        peid = request.session['peid']  # retrieveing variable using session

        if pharmacymedicine.objects.filter(mid=mid,
                                           eid=peid):  # checking whether medicine,email is present in database or not
            obj = pharmacymedicine.objects.get(mid=mid, eid=peid)
            obj.price = price
            obj.quantity = quantity
            obj.save()  # Save() helps to store the data in the database

            messages.info(request, "Medicine updated successfully",
                          extra_tags='update_success')  # shows messages in html page

            if pharmacyowner.objects.filter(email=peid):
                po = pharmacyowner.objects.get(email=peid)
                name = po.firstname
                return render(request, 'pharmacy_query.html', {
                    'Name': name})  # Combines the given pharmacy_query.html with name and returns HttpResponse object.

        else:
            po = pharmacyowner.objects.get(email=peid)
            name = po.firstname
            messages.info(request, "The medicine you are updating is not present in your record please add it",
                          extra_tags='update_error')  # shows messages in html page
            return render(request, 'pharmacy_query.html', {
                'Name': name})  # Combines the given pharmacy_query.html with name and returns HttpResponse object.



#-----------------------------------------------------------------------------------------------------------------------



def delete(request):
    if request.method == "POST":  # Post method is used for security

        mid = request.POST['mid']
        peid = request.session['peid']

        if pharmacymedicine.objects.filter(mid=mid, eid=peid):  # checking either medicine,email is registered or not

            obj = pharmacymedicine.objects.get(mid=mid)
            obj.delete()
            messages.error(request, "Medicine deleted successfully",
                           extra_tags='delete_success')  # shows messages in html page

            if pharmacyowner.objects.filter(email=peid):  # checking either email is registered or not
                po = pharmacyowner.objects.get(email=peid)
                name = po.firstname
                return render(request, 'pharmacy_query.html', {'Name': name})  # Renders to pharmacy query page

        else:
            po = pharmacyowner.objects.get(email=peid)
            name = po.firstname
            messages.error(request, "The medicine you are deleting is not present in your record please add it",
                           extra_tags='delete_error')  # shows messages in html page
            return render(request, 'pharmacy_query.html', {'Name': name})  # Renders to pharmacy query page


#-----------------------------------------------------------------------------------------------------------------------


#function for autocomplete

def autocomplete(request):
    if 'term' in request.GET:
        obj = medicine.objects.filter(name__istartswith=request.GET.get('term'))
        medicines = list()  # display a list of all medicines starting with term
        for medi_name in obj:
            medicines.append(medi_name.name)  # append the medicine containing term into list

        return JsonResponse(medicines, safe=False)   # return a dropdown with nedicines

    return render(request, 'pharmacy_query.html')  # Renders to pharmacy query page



#-----------------------------------------------------------------------------------------------------------------------



def customer_search(request):
    if 'term' in request.GET:
        obj = medicine.objects.filter(name__istartswith=request.GET.get('term'))
        medicines = list()  # display a list of all medicines starting with term
        for medi_name in obj:
            medicines.append(medi_name.name)      # append the medicine containing term into list

        return JsonResponse(medicines, safe=False)  # return a dropdown with nedicines


    return render(request, 'customer_query.html')  # Renders to pharmacy query page



#-----------------------------------------------------------------------------------------------------------------------


def customer_query(request):
    if request.method == "POST":  # Post method is used for security

        mide = request.POST['mid']

        obj = medicine.objects.get(name=mide)
        medi_data = {}
        medi_data["mname"] = obj.manufacturer_name
        medi_data["type"] = obj.type
        medi_data["price"] = obj.price
        medi_data["name"] = obj.name
        medi_data["scomp"] = obj.short_composition
        medi_data["psize"] = obj.pack_size_label
        medi_data["prescription"] = obj.isprescriptionrequired
        medi_data["image"] = obj.image_url

        ceid = request.session['ceid']

        request.session['medicinename'] = mide

        po = customer.objects.get(email=ceid)

        name = po.firstname
        cpin = po.pincode

        obj = medicine.objects.get(name=mide)

        pd = pharmacymedicine.objects.filter(mid=mide, pin=cpin)
        for k in range(-5, 5, 1):  # for showing pharmacies from nearby pincode areas
            pd = pd | pharmacymedicine.objects.filter(mid=mide, pin=str(int(cpin) + k))

        parameters = {'medi_data': medi_data, 'Name': name, 'pdetailes': pd}

        return render(request, 'customer_query.html',
                      parameters)  # Combines the given customer_query.html with parameters and returns HttpResponse object with that rendered text.

    return render(request, 'customer_query.html')  # Renders to customer query page

#-----------------------------------------------------------------------------------------------------------------------

# logout the user

def logout(request):
    auth.logout(request)
    return redirect('homepage.html')  # Redirects to home page.

#-----------------------------------------------------------------------------------------------------------------------

def check_change_password(request):
    if request.user.is_authenticated:
        if customer.objects.filter(email=request.user.email):  # checking either email is registered or not
            return render(request, 'change_password.html')  # Renders to change password page

        else:
            po = pharmacyowner.objects.get(email=request.user.email)
            return render(request, 'change_password.html')  # Renders to change password page

#-----------------------------------------------------------------------------------------------------------------------



def change_password(request):
    if request.method == "POST":  # Post method is used for security
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            u = User.objects.get(email=request.user.email)  # retrieveing object by checking email
            u.set_password(password2)
            u.save()  # Save() helps to store the data in the database
            return render(request, 'commonloginpage.html')  # Renders to common login page

        else:
            messages.info(request, "Passwords didnot match")  # shows messages in html page


    else:
        return render(request, 'changepassword.html')  # Renders to change password page

#-----------------------------------------------------------------------------------------------------------------------


def profile(request):
    if request.user.is_authenticated:

        if customer.objects.filter(email=request.user.email):  # checking either email is registered or not
            email = request.session['ceid']  # accessing using session

            obj = customer.objects.get(email=email)
            data = {}
            data["fname"] = obj.firstname
            data["lname"] = obj.lastname
            data["gender"] = obj.gender
            data["pno"] = obj.phone1
            data["city"] = obj.city
            data["state"] = obj.state
            data["country"] = obj.country
            data["email"] = obj.email
            data["DOB"] = obj.DOB
            data["pincode"] = obj.pincode

            return render(request, 'customer_profile.html', {
                'data': data})  # Combines the given customer_profile.html with data and returns HttpResponse object with that rendered text.

        else:
            peid = request.session['peid']  # accessing using session

            obj = pharmacyowner.objects.get(email=peid)
            data = {}
            data["fname"] = obj.firstname
            data["lname"] = obj.lastname
            data["gender"] = obj.gender
            data["pno"] = obj.phone1
            data["city"] = obj.city
            data["state"] = obj.state
            data["country"] = obj.country
            data["email"] = obj.email
            data["sname"] = obj.shopname
            data["DOB"] = obj.DOB
            data["pincode"] = obj.pincode
            data["license_file"] = obj.license_file
            data["permission_file"] = obj.permission_file
            return render(request, 'pharmacy_profile.html', {
                'data': data})  # Combines the given pharmacy_profile.html with data and returns HttpResponse object with that rendered text.



    else:

        return render(request, 'homepage.html')  # Renders to home page



#-----------------------------------------------------------------------------------------------------------------------


def show_meds(request):
    email = request.session['peid']  # accessing using session
    if pharmacymedicine.objects.filter(eid=email):  # checking either email is registered or not
        queryset = pharmacymedicine.objects.filter(eid=email)
        context = {
            'queryset': queryset,
        }

        return render(request, 'medicine.html',
                      context)  # Combines the given medicine.html with context and returns HttpResponse object with that rendered text.

    else:
        return render(request, 'medicine.html')  # Renders to medicine.html page


# url:complete detailes


#-----------------------------------------------------------------------------------------------------------------------


def complete_detailes(request):
    mname = request.session['medicinename']
    obj = medicine.objects.get(name=mname)
    medi_data = {}
    medi_data["mediname"] = obj.manufacturer_name
    medi_data["type"] = obj.type
    medi_data["price"] = obj.price
    medi_data["name"] = obj.name
    medi_data["scomp"] = obj.short_composition
    medi_data["psize"] = obj.pack_size_label
    medi_data["prescription"] = obj.isprescriptionrequired
    medi_data["image"] = obj.image_url
    # ---------------------------------------------------------------
    medi_data["side_effects"] = eval(obj.side_effects)
    medi_data["alternate"] = eval(obj.alternate_brands)
    medi_data["benefits"] = eval(obj.benefits)
    medi_data["uses"] = eval(obj.uses)
    medi_data["storage"] = obj.storage_conditions
    medi_data["salt"] = obj.salt_composition

    return render(request, 'complete_medicines.html', {
        'medi_data': medi_data})  # Combines the given complete_medicines.html with medi_data and returns HttpResponse object with that rendered text.

#-----------------------------------------------------------------------------------------------------------------------


def edit_profile(request):
    return render(request, 'edit_profile.html')  # Renders to edit_profile.html page



#-----------------------------------------------------------------------------------------------------------------------

def edit_customer_profile(request):
    return render(request, 'edit_customer_profile.html')  # Renders to edit_customer_profile.html page


#-----------------------------------------------------------------------------------------------------------------------

def check_update(request):
    if request.user.is_authenticated:

        if customer.objects.filter(email=request.user.email):  # checking whether email is registered or not
            return render(request, 'edit_customer_profile.html')  # Renders to edit_customer_profile.html page

        else:
            return render(request, 'edit_profile.html')  # Renders to edit_profile.html page




#-----------------------------------------------------------------------------------------------------------------------

def profile_update(request):
    if request.user.is_authenticated:

        if customer.objects.filter(email=request.user.email):  # checking whether email is registered or not
            email = request.session['ceid']  # accessing using session
            if request.method == "POST":  # Post method is used for security

                firstname = request.POST['firstname']  # Post method helps to access data from html page
                middlename = request.POST['middlename']
                lastname = request.POST['lastname']
                phone1 = request.POST['phone1']
                phone2 = request.POST['phone2']
                city = request.POST['city']
                streetno = request.POST['streetno']
                state = request.POST['state']
                country = request.POST['country']
                pincode = request.POST['pincode']

                if customer.objects.filter(email=email):       #check wheather the user exists or not
                    obj = customer.objects.get(email=email)
                    obj.firstname = firstname
                    obj.middlename = middlename
                    obj.lastname = lastname
                    obj.phone1 = phone1
                    obj.phone2 = phone2
                    obj.streetno = streetno
                    obj.state = state
                    obj.city = city
                    obj.country = country
                    obj.pincode = pincode
                    obj.save()  # saves data in database

                    return render(request, 'homepage.html')  # Renders to homepage.html

                else:
                    messages.info(request,
                                  "The information you are updating is not present in your record please add it",
                                  extra_tags='update_error')  # shows messages
                    return render(request, 'edit_customer_profile.html')  # Renders to edit_customer_profile.html page
        else:
            if request.method == "POST":  # Post method is used for security
                firstname = request.POST['firstname']  # Post method helps to access data from html page
                middlename = request.POST['middlename']  # Post method helps to access data from html page
                lastname = request.POST['lastname']
                phone1 = request.POST['phone1']
                phone2 = request.POST['phone2']
                city = request.POST['city']
                streetno = request.POST['streetno']
                state = request.POST['state']
                license_file = request.FILES['license_file']
                permission_file = request.FILES['permission_file']
                country = request.POST['country']
                pincode = request.POST['pincode']
                shopname = request.POST['shopname']
                peid = request.session['peid']
                if pharmacyowner.objects.filter(email=peid):            #check wheather the user exists or not
                    obj = pharmacyowner.objects.get(email=peid)
                    obj.firstname = firstname
                    obj.middlename = middlename
                    obj.lastname = lastname
                    obj.phone1 = phone1
                    obj.phone2 = phone2
                    obj.license_file = license_file
                    obj.permission_file = permission_file
                    obj.streetno = streetno
                    obj.state = state
                    obj.city = city
                    obj.country = country
                    obj.pincode = pincode
                    obj.shopname = shopname
                    obj.save()  # saves data in database

                    return render(request, 'homepage.html')  # Renders to homepage.html

                else:
                    messages.info(request,
                                  "The information you are updating is not present in your record please add it",
                                  extra_tags='update_error')  # shows messages
                    return render(request, 'edit_profile.html')  # Renders to edit_profile.html

                # -----------------------------------------------------------------------------------------------------------------------