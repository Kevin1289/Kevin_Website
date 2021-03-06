from django.shortcuts import render
from django.contrib.auth import login, get_user_model, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import os
train_and_stops_dict = {}
from .forms import UserCreationForm, UserLoginForm


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, "Train_Website/Train_Register.html", context)


def login_view(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return render(request, "Train_Website/Train_Home.html")
    return render(request, "Train_Website/landing.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")

def test(request):
    return render(request, 'Train_Website/landing.html')

def Train_Choose_Service(request):
    if request.method == 'POST':
        job = request.POST.get('Service')
        if job == "all stops":
            return HttpResponseRedirect('all_stops')
        elif job == "common station":
            return HttpResponseRedirect('/common_stations')
        elif job == 'done':
            return render(request, 'resume_website/resume_page.html')
        else:
            messages.success(request, 'Please enter a valid input.')
            return render(request, 'Train_Website/Train_Home.html')
    return render(request, 'Train_Website/Train_Home.html')

def common_stations(request):
    if request.method == 'POST':
        train1= request.POST.get('train_wanted1')
        train2= request.POST.get('train_wanted2')
        if train1.isalpha():
            train1 = train1.upper()
        if train2.isalpha():
            train2 = train2.upper()
        messages=[]
        args = {}
        if train1 != "STOP" and train2 != 'STOP':
            if train_and_stops_dict == {}:  
                make_train_dict()
            if train1 not in train_and_stops_dict:
                messages.append('Please enter a valid Train 1')
            else:
                args['train1'] = train1
            if train2 not in train_and_stops_dict:
                messages.append('Please enter a valid Train 2')
            else:
                args['train2'] = train2
            if len(messages) > 0:
                args['messages'] = messages
                return render(request, 'Train_Website/Train_common_station_without_stops.html', args)
            if train1 == train2:
                messages.append('The trains entered are the same.')
            common_stops_dict = {}
            common_stops = []
            for stop in train_and_stops_dict[train1]:
                if stop not in common_stops:
                    common_stops_dict[stop]=1
                else:
                    common_stops_dict[stop]+=1
            for stop in train_and_stops_dict[train2]:
                if stop in common_stops_dict:
                    common_stops.append(stop)
            common_stops_str = ''
            if len(common_stops) == 0:
                common_stops.append('There are no common stops between these two trains.')
                common_stops_str = 'There are no common stops between these two trains.'
            if len(common_stops) > 0:
                for stops in common_stops:
                    common_stops_str += stops + ','
                
            request.user.search_history += '@c' + train1 + ',' + train2 +',' + common_stops_str
            request.user.save()
            args = {'common_stops':common_stops, 'train1':train1, 'train2': train2, 'messages':messages}
            return render(request, 'Train_Website/Train_common_station.html', args)
        return render(request, 'Train_Website/Train_Home.html', {'messages':messages})
    return render(request, 'Train_Website/Train_common_station_without_stops.html')

def all_stops(request):
    if request.method == 'POST':
        entered =request.POST.get('train_wanted')
        if entered.isalpha():
            entered = entered.upper()
        messages = []
        if entered != "STOP":
            if train_and_stops_dict == {}:  
                make_train_dict()
            if entered not in train_and_stops_dict:
                messages.append("Please enter in a valid train. Thank you.")
                args={'messages':messages, 'train_and_stops_dict':train_and_stops_dict}
                return render(request, 'Train_Website/Train_all_stops_without_stops.html', args)
            else:
                stops_for_train=[]
                for item in train_and_stops_dict[entered]:
                    stops_for_train.append(item)
                start = stops_for_train[0]
                end = stops_for_train[len(stops_for_train)-1]

                stops_for_train_str = ''
                for stops in stops_for_train:
                    stops_for_train_str += stops+','
                

                request.user.search_history += '@s' + entered + ',' + stops_for_train_str
                request.user.save()

                args = {'messages':messages, 'stops_for_train':stops_for_train, 'entered':entered, 'start':start, 'end':end, 'train_and_stops_dict':train_and_stops_dict}
                return render(request, 'Train_Website/Train_all_stops.html', args )
        return render(request, 'Train_Website/Train_Home.html', {'messages':messages})
    return render(request, 'Train_Website/Train_all_stops_without_stops.html')

def make_train_dict(stop_file='mta_train_stop_data1.txt'):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, stop_file)
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            lst = line.strip().split(",")
            train = lst[0][0]
            stop = lst[2]
            if train not in train_and_stops_dict:
                train_and_stops_dict[train] = [stop]
            elif stop not in train_and_stops_dict[train]:
                train_and_stops_dict[train].append(stop)
    return train_and_stops_dict

def History(request):
    history = request.user.search_history
    if history == '':
        args = {'organized_his':[[['You have not made any previous searches',], []]]}
        return render(request, 'Train_Website/history.html', args)
    organized_his = []
    char = 0
    stop  = ''
    ind = -1
    while char < len(history):
        if history[char] == '@':
            ind+=1
            organized_his.append([[],[]])
            char +=1
            if history[char] == 's':
                organized_his[ind][0].append('Show all stops of train: ' + history[char+1])
                char +=3

            if history[char] == 'c':
                organized_his[ind][0].append('Show all common stops of train: ' + history[char+1] + ' and ' + history[char+3])
                char +=5
        else:
            if history[char] == ',':
                organized_his[ind][1].append(stop) 
                stop = ''
                char += 1
            else:
                stop += history[char]
                char += 1
    if stop != '':
        organized_his[ind][1].append(stop)
    args = {'organized_his': organized_his}
    return render(request, 'Train_Website/history.html', args)

def logout_view(request):
    try:
        name = request.user.full_name
        logout(request)
        messages=[]
        messages.append(name + ' has successfully logged out. Than you for using the MTA Assistant App!')
        return render(request, 'Train_Website/landing.html', {'messages':messages})
    except:
        return render(request, 'Train_Website/landing.html')
