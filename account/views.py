from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.images import ImageFile
from django.core.files.base import File

from .models import User, Post, Comment
from .forms import SignupForm, LoginForm, PostForm, CommentForm

import hashlib   # password hasher
from datetime import datetime

# helper function to save all post info in one object
def getComment(postObj):
    return{
        'post': postObj.post,
        'user': commentObj.user,
        'when': commentObj.when
    }

#   helper function to save all user info in one object
def getUser(userObj):
    return {
        'firstName': userObj.firstName,
        'lastName': userObj.lastName,
        'email': userObj.email,
        'password': userObj.password,
        'phone': userObj.phone,
        'address': userObj.address,
        'department': userObj.department
    }

# helper function to save all comment info in one object
def getComment(commentObj):
    return{
        'comment': commentObj.comment,
        'user': commentObj.user,
        'when': commentObj.when
    }

def index(request):
    try:
        del request.session['email']
    except:
        pass
    return render_to_response('login.html')

# controller for creating a new account
def signup(request):
    if (request.method == 'POST'):
        form = SignupForm(data=request.POST)   # instance of signupForm

        if (form.is_valid()):
            # encrypt the password so we can't just read what it is
            pwdEncrypt = hashlib.sha224(form.cleaned_data['password']).hexdigest()

            #save the information in the form to variables
            userType = form.cleaned_data['userType']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            password = pwdEncrypt
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            userObj = User(
                firstName=firstName,
                lastName=lastName,
                email=email,
                password=password,
                phone=phone,
                address=address)
            barberObj.save()    #save to database this new barber
            request.session['email'] = email
            outURL = '{0}/{1}'.format(email,'userhome.html', {'email': email})
            return HttpResponseRedirect(outURL)

    else:
        form = SignupForm()
    #signup.html posts to this same page and then this view will redirect
    return render(request, 'account/signup.html', {'form': form})

def login(request):
    if(request.session.has_key('email')):
        email = request.session['email']
        try:
            userObj = User.objects.get(email=email)
            returnUser = getUser(userObj)
            outURL = '{0}/{1}'.format(email,'userhome.html')
            return HttpResponseRedirect(outURL, {'email': email})
        except ObjectDoesNotExist:
            pass

    else:
        if (request.method == 'POST'):
            form = LoginForm(request.POST)#

            if (form .is_valid()):
                pwdEncrypt = hashlib.sha224(form.cleaned_data['password']).hexdigest()
                userType = form.cleaned_data['userType']
                email = form.cleaned_data['email']
                password = pwdEncrypt
 
                try:
                    userObj = User.objects.get(email=email)
                    returnUser = getUser(userObj)
                    if (password == userObj.password):
                        request.session['email'] = email
                        outURL = '{0}/{1}'.format(email,'userhome.html')
                        return HttpResponseRedirect(outURL, {'email': email})
                except ObjectDoesNotExist:
                    pass
        else:
            form = LoginForm()

        return render(request, 'account/login.html', {'form': form})

def postlist(request, userEmail):
    return render(request, 'account/postlist.html')

def userhome(request, userEmail):
    if (request.session.has_key('email')):
        if(clientEmail == request.session['email']):
            email = request.session['email']
            try:
                clientObj = Client.objects.get(email=clientEmail)
                returnClient = getClient(clientObj)

            except ObjectDoesNotExist:
                return HttpResponseRedirect('../login.html')

            try:
                # get a list of appointments associated with this client
                apptQuery = Appointment.objects.filter(client=clientObj)
                apptList = [getAppointment(singleAppt) for singleAppt in apptQuery]

            except ObjectDoesNotExist:
                apptList = ""

            reviewQuery = []
            # get a list of a reviews based on the list of appointments 
            for oneAppt in apptQuery:
                try:
                    reviewQuery.append(oneAppt.review_set.all().exclude(writer=clientEmail).get())
                except ObjectDoesNotExist:
                    pass

            if(len(reviewQuery) > 0):
                reviewList = [getReview(reviewObj) for reviewObj in reviewQuery]
            else:
                reviewList = ""

            return render(request, 'account/userhome.html', 
                          {'client': returnClient,
                            'apptList': apptList,
                            'reviewList': reviewList} )

    return HttpResponseRedirect('../login.html')


def userprofile(request, userEmail):
    # filter through the client table by matching emails
    userObj = User.objects.get(email=userEmail)
    returnUser = getUser(userObj)

    try:
        # get a list of appointments associated with this client
        postQuery = post.objects.filter(client=userObj)
        postList = [getPost(singlePost) for singlePost in postQuery]

    except ObjectDoesNotExist:
        postList = ""

    # send the information about the particular client with matching
    # email to clientprofile.html
    return render(request, 'account/userprofile.html', 
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
                        
                        return HttpResponseRedirect('clientprofile.html')

                else:
                    form = EditClientForm(initial = data)
                return render(request, 'account/editclient.html', {'form': form})
            except ObjectDoesNotExist:
                pass
    return HttpResponseRedirect('../login.html')

def findbarber(request, clientEmail):
    if (request.session.has_key('email')):
        email = request.session['email']
        barber_array = Barber.objects.all()
        try:
            clientObj = Client.objects.get(email=clientEmail)
            barberList = Barber.objects.all()            
            return render(request, 'account/findbarber.html',{'barberList': barberList})
        except ObjectDoesNotExist:
            pass
    return HttpResponseRedirect('../login.html')

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

def post(request, postId, userEmail):
    return render(request, 'account/post.html')

def editpost(request, postId, userEmail):
    return render(request, 'account/editpost.html')

def newpost(request, apptReviewID):
    if(request.session.has_key('email')):
        userEmail = request.session['email']

        # get the appointment associated
        apptObj=Appointment.objects.get(pk=apptReviewID)
        passAppt=getAppointment(apptObj)
        if(request.method == 'POST'):
            form = ReviewForm(data=request.POST)

            print("form is " + str(form.is_valid()))
            if (form.is_valid()):
                comment=form.cleaned_data['comment']

                #get review of the appointment
                print("number of reviews:" + str(apptObj.review_set.all()))
                
                # review already exists for this client and appt
                if(apptObj.review_set.count() > 0):
                    try:
                        reviewObj = apptObj.review_set.get(writer=userEmail)
                        reviewObj.comment = comment
                        reviewObj.save()
                    except ObjectDoesNotExist: # new review must be made
                        reviewObj = Review(comment=comment, writer=userEmail,appointment=apptObj)
                        reviewObj.save()
                else:
                    reviewObj = Review(comment=comment, writer=userEmail,appointment=apptObj)
                    reviewObj.save()
                outURL = '../{0}/userhome.html'.format(userEmail)
                return HttpResponseRedirect(outURL)
        else:
            form = ReviewForm()
        return render(request, "account/newpost.html", {'form': form, 'appointment': passAppt})

    return HttpResponseRedirect('../../login.html')


def deletepost(request, postId):
        clientEmail = request.session['email']
        postObj = Post.objects.get(pk=postId)
        postObj.delete()
        outURL = '../{0}/postlist.html'.format(clientEmail)
        return HttpResponseRedirect(outURL)
