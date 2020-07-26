class train(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.dict = {}
        self.dict_overlap = []
        
        

    def make_line(self, answer):
        #dict = {}
        final = ""
        with open(self.file_name, "r") as file:
            file.readline()
            for line in file:
                lst = line.split(",")
                train = lst[0][0]
                stop = lst [2]
                if train not in self.dict:
                    self.dict[train] = stop+", "
                elif stop not in self.dict[train]:
                    self.dict[train] += stop+", "
            for item in self.dict[answer]:
                final += item
            print( answer, "line: ", final[:-2])
            #print("Thank you so much for using our service. Have a nice day. \n")
            #main()


    def make_list(self):
        with open("mta train stop data1.txt", "r") as file:
            file.readline()
            for line in file:
                lst = line.strip().split(",")
                train = lst[0][0]
                stop = lst [2]
                if train not in self.dict:
                    self.dict[train] = stop+", "
                elif stop not in self.dict[train]:
                    self.dict[train] += stop+", "
            #for train in self.dict:
                #print (train, "\n", self.dict[train])
            
        

    def stop_overlap(self, line1, line2):
        self.make_list()
        count1 = 0
        count2 = 0
        lst1 = self.dict[line1].split(",")
        #print(type(lst1))
        #print(type(lst1[0]))
        lst1[0] = ' '+lst1[0]
        #print(lst1[0])
        lst2 = self.dict[line2].split(",")
        lst2[0] = ' '+lst2[0]
        #input("")
        #print(len(lst1))
        #input("")
        #print(len(lst2))
        #input("")
        for stop in lst1:
            count2 = 0
            #print(self.dict[line2])
            #print("length=", len(self.dict[line2])-2)
            for stop_other in range (len(lst2)-1):
            #for stop_other in self.dict[line2]:
                counter = stop_other-1
                '''
                for train in self.dict:
                    print (train, "\n", self.dict[train])
                input("")
                print(lst1)
                print(type(lst1))
                input("")
                print(lst2)
                input("")
                '''
                #print (count2, stop_other)
                #print (lst2[count2])
                if lst1[count1] == lst2[count2]:
                    self.dict_overlap.append(stop)
                count2 += 1
            #print (count1)
            count1 += 1
        
        if len(self.dict_overlap) == 0:
            print("Unfortunately, there are no common stops for these trains. Please try a different set of trains.")
        else:
            sto = ""
            #print(self.dict_overlap)
            for station in self.dict_overlap:
                sto += station+" "
            print("The common stops for theses trains are "+sto[:-1]+".")
            print("Thank you so much for using our service. Have a nice day. \n")
        main()



    

def choose_operation():
    print("Enter 'all stops' to display all the stops for a train"+'\n'+"Enter 'common station' to find any common stations between two trains")
    return input()
            

def show_stops():
    answer = ("default")
    while answer != "done":
        print("")
        answer = input("Please enter a train line. If done with this service, please enter 'stop'. ")
        trainoverlap = train('mta train stop data1.txt')
        trainoverlap.make_list()
        #print(trainoverlap.dict)
        if answer == 'stop':
            print("Thank you so much for using our service. Have a nice day. \n")
            main()
        train1 = train('mta train stop data1.txt')
        if answer not in trainoverlap.dict and answer != "done":
            print("Please enter in a valid train. Thank you.")
            show_stops()
        print ("")
        print ("")
        train1.make_line(answer)

def main():
    job = choose_operation()
    trainoverlap = train('mta train stop data1.txt')
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
        trainoverlap = train('mta train stop data1.txt')
        trainoverlap.make_list()
        trainoverlap.stop_overlap(line1, line2)
    else:
        print("please enter a valid choice.")
        main()
        
        
    
main()
