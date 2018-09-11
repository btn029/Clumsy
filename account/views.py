from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.images import ImageFile
from django.core.files.base import File
from django.contrib.auth import logout as django_logout
from django import forms
from django.contrib import messages

from .models import Employee, Post, Comment
from .forms import SignupForm, LoginForm, PostForm, CommentForm

import hashlib
from datetime import datetime

# helper function to save all comment info in one object
def getPost(postObj):
    return{
        'post': postObj.post,
        'employee': postObj.employee,
        'when': postObj.when,
        'subject': postObj.subject,
        'postId': postObj.postId
    }

#   helper function to save all employee info in one object
def getEmployee(employeeObj):
    return {
        'firstName': employeeObj.firstName,
        'lastName': employeeObj.lastName,
        'email': employeeObj.email,
        'password': employeeObj.password,
        'phone': employeeObj.phone,
        'address': employeeObj.address,
        'department': employeeObj.department,
        'profilePic': employeeObj.profilePic
    }

# helper function to save all comment info in one object
def getComment(commentObj):
    return{
        'comment': commentObj.comment,
        'employee': commentObj.employee,
        'when': commentObj.when
    }

# controller for creating a new account
def signup(request):
    if (request.method == 'POST'):
        form = SignupForm(data=request.POST)   # instance of signupForm

        if (form.is_valid()):
            # encrypt the password so we can't just read what it is
            pwdEncrypt = hashlib.sha224(form.cleaned_data['password']).hexdigest()

            #save the information in the form to variables
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            password = pwdEncrypt
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            department = form.cleaned_data['department']

            try:
                profilePic = request.FILES['profilePic']
                profPic = True
            except MultiValueDictKeyError:
                profPic = False
                pass

            if Employee.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use")
            if(profPic):    
                employeeObj = Employee(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=password,
                    phone=phone,
                    address=address,
                    department=department,
                    profilePic = profilePic)
            else:
                    employeeObj = Employee(
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    password=password,
                    phone=phone,
                    address=address,
                    department=department)

            employeeObj.save()    #save to database this new employee
            request.session['email'] = email
            outURL = '{0}/{1}'.format(email,'employeehome', {'email': email})
            return HttpResponseRedirect(outURL)

    else:
        form = SignupForm()
    #signup.html posts to this same page and then this view will redirect
    return render(request, 'signup.html', {'form': form})

def login(request):
    if(request.session.has_key('email')):
        email = request.session['email']
        try:
            employeeObj = Employee.objects.get(email=email)
            returnEmployee = getEmployee(employeeObj)
            outURL = '{0}/{1}'.format(email,'employeehome')
            return HttpResponseRedirect(outURL, {'email': email})
        except ObjectDoesNotExist:
            pass

    else:
        if (request.method == 'POST'):
            form = LoginForm(request.POST)

            if (form .is_valid()):
                pwdEncrypt = hashlib.sha224(form.cleaned_data['password']).hexdigest()
                email = form.cleaned_data['email']
                password = pwdEncrypt
 
                try:
                    employeeObj = Employee.objects.get(email=email)
                    returnEmployee = getEmployee(employeeObj)
                    if (password == employeeObj.password):
                        request.session['email'] = email
                        outURL = '{0}/{1}'.format(email,'employeehome')
                        return HttpResponseRedirect(outURL, {'email': email})
                except ObjectDoesNotExist:
                    messages.info(request, 'E-mail is not registered or Password is incorrect.')
                    pass
        else:
            form = LoginForm()

        return render(request, 'login.html', {'form': form})

def logout(request):
    django_logout(request)
    request.session.flush()
    # Redirect to a success page.
    messages.info(request, 'Successfully logged out!')
    form = LoginForm()
    return HttpResponseRedirect("/")

def employeehome(request, employeeEmail):
    if (request.session.has_key('email')):
        if(employeeEmail == request.session['email']):
            email = request.session['email']
            try:
                employeeObj = Employee.objects.get(email=employeeEmail)
                returnEmployee = getEmployee(employeeObj)

            except ObjectDoesNotExist:
                return HttpResponseRedirect('login')

            #try:
                # get a list of posts associated with this employee
                #apptQuery = Appointment.objects.filter(client=clientObj)
                #apptList = [getAppointment(singleAppt) for singleAppt in apptQuery]

            #except ObjectDoesNotExist:
                #apptList = ""

            #reviewQuery = []
            # get a list of a reviews based on the list of appointments 
            #for oneAppt in apptQuery:
                #try:
                    #reviewQuery.append(oneAppt.review_set.all().exclude(writer=clientEmail).get())
                #except ObjectDoesNotExist:
                    #pass

            #if(len(reviewQuery) > 0):
                #reviewList = [getReview(reviewObj) for reviewObj in reviewQuery]
            #else:
                #reviewList = ""

            return render(request, 'employeehome.html', {'employee': returnEmployee})

    return HttpResponseRedirect('login')


def employeeprofile(request, employeeEmail):
    # filter through the client table by matching emails
    employeeObj = Employee.objects.get(email=employeeEmail)
    returnEmployee = getEmployee(employeeObj)

    try:
        # get a list of appointments associated with this client
        postQuery = post.objects.filter(client=employeeObj)
        postList = [getPost(singlePost) for singlePost in postQuery]

    except ObjectDoesNotExist:
        postList = ""

    # send the information about the particular client with matching
    # email to clientprofile.html
    return render(request, 'account/employeeprofile.html', 
                  {'client': returnClient,
                    'postList': postList,
                    'reviewList': reviewList} )

def editclient(request, clientEmail):
    if (request.session.has_key('email')):
        if(clientEmail == request.session['email']):
            email = request.session['email']
            try:
                clientObj = Client.objects.get(email=clientEmail)
                data = {
                    'phone':clientObj.phone,
                    'address':clientObj.address,
                    'description':clientObj.description
                }

                form = EditClientForm(data)
            
                if(request.method=='POST'):
                    form = EditClientForm(request.POST, request.FILES)   # instance of EditClientForm
                    if (form.is_valid()):
                        #save the information in the form to variables
                        phone = form.cleaned_data['phone']
                        address = form.cleaned_data['address']
                        description = form.cleaned_data['description']

                        try:
                            clientObj.profilePic = request.FILES['profilePic']
                        except MultiValueDictKeyError:
                            pass
                        clientObj.phone = phone
                        clientObj.address = address
                        clientObj.description = description
                        clientObj.save()
                        
                        return HttpResponseRedirect('employeehome')

                else:
                    form = EditClientForm(initial = data)
                return render(request, 'account/editclient.html', {'form': form})
            except ObjectDoesNotExist:
                pass
    return HttpResponseRedirect('../login.html')

def postlist(request, employeeEmail):
    if (request.session.has_key('email')):
        email = request.session['email']
        post_array = Post.objects.all()
        return render(request, 'postlist.html')

def makeappointment(request, barberEmail):
    if (request.session.has_key('email')):
        clientEmail = request.session['email']
        clientObj = Client.objects.get(email=clientEmail)

        barberObj = Barber.objects.get(email=barberEmail)
        if (request.method == 'POST'):
            form = AppointmentForm(data=request.POST)
            print("form is " + str(form.is_valid()))
            if(form.is_valid()):

                # get time
                dateTimeString = form.cleaned_data['when']
                # 03/16/2017 4:36 PM output
                dateTimeObj = datetime.strptime(dateTimeString, '%m/%d/%Y %I:%M %p')

                # get address from radio button
                address="undecided"
                location = form.cleaned_data['addressChoice']
                if(location == "selectLocationBarber"):
                    if(barberObj.address):
                        address = barberObj.address
                else:
                    if(barberObj.address):
                        address = clientObj.address

                # save new appointment into model
                newAppt = Appointment(when=dateTimeObj, address=address, barber=barberObj, client=clientObj)
                newAppt.save()
                outURL = '../{0}/clienthome.html'.format(clientEmail)
                return HttpResponseRedirect(outURL)
        else:
            # empty form if form is not valid
            form = AppointmentForm()
        return render(request, 'account/makeappointment.html',{'form': form})
    #if fail to have session redirect to login
    return HttpResponseRedirect('../../login.html')

def post(request, postId, employeeEmail):
    return render(request, 'account/post.html')

def editpost(request, postId, employeeEmail):
    return render(request, 'account/editpost.html')

def newpost(request, employeeEmail):
    if(request.session.has_key('email')):
        employeeEmail = request.session['email']

        # get the appointment associated
        employeeObj=Employee.objects.get(email=employeeEmail)
        if(request.method == 'POST'):
            form = PostForm(data=request.POST)

            print("form is " + str(form.is_valid()))
            if (form.is_valid()):
                comment=form.cleaned_data['comment']

                #get review of the appointment
                print("number of reviews:" + str(apptObj.review_set.all()))
                
                # review already exists for this client and appt
                #if(apptObj.review_set.count() > 0):
                 #   try:
                 #       postObj = apptObj.review_set.get(writer=employeeEmail)
                 #       reviewObj.comment = comment
                 #       reviewObj.save()
                 #   except ObjectDoesNotExist: # new review must be made
                 #       reviewObj = Review(comment=comment, writer=employeeEmail,appointment=apptObj)
                 #       reviewObj.save()
                #else:
                #    reviewObj = Review(comment=comment, writer=employeeEmail,appointment=apptObj)
                #    reviewObj.save()
                #outURL = '../{0}/employeehome.html'.format(employeeEmail)
                #return HttpResponseRedirect(outURL)
        else:
            form = PostForm()
        return render(request, "newpost.html", {'form': form})

    return HttpResponseRedirect('postlist')


def deletepost(request, postId):
        clientEmail = request.session['email']
        postObj = Post.objects.get(pk=postId)
        postObj.delete()
        outURL = '../{0}/postlist.html'.format(clientEmail)
        return HttpResponseRedirect(outURL)
