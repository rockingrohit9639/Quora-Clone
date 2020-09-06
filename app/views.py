from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Questions, Comments
# Create your views here.


def index(request):
    if request.method == 'POST':
        id = request.POST['ques']
        print(id)
    allQuestions = Questions.objects.all()
    allComments = Comments.objects.all()
    user = request.user

    context = {
        "questions":allQuestions,
        "comments":allComments,
        "user":user
    }
    return render(request, 'index.html', context)


def addQues(request):
    title = request.GET['title']
    descr = request.GET['desc']

    ques = Questions(title=title, desc=descr)
    ques.save()

    return redirect("/")


def addComment(request):
    comment = request.GET['newComment']
    quesId = request.GET['questionId']
    ques = Questions.objects.get(id=quesId)
    user = request.user
    parentId = request.GET['parentId']

    if parentId == "":
        newComment = Comments(comment=comment, user=user, question=ques)
    else:
        parent = Comments.objects.get(id=parentId)
        newComment = Comments(comment=comment, user=user, question=ques, parent=parent)
    newComment.save()
    return redirect('/')


def handlelogin(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('/')
        else:
            messages.error(request, "Sorry!! Username of password does not match.")
            return redirect('/')

    return redirect("404 - Page not found.")


def handlelogout(request):
    logout(request)
    messages.success(request, "Logout Successfully.")
    return redirect("/")


def handlesignup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['emailA']
        password = request.POST['pass']

        user = User.objects.create_user(uname, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request, "Signup Successful.")
        login(request, user)
    return redirect('/')


def search(request):
    query = request.GET['search']

    if len(query) > 30:
        allQuestions = []
    else:
        allQuestions = Questions.objects.filter(title__icontains=query)

    params = {
        "questions":allQuestions
    }
    print(f"Search query : {query}")
    return render(request, "search.html", params)