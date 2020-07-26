from django.shortcuts import render
from django.contrib.auth import login, get_user_model, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import os
train_and_stops_dict = {}
# Create your views here.
from .forms import UserCreationForm, UserLoginForm


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        
        #return HttpResponse('Registration Fail')
    else:
        form = UserCreationForm()
    context = {'form': form}
    #return render(request, "Train_Website/register.html", context)
    return render(request, "Train_Website/Train_Register.html", context)


def login_view(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        #form = UserLoginForm(request.POST or None)
        #return HttpResponseRedirect("/test")
        #return render(request, 'Train_Website/landing.html.html', {"form": form})
        #id = request.user.id  , {'id':id}
        return render(request, "Train_Website/Train_Home.html")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', form)
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
            return HttpResponseRedirect('/all_stops')
            #return HttpResponse('ALL STOPS')
            #show_stops() 
        elif job == "common station":
            return HttpResponseRedirect('/common_stations')
            #return HttpResponse('COMMON STATIONS')
        elif job == 'done':
            return render(request, 'resume_website/resume_page.html')
        else:
            messages.success(request, 'Please enter a valid input.')
            return render(request, 'Train_Website/Train_Home.html')
    return HttpResponse('Service submitted: NOT POST')

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
                print('NEWWWWWWWWWWWWWW')
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
            print(common_stops_dict)
            for stop in train_and_stops_dict[train2]:
                #print(stop)
                if stop in common_stops_dict:
                    #print('>>>>>>>>>>>>>>IN')
                    common_stops.append(stop)
            #print(common_stops)
            if len(common_stops) == 0:
                common_stops.append('There are no common stops between these two trains.')
            args = {'common_stops':common_stops, 'train1':train1, 'train2': train2, 'messages':messages}
            return render(request, 'Train_Website/Train_common_station.html', args)
        return render(request, 'Train_Website/Train_Home.html', {'messages':messages})
    return render(request, 'Train_Website/Train_common_station_without_stops.html')
    #return HttpResponse('NOT POST COMMON STATIONS')

def all_stops(request):
    if request.method == 'POST':
        entered =request.POST.get('train_wanted')
        if entered.isalpha():
            entered = entered.upper()
        messages = []
        if entered != "STOP":
            #print('A')
            #print(request.POST, '>request.POST.get(train_and_stops_dict)>', request.POST.get('train_and_stops_dict'), '<')
            if train_and_stops_dict == {}:  
                make_train_dict()
            if entered not in train_and_stops_dict:
                #print('D')
                messages.append("Please enter in a valid train. Thank you.")
                args={'messages':messages, 'train_and_stops_dict':train_and_stops_dict}
                return render(request, 'Train_Website/Train_all_stops_without_stops.html', args)
            else:
                #print('E')
                stops_for_train=[]
                #print('$$$$$$$$$$$$$$$$$', train_and_stops_dict[entered])
                for item in train_and_stops_dict[entered]:
                    stops_for_train.append(item)

                #print('stops_for_train>>>>', stops_for_train)
                start = stops_for_train[0]
                end = stops_for_train[len(stops_for_train)-1]
                args = {'messages':messages, 'stops_for_train':stops_for_train, 'entered':entered, 'start':start, 'end':end, 'train_and_stops_dict':train_and_stops_dict}
                return render(request, 'Train_Website/Train_all_stops.html', args )
            # if answer not in trainoverlap.dict and answer != "stop":
            #     messages.append("Please enter in a valid train. Thank you.")
        
        #print('F')
        return render(request, 'Train_Website/Train_Home.html', {'messages':messages})
        #return HttpResponse(request.POST.get('show_stop_train'))
    #print('G')
    return render(request, 'Train_Website/Train_all_stops_without_stops.html')
    #return HttpResponse('ALL STOPS IN NEW HTMLLLLL')


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
    #print(train_and_stops_dict)
    return train_and_stops_dict


#         # sto = request.POST.get('Service')
#         # print(request.POST.get('Service'))
#         # print('POSTTT', request.POST)


#         job = request.POST.get('Service')
#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
#         trainoverlap = train(file_path)
#         trainoverlap.make_list()
#         if job == "all stops":
#             show_stops()
#         elif job == "common station":
#             line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             while line1 not in trainoverlap.dict:
#                 print("Please enter in a valid train. Thank you.")
#                 line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             print("")
#             line2 = input("Enter the second of the two trains that you would like to find similiar stations of.")
#             while line2 not in trainoverlap.dict:
#                 print("Please enter in a valid train. Thank you.")
#                 line2 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             print("")
#             trainoverlap = train(file_path)
#             trainoverlap.make_list()
#             trainoverlap.stop_overlap(line1, line2)
#         elif job == 'done':
#             return render(request, 'resume_website/resume_page.html')
#         else:
#             print("please enter a valid choice.")
#             main()




#         return HttpResponse(sto)
#     print('NOT POSTTT')
#     return HttpResponse('Service submitted: NOT POST')

# class train(object):
#     def __init__(self, file_name):
#         self.file_name = file_name
#         self.dict = {}
#         self.dict_overlap = []

    def make_line(self, answer):
        final = ""
        with open(self.file_name, "r") as file:
            file.readline()
            for line in file:
                lst = line.split(",")
                train = lst[0][0]
                stop = lst[2]
                if train not in self.dict:
                    self.dict[train] = stop + ", "
                elif stop not in self.dict[train]:
                    self.dict[train] += stop + ", "
            for item in self.dict[answer]:
                final += item
            print(answer, "line: ", final[:-2])

#     def make_list(self):
#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
#         with open(file_path, "r") as file:
#             file.readline()
#             for line in file:
#                 lst = line.strip().split(",")
#                 train = lst[0][0]
#                 stop = lst[2]
#                 if train not in self.dict:
#                     self.dict[train] = stop + ", "
#                 elif stop not in self.dict[train]:
#                     self.dict[train] += stop + ", "

#     def stop_overlap(self, line1, line2):
#         self.make_list()
#         count1 = 0
#         count2 = 0
#         lst1 = self.dict[line1].split(",")
#         lst1[0] = ' ' + lst1[0]
#         lst2 = self.dict[line2].split(",")
#         lst2[0] = ' ' + lst2[0]
#         for stop in lst1:
#             count2 = 0
#             for stop_other in range(len(lst2) - 1):
#                 counter = stop_other - 1
#                 if lst1[count1] == lst2[count2]:
#                     self.dict_overlap.append(stop)
#                 count2 += 1
#             count1 += 1

#         if len(self.dict_overlap) == 0:
#             print(
#                 "Unfortunately, there are no common stops for these trains. Please try a different set of trains.")
#         else:
#             sto = ""
#             for station in self.dict_overlap:
#                 sto += station + " "
#             print("The common stops for theses trains are " + sto[:-1] + ".")
#             print("Thank you so much for using our service. Have a nice day. \n")
#         main()

#     def choose_operation():
#         print("Enter 'all stops' to display all the stops for a train" + '\n' + "Enter 'common station' to find any common stations between two trains" + '\n' + 'Enter "done" to exit this application.')
#         return input()

    def show_stops():
        answer = ("default")
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
        while answer != "done":
            print("")
            answer = input("Please enter a train line. If done with this service, please enter 'stop'. ")
            trainoverlap = train(file_path)
            trainoverlap.make_list()
            if answer == 'stop':
                print("Thank you so much for using our service. Have a nice day. \n")
                main()
            train1 = train(file_path)
            if answer not in trainoverlap.dict and answer != "done":
                print("Please enter in a valid train. Thank you.")
                show_stops()
            print("")
            print("")
            train1.make_line(answer)

#     def main():
#         job = choose_operation()
#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
#         trainoverlap = train(file_path)
#         trainoverlap.make_list()
#         if job == "all stops":
#             show_stops()
#         elif job == "common station":
#             line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             while line1 not in trainoverlap.dict:
#                 print("Please enter in a valid train. Thank you.")
#                 line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             print("")
#             line2 = input("Enter the second of the two trains that you would like to find similiar stations of.")
#             while line2 not in trainoverlap.dict:
#                 print("Please enter in a valid train. Thank you.")
#                 line2 = input("Enter one of the two trains that you would like to find similiar stations of.")
#             print("")
#             trainoverlap = train(file_path)
#             trainoverlap.make_list()
#             trainoverlap.stop_overlap(line1, line2)
#         elif job == 'done':
#             return render(request, 'resume_website/resume_page.html')
#         else:
#             print("please enter a valid choice.")
#             main()

#     main()