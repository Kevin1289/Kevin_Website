
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import os

def home_page(request):
    return render(request, 'resume_website/resume_page.html')

def iFeeder(request):
    return render(request, 'resume_website/iFeeder_Home.html')

def ifeeder_ppt(request):
    return render(request, 'resume_website/ifeeder_ppt.html')

def ifeeder_flowchart(request):
    return render(request, 'resume_website/ifeeder_ppt.html')

def ifeeder_ad(request):
    return render(request, 'resume_website/ifeeder_ppt.html')

def train_project(request):
    class train(object):
        def __init__(self, file_name):
            self.file_name = file_name
            self.dict = {}
            self.dict_overlap = []

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

        def make_list(self):
            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
            with open(file_path, "r") as file:
                file.readline()
                for line in file:
                    lst = line.strip().split(",")
                    train = lst[0][0]
                    stop = lst[2]
                    if train not in self.dict:
                        self.dict[train] = stop + ", "
                    elif stop not in self.dict[train]:
                        self.dict[train] += stop + ", "

        def stop_overlap(self, line1, line2):
            self.make_list()
            count1 = 0
            count2 = 0
            lst1 = self.dict[line1].split(",")
            lst1[0] = ' ' + lst1[0]
            lst2 = self.dict[line2].split(",")
            lst2[0] = ' ' + lst2[0]
            for stop in lst1:
                count2 = 0
                for stop_other in range(len(lst2) - 1):
                    counter = stop_other - 1
                    if lst1[count1] == lst2[count2]:
                        self.dict_overlap.append(stop)
                    count2 += 1
                count1 += 1

            if len(self.dict_overlap) == 0:
                print(
                    "Unfortunately, there are no common stops for these trains. Please try a different set of trains.")
            else:
                sto = ""
                for station in self.dict_overlap:
                    sto += station + " "
                print("The common stops for theses trains are " + sto[:-1] + ".")
                print("Thank you so much for using our service. Have a nice day. \n")
            main()

    def choose_operation():
        print(
            "Enter 'all stops' to display all the stops for a train" + '\n' + "Enter 'common station' to find any common stations between two trains" + '\n' + 'Enter "done" to exit this application.')
        return input()

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

    def main():
        job = choose_operation()
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'mta_train_stop_data1.txt')
        trainoverlap = train(file_path)
        trainoverlap.make_list()
        if job == "all stops":
            show_stops()
        elif job == "common station":
            line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
            while line1 not in trainoverlap.dict:
                print("Please enter in a valid train. Thank you.")
                line1 = input("Enter one of the two trains that you would like to find similiar stations of.")
            print("")
            line2 = input("Enter the second of the two trains that you would like to find similiar stations of.")
            while line2 not in trainoverlap.dict:
                print("Please enter in a valid train. Thank you.")
                line2 = input("Enter one of the two trains that you would like to find similiar stations of.")
            print("")
            trainoverlap = train(file_path)
            trainoverlap.make_list()
            trainoverlap.stop_overlap(line1, line2)
        elif job == 'done':
            return render(request, 'resume_website/resume_page.html')
        else:
            print("please enter a valid choice.")
            main()

    main()
    return render(request, 'resume_website/resume_page.html')

