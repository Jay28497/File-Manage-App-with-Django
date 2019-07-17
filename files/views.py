from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from files.models import Document
# from uploads.core.models import Document
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    documents = Document.objects.all()
    return render(request, 'files/home.html', {'documents': documents})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'files/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'files/login.html')


def signup(request):
    if request.method == 'POST':
        if request.POST['username'] != "" and request.POST['password1'] != "" and request.POST['password2'] != "":
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'files/signup.html', {'error': 'Username is already taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'files/signup.html', {'error': 'Password doesn\'t matched'})
        else:
            return render(request, 'files/signup.html', {'error': 'Please Fill the all fields.'})
    else:
        return render(request, 'files/signup.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


@login_required(login_url='/accounts/login/')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'files/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'files/simple_upload.html')


@login_required(login_url='/accounts/login/')
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'files/model_form_upload.html', {'form': form})
