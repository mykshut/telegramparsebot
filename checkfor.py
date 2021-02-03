import csv
def openfile():
    with open('users.csv', mode='r', newline='') as users:
        reader = csv.reader(users)
        for line in reader:
            if line != []:
                user, id = line
            print(user, id)


openfile()
