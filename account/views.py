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
from .forms import SignupForm, LoginForm, PostForm, CommentForm, UpdateForm, EditProfileForm

import hashlib
from datetime import datetime

# helper function to save all comment info in one object
def getPost(postObj):
    return{
        'post': postObj.post,
        'employee': postObj.employee,
        'when': postObj.when,
        'subject': postObj.subject,
        'postId': postObj.postId,
        'anonymity': postObj.anonymity,
        'status': postObj.status
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
        'when': commentObj.when,
        'post': commentObj.post,
        'anonymity': commentObj.anonymity,
        'commentId': commentObj.commentId,
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

            except ObjectDoesNotExist:
                return HttpResponseRedirect('login')

            try:
                #get a list of posts associated with this employee
                posts = Post.objects.filter(employee=employeeObj).order_by('-when')
            except ObjectDoesNotExist:
                posts = ""

            try:
                #get a list of posts associated with this employee
                comments = Comment.objects.filter(employee=employeeObj).order_by('-when')
            except ObjectDoesNotExist:
                posts = ""

            return render(request, 'employeehome.html', {'employee': employeeObj, 'postList':posts, 'comments':comments})

    return HttpResponseRedirect('login')


def employeeprofile(request, employeeEmail):
    if (request.session.has_key('email')):
        currentUser = request.session['email']
        currentUserObj = Employee.objects.get(email=currentUser)
        try:
            employeeObj = Employee.objects.get(email=employeeEmail)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('login')

        try:
            #get a list of posts associated with this employee
            posts = Post.objects.filter(employee=employeeObj,anonymity="NotAnonymous").order_by('-when')
        except ObjectDoesNotExist:
            posts = ""

        try:
            #get a list of posts associated with this employee
            comments = Comment.objects.filter(employee=employeeObj,anonymity="NotAnonymous").order_by('-when')
        except ObjectDoesNotExist:
            posts = ""

        return render(request, 'employeeprofile.html', {'employee': employeeObj, 'postList':posts, 'comments':comments,'currentUser': currentUserObj})

    return HttpResponseRedirect('employeehome')

def editprofile(request, employeeEmail):
    if (request.session.has_key('email')):
        if(employeeEmail == request.session['email']):
            email = request.session['email']
            try:
                employeeObj = Employee.objects.get(email=employeeEmail)
                data = {
                    'phone':employeeObj.phone,
                    'address':employeeObj.address,
                    'department':employeeObj.department,
                }

                form = EditProfileForm(data)
            
                if(request.method=='POST'):
                    form = EditProfileForm(request.POST, request.FILES)
                    if (form.is_valid()):
                        phone = form.cleaned_data['phone']
                        address = form.cleaned_data['address']
                        department = form.cleaned_data['department']

                        try:
                            employeeObj.profilePic = request.FILES['profilePic']
                        except MultiValueDictKeyError:
                            pass
                        employeeObj.phone = phone
                        employeeObj.address = address
                        employeeObj.department = department
                        employeeObj.save()
                        
                        return HttpResponseRedirect('employeehome')

                else:
                    form = EditProfileForm(initial = data)
                return render(request, 'editprofile.html', {'form': form})
            except ObjectDoesNotExist:
                pass
    return HttpResponseRedirect('employeehome')

def postlist(request, employeeEmail):
    if (request.session.has_key('email')):
        post_array = Post.objects.all().order_by('-when')
        email = request.session['email']
        return render(request, 'postlist.html',{'posts':post_array})

def post(request, postId):
    if(request.session.has_key('email')):
        userEmail = request.session['email']
        employee = Employee.objects.get(email=userEmail)
        form = UpdateForm(data=request.POST)
        try:
            post = Post.objects.get(postId=postId)
        except ObjectDoesNotExist:
            pass
        
        try:
            #get a list of comments associated with this post
            comments = Comment.objects.filter(postId=postId)
        except ObjectDoesNotExist:
            posts = ""
        if(request.method == 'POST'): 
            if(form.is_valid()):   
                status = form.cleaned_data['status']
                post.status = status
                post.save()
                outURL = '/{0}/{1}'.format(userEmail,'postlist')
                return HttpResponseRedirect(outURL)
        else:
            return render(request, 'post.html', {'post': post, 'currentUser':employee, 'form': form, 'comments':comments})

def editpost(request, postId):
    return render(request, 'account/editpost.html')

def newpost(request, employeeEmail):
    if(request.session.has_key('email')):
        employeeEmail = request.session['email']

        # get the appointment associated
        employeeObj=Employee.objects.get(email=employeeEmail)
        if(request.method == 'POST'):
            form = PostForm(data=request.POST)

            if (form.is_valid()):
                post = form.cleaned_data['post']
                subject = form.cleaned_data['subject']
                anonymity = form.cleaned_data['anonymity']
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                postObj = Post(
                    post=post,
                    employee=employeeObj,
                    when=date,
                    subject=subject,
                    anonymity=anonymity
                )
                postObj.save()
                return HttpResponseRedirect('postlist')
        else:
            form = PostForm()
        return render(request, "newpost.html", {'form': form})

    return HttpResponseRedirect('postlist')

def newcomment(request, postId):
    if(request.session.has_key('email')):
        employeeEmail = request.session['email']

        # get the appointment associated
        employeeObj=Employee.objects.get(email=employeeEmail)
        postObj = Post.objects.get(postId=postId)
        if(request.method == 'POST'):
            form = CommentForm(data=request.POST)

            if (form.is_valid()):
                comment = form.cleaned_data['comment']
                anonymity = form.cleaned_data['anonymity']
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commentObj = Comment(
                    comment=comment,
                    employee=employeeObj,
                    when=date,
                    post=postObj,
                    anonymity=anonymity,
                    postId=postId
                )
                postObj.numComments += 1
                postObj.save()
                commentObj.save()
                return HttpResponseRedirect('post')
        else:
            form = CommentForm()
        return render(request, "newcomment.html", {'form': form, 'currentUser':employeeObj})

    return HttpResponseRedirect('post')

def deletepost(request, postId):
        employeeEmail = request.session['email']
        postObj = Post.objects.get(postId=postId)
        postObj.delete()
        outURL = '../{0}/postlist.html'.format(employeeEmail)
        return HttpResponseRedirect(outURL)
