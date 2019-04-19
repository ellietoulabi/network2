import requests
import os
import time
import sys
import platform

USERNAME = PASSWORD = API = ""
HOST = "localhost"
PORT = "1104"


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')




while True:
    clear()
    print("""Ticketing System
    1. Log In
    2. Sign Up
    3. Exit""")
    option = sys.stdin.readline()
    if option[:-1] == '1':
        clear()
        print("LOG IN\n")
        while True:
            print("USERNAME : ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD : ")
            PASSWORD = sys.stdin.readline()[:-1]
            request = "http://" + HOST + ":" + PORT + "/" + "login?" + "username=" + USERNAME + "&password=" + PASSWORD
            r = requests.post(request).json()
            if r['code'] == '200':
                print("Logged In Successfully")
                API = r['token']['token']
                time.sleep(2)
                break
            else:
                print("INCORRECT USERNAME AND PASSWORD \nTRY AGAIN ...")

        while True:
            clear()
            print ("MENU")
            print ("1. Send A Ticket")
            print ("2. Get Tickets")
            print ("3. Change Status")
            print ("4. Response To A Ticket (Available Only For Admin)")
            print ("5. Logout")

            func_type = sys.stdin.readline()
            if func_type[:-1] == '1':
                clear()
                print("SEND TICKET\n")
                print("SUBJECT: ")
                SUBJECT = sys.stdin.readline()[:-1]
                print("BODY: ")
                BODY = sys.stdin.readline()[:-1]
                r = "http://" + HOST + ":" + PORT + "/sendticket?token=" + API + "&subject=" + SUBJECT + "&body=" + BODY
                data = requests.post(r).json()
                output = "Your Message ID is : " + str(data['id'])
                print (output)

            if func_type[:-1] == '2':
                clear()
                print("GET TICKETS\n")
                print("1. Adminstrator")
                print("2. User")
                role = sys.stdin.readline()
                if role[:-1] == '1':
                    r = "http://" + HOST + ":" + PORT + "/getticketmod?token=" + API
                    data = requests.post(r).json()
                    if data['code'] == '200':
                        print(data['tickets'] + "\n")
                        Num = int(filter(str.isdigit, str(data['tickets'])))
                        for i in range(Num):
                            index = 'block' + str(i)
                            print (index)
                            print('Subject : ' + data[index]['subject'])
                            print('Body : ' + data[index]['body'])
                            print('Response : ' + str(data[index]['response']))
                            print('Status : ' + data[index]['status'])
                            print('Id : ' + str(data[index]['ID']))
                            print('Date : ' + data[index]['date'])

                            print('\n')
                    else:
                        print (data['message'] + '\n')

                if role[:-1] == '2':
                    r = "http://" + HOST + ":" + PORT + "/getticketcli?token=" + API
                    data = requests.post(r).json()
                    if data['code'] == '200':
                        print(data['tickets'] + "\n\n")
                        Num = int(filter(str.isdigit, str(data['tickets'])))
                        for i in range(Num):
                            index = 'block' + str(i)
                            print (index)
                            print('Subject : ' + data[index]['subject'])
                            print('Body : ' + data[index]['body'])
                            print('Response : ' + str(data[index]['response']))
                            print('Status : ' + data[index]['status'])
                            print('Id : ' + str(data[index]['ID']))
                            print('Date : ' + data[index]['date'])

                            print('\n')
                    else:
                        print (data['message'] + '\n')
                    input("Press Any Key To Continue ...")

            if func_type[:-1] == '3':
                clear()
                print("CHANGE STATUS\n")
                print("1. Adminstrator")
                print("2. User")
                role = sys.stdin.readline()
                if role[:-1] == '1':
                    print("ID:\n >>")
                    ID = sys.stdin.readline()[:-1]
                    print("STATUS\n >>>")
                    STATUS = sys.stdin.readline()[:-1]

                    r = "http://" + HOST + ":" + PORT + "/changestatus?token=" + API + "&id=" + ID + "&status=" + STATUS
                    data = requests.post(r).json()
                    print(data['message'] + '\n')
                    input("Press Any Key To Continue ...")

                if role[:-1] == '2':
                    print("ID:\n >>")
                    ID = sys.stdin.readline()[:-1]
                    r = "http://" + HOST + ":" + PORT + "/closeticket?token=" + API + "&id=" + ID
                    data = requests.post(r).json()
                    print (data['message'] + '\n')

            if func_type[:-1] == '4':
                print("RESPONSE TO A TICKET\n")
                print("ID: ")
                ID = sys.stdin.readline()[:-1]
                print("RESPONSE: ")
                RES = sys.stdin.readline()[:-1]

                r = "http://" + HOST + ":" + PORT + "/restoticketmod?token=" + API + "&id=" + ID + "&body=" + RES
                data = requests.post(r).json()
                print (data['message'] + '\n')

            if func_type[:-1] == '5':
                sys.exit()

    elif option[:-1] == '2':
        clear()
        while True:
            print("SIGN UP AS A NEW ACCOUNT")
            print("USERNAME :\n>>> ")
            USERNAME = sys.stdin.readline()[:-1]
            print("PASSWORD :\n>>>  ")
            PASSWORD = sys.stdin.readline()[:-1]
            print("FIRST NAME :\n>>>  ")
            FIRSTNAME = sys.stdin.readline()[:-1]
            print("LAST NAME :\n>>>  ")
            LASTNAME = sys.stdin.readline()[:-1]
            request = "http://" + HOST + ":" + PORT + "/" + "signup?" + "username=" + USERNAME + "&password=" + PASSWORD + "&firstname=" + \
                      FIRSTNAME + "&lastname=" + LASTNAME
            clear()
            r = requests.post(request).json()
            if str(r['code']) == "200":
                print("Account Created.")
                break
            else:
                print("A Problem Occured!\n")
                clear()

    elif option[:-1] == '3':
        sys.exit()
    else:
        print("There Is Not Such An Option! Try Again.")
