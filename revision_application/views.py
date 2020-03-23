from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import LoginForm, RegistrationForm, UploadImageForm, UploadPdfForm
from .models import User, Folder, Set, Question
from .ocr import pdf_to_text, img_to_text

import os

# ///////////////////////

# region Upload images,PDF & OCR


def upload(request):
    if request.method == 'POST':
        print(request.POST)  # testing
        if 'upload_image' in request.POST:
            img_form = UploadImageForm(request.POST, request.FILES)
            if img_form.is_valid():
                # store the file inside folder - 'upload'
                store_uploaded_file(request.FILES['file'])
                path = 'upload/' + request.FILES['file'].name
                img_to_text(path)
                delete_file(path)
                return HttpResponse('<h5>Upload Successful</h5>')

        elif 'upload_pdf' in request.POST:
            pdf_form = UploadPdfForm(request.POST, request.FILES)
            if pdf_form.is_valid():
                # store the file inside folder - 'upload'
                store_uploaded_file(request.FILES['file'])
                path = 'upload/' + request.FILES['file'].name
                pdf_to_text(path)
                delete_file(path)
                return HttpResponse('<h5>Upload Successful</h5>')
    else:
        img_form = UploadImageForm()
        pdf_form = UploadPdfForm()

    if 'Upload_image' in request.POST:
        return render(request, 'upload.html', {'form': img_form})
    else:
        return render(request, 'upload.html', {'form': pdf_form})


def store_uploaded_file(f):
    path = 'upload/' + f.name
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

# endregion

# ///////////////////////

# region Reg & login

# # test
# show_list()
# # # #
# # Put user id into HTTP session
# request.session['Username'] = u.username


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # get user's input
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # If the entered username isn't in the database, reload an empty form
            if len(User.objects.filter(username=username)) == 0:
                form = LoginForm()
            else:
                # check if password matches
                u = User.objects.get(username=username)
                if u is not None and u.password == password:
                    # Put user id into HTTP session
                    request.session['Username'] = u.username
                    return HttpResponseRedirect('/home/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.method == "POST":
        print(request.POST)
        # Use the query dictionary to create a form object
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # create an User object and add attributes
            new_user = User()
            new_user.username = form.cleaned_data['username']
            new_user.password = form.cleaned_data['password1']
            new_user.email = form.cleaned_data['email']
            new_user.save()

            return render(request, 'reg_success.html')

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def logout(request):
    # check if this user has logged in
    print(request.session.has_key('Username'))
    if request.session.has_key('Username'):
        del request.session['Username']
        # if request.session.has_key('cart'):
        #     del request.session['cart']
        return HttpResponseRedirect('/login/')


# # # # # # # # # # # # # #
# Reg & login development #
# # # # # # # # # # # # # #


def show_list():
    # show all data
    data_list = User.objects.all()
    print(data_list)


def remove_user(request):
    # get the username in url
    username = request.GET['username']
    u = username.object.get(username=username)
    u.delete()
    show_list()

# endregion

# ///////////////////////

# region /home/


def show_folders(request):
    # check if this user has logged in
    if not request.session.has_key('Username'):
        print("Not logged in")
        # Log in again
        return HttpResponseRedirect('/login/')
    else:
        folders = Folder.objects.filter(username=request.session['Username'])
        return render(request, 'home.html', {'folders': folders})

# endregion

# ///////////////////////

# region set


def show_sets(request):
    # check if this user has logged in
    if not request.session.has_key('Username'):
        print("Not logged in")
        # Log in again
        return HttpResponseRedirect('/login/')
    else:
        folder_id = request.GET['folder_id']
        sets = Set.objects.filter(folder_id=request.GET['folder_id'])
    return render(request, 'sets.html', {'sets': sets, 'folder_id': folder_id})

# endregion

# ///////////////////////

# region add folders & sets


def add(request, folder_id):  # DEBUGGING - don't pass in folder_id
    # check if this user has logged in
    if not request.session.has_key('Username'):
        print("Not logged in")
        # Log in again
        return HttpResponseRedirect('/login/')

    # get the new folder/set name from  URL
    if 'folder_name' in request.GET:
        folder_name = request.GET['folder_name']
        # add this new folder to the database
        f = Folder()
        f.folder_name = folder_name
        username = request.session['Username']
        f.username = User.objects.get(username=username)
        f.save()
        return HttpResponseRedirect('/home/')

    elif 'set_name' in request.GET:
        print(request)
        set_name = request.GET['set_name']
        # add this new set to the database
        s = Set()
        s.set_name = set_name
        s.folder_id = Folder.objects.get(folder_id=folder_id)
        s.save()
        return HttpResponseRedirect('/sets/?folder_id=' + str(folder_id))


# endregion

# ///////////////////////

# region delete folders & sets


def delete_folder(request):
    # check whether we are deleting a folder or a set
    if 'folder_id' in request.GET:
        # 取出URL后面的folder_id参数
        folder_id = request.GET['folder_id']
        # Delete data
        f = Folder.objects.get(folder_id=folder_id)
        f.delete()
        return HttpResponseRedirect('/home/')
    elif 'set_id' in request.GET:
        # 取出URL后面的set_id参数
        set_id = request.GET['set_id']
        # Delete data
        s = Set.objects.get(set_id=set_id)
        folder_id = s.folder_id.folder_id
        s.delete()
        return HttpResponseRedirect('/sets/?folder_id=' + str(folder_id))

# endregion

# ///////////////////////

# region question


def show_questions(request):
    # check if this user has logged in
    if not request.session.has_key('Username'):
        print("Not logged in")
        # Log in again
        return HttpResponseRedirect('/login/')
    else:
        set_id = request.GET['set_id']
        questions = Question.objects.filter(set_id=set_id)
        s = Set.objects.get(set_id=set_id)
        folder_id = s.folder_id.folder_id   # DEBUGGING: only do one folder_id
    return render(request, 'questions.html', {'questions': questions, 'set_id': set_id, 'folder_id': folder_id})

# endregion

# ///////////////////////

# region edit question


def edit(request):

    # create a queryset that contains all the question objects in this set
    set_id = request.GET['set_id']
    question_list = Question.objects.filter(set_id=set_id)

    return render(request, 'edit.html', {'question_list': question_list})


def add_question(request, set_id):
    q = Question()
    q.question = ""
    q.answer = ""
    q.set_id = Set.objects.get(set_id=set_id)
    q.save()

    question_list = Question.objects.filter(set_id=set_id)
    print(question_list)
    return render(request, 'edit.html', {'question_list': question_list})


def del_question(request, question_id):
    # Delete question
    q = Question.objects.get(question_id=question_id)
    set_id = q.set_id.set_id
    q.delete()
    return HttpResponseRedirect('/edit/?set_id=' + str(set_id))

# endregion

# ///////////////////////


# this could be used as an improvement / testing refinement
def check_if_logged_in(request):
    # check if this user has logged in
    if not request.session.has_key('Username'):
        print("Not logged in")
        # Log in again
        return HttpResponseRedirect('/login/')


def popup_test(request):
    return render(request, 'popup.html')



def quiz_question(request):
    return render(request, 'quiz_question.html')


def quiz_answer(request):
    return render(request, 'quiz_answer.html')


def result(request):
    return render(request, 'result.html')
