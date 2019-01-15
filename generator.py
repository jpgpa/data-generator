import csv
import random
import string
import json
import sys

#names
names = []
lastnames = []
firstName = [1, 2]
lastName = [1, 2, 3, 4]

#emails
emailSufix = ["@gmail.com", "hotmail.com", "@outlook.com", "@iol.pt", "@sapo.pt", "@live.com.pt"]
emailPrefix = [1, 2, 3, 4]

#usernames
usernames = {}
usernamePattern = [1, 2, 3, 4]

#credit card
creditCards = {}
creditCardsPrefix = [4,5,6]

#date
months = [1, 3, 5, 7, 8, 10, 12]

#nif
nifs = {}
nifPrefix = [1, 2]

#export stuff
personInfos = []

#cc
alfabetoDict = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15', 'G': '16', 'H': '17', 'I': '18', 'J': '19', 'K': '20',
 'L': '21', 'M': '22', 'N': '23', 'O': '24', 'P': '25', 'Q': '26', 'R': '27', 'S': '28', 'T': '29', 'U': '30', 'V': '31', 'W': '32', 'X': '33',
  'Y': '34', 'Z': '35'}

alfabeto = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

ccs = {}


# function to load first name csv file to array
def loadNames ():
    with open('names.csv') as csvfile:
        reader = csv.reader(csvfile)
        iterator = 0
        for row in reader:
            iterator += 1
            entry = {'id': iterator, 'name': row[0], 'gender': row[1]}
            names.append(entry)
    with open('apelidos.csv') as lastnamescsv:
        reader = csv.reader(lastnamescsv)
        iterator = 0
        for row in reader:
            iterator+=1
            entry = {'id': iterator, 'name': row[0]}
            lastnames.append(entry)


# exports generated data to a csv file
def exportToCsv (filename):
    with open(filename+".csv", 'wb') as csvfile:
        fieldnames = ['nif', 'name', 'cc', 'birthdate', 'username', 'email', 'password', 'creditCard', 'altura', 'peso', 'gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for p in personInfos:
            writer.writerow(p)

# exports generated data to json file
def exportToJson (filename):
    with open(filename+".json", 'wb') as jsonfile:
        json.dump(personInfos, jsonfile, ensure_ascii=False, indent=4, separators=(',', ': '))
        
# exports generated data to html file as a table
def exportToHtml (filename):
    with open (filename+".html", 'wb') as htmlfile:
        htmlfile.write("<!DOCTYPE html><html><body><h2>Generated Data Results: </h2><table width=\"100%\" cellspacing=\"2\" cellpadding=\"0\" border=\"0\" align=\"center\" bgcolor=\"#ff6600\" ><tr>")
        htmlfile.write("<th>#</th><th>Name</th><th>Gender</th><th>Birthdate</th><th>Height</th><th>Weight</th><th>Email</th>")
        htmlfile.write("<th>Username</th><th>Password</th><th>National ID (Cartao de Cidadao)</th><th>NIF</th><th>Credit Card</th></tr>")
        count = 0
        for p in personInfos:
            count+=1
            htmlfile.write("<tr bgcolor=\"#ffffff\"><th>"+str(count)+"</th><th>"+p["name"]+"</th><th>"+p["gender"]+"</th><th>"+p["birthdate"]+"</th><th>"+str(p["altura"])+"</th>")
            htmlfile.write("<th>"+str(p["peso"])+"</th><th>"+p["email"]+"</th><th>"+p["username"]+"</th><th>"+p["password"]+"</th>")
            htmlfile.write("<th>"+p["cc"]+"</th><th>"+str(p["nif"])+"</th><th>"+str(p["creditCard"])+"</th></tr>")
        htmlfile.write("</table></body></html>")

# exports generated data to txt file
def exportToTxt (filename):
    with open (filename+".txt", 'wb') as txtfile:
        txtfile.write("| Name"+txtSpaces(" Name", 60)+"| Birthdate\t| Height| Weight| National ID\t| NIF\t\t| Email"+txtSpaces("Email", 40)+"| Username"+txtSpaces("Username", 25)+"| Password"+txtSpaces("Password", 15)+"| Credit Card\t\t\t| Gender|\n")
        for p in personInfos:
            txtfile.write("|"+p['name']+txtSpaces(p['name'], 60)+"| "+p['birthdate']+" \t| "+str(p['altura'])+"\t| "+str(p['peso'])+"\t| "+p['cc']+"\t| "+str(p['nif'])+"\t| "+p['email']+txtSpaces(p['email'], 40)+"| "+p['username']+txtSpaces(p['username'], 25)+"| "+p['password']+txtSpaces(p['password'], 15)+"| "+str(p['creditCard'])+"\t| "+p['gender']+"\t\t|\n")

# adds white spaces to string to have a certain length
def txtSpaces(name, number):
    count = len(name.decode("utf-8"))
    st = ""
    for x in range(count, number):
        st+=" "
    return st

# validate if  nif already exists
def checkNifExists (pretendedNif):
    return nifs.get(pretendedNif) == None

# check if cc number already exists
def checkCCExists (ccNumber):
    return ccs.get(ccNumber) == None

# check if passed month has 31 days
def checkMonth(month):
    for x in months:
        if x == month:
            return True
    return False    

# validate credit card using luhn's algorithm
def validateCreditCard(s):
    s.reverse()

    if 0 > len(s) or len(s) > 16:
        return False

    sum = 0
    alt = False

    for i in s:
        if alt:
            i *= 2
            if i > 9:
                i -= 9
        sum += i
        alt = not alt

    return not (sum % 10)
    
# checks that the credit card is not already generated
def checkCreditCard(cc):
    return creditCards.get(cc) == None

# generates a random height
def generateAltura():
    return round(random.uniform(1.45, 1.98), 2)

# generates a random weight
def generatePeso():
    return random.randrange(45, 100)

# generates a credit card using random values
def generateCreditCard():
    workDone = True

    while workDone:
        creditCard = []
        count = 0
        while count < 16:
            if count == 0:
                randomNumber = random.choice(creditCardsPrefix)
            else:
                randomNumber = random.randrange(0, 9)
            creditCard.append(randomNumber)
            count += 1

        creditCardString = ""
        for number in creditCard:
            creditCardString = creditCardString + str(number)
        
        if validateCreditCard(creditCard):
            if checkCreditCard(creditCardString):
                workDone = False
                creditCards[creditCardString] = creditCardString
                return creditCardString    
        else:
            creditCard = []
        

# generates a random password from 5 to 12 chars
def generatePassword():
    chars = string.ascii_uppercase + string.digits
    size = random.randrange(5, 12)
    return ''.join(random.choice(chars) for _ in range(size))


#generates email from a list of patterns
def generateEmail(name, username, year):
    nameInList = name.split(" ")

    emailPattern = random.choice(emailPrefix)
    emailEnding = random.choice(emailSufix)

    someRandomValue = random.randrange(1, 20)

    if emailPattern == 1:
        email = nameInList[1] + str(someRandomValue) + emailEnding
    elif emailPattern == 2:
        email = username + "_" + str(someRandomValue) + emailEnding
    elif emailPattern == 3:
        email = nameInList[1] + nameInList[-1] + str(year) + emailEnding
    else:
        email = str(someRandomValue) + nameInList[-1] + "." + str(year) + emailEnding
    
    return email

# generates username from a list of patterns
def generateUsername(name, age):
    nameInList = []
    nameInList = name.split(" ")
    
    selectedPattern = random.choice(usernamePattern)

    if selectedPattern == 1:
        username = nameInList[1] + str(age[2])
    elif selectedPattern == 2:
        username = nameInList[-1] + str(age[2])
    elif selectedPattern == 3:
        someNumber = random.randrange(1,20)
        username = nameInList[1] + str(someNumber) + nameInList[-1]
    else:
        someNumber = random.randrange(1,20)
        username = nameInList[1] + str(someNumber)
    return username

# generates birthdate from 1950 to 2001
def generateAges():
    year = random.randrange(1950, 2001)
    month = random.randrange(1, 12)

    if checkMonth(month):
        day = random.randrange(1, 31)
    elif month == 2:
        day = random.randrange(1, 28)
    else:
        day = random.randrange(1, 30)
    
    date = [day, month, year]
    return date



# generate valid cc control number 
def generatevalidCCControlNumber (ccDict):
    total = 0
    secondDigit = True
    count = 0
    while count < 12:
        value = int(ccDict.get(str(count)))
        if secondDigit:
            value *= 2
            if value > 9:
                value -= 9
        total += value
        secondDigit = not secondDigit
        count += 1
    return (total % 10) == 0



# generate a valid portuguese cc number
def generateCC (): 
    workDone = True
    while workDone:
        ccDict = {}
        number1 = random.randrange(0, 9)
        ccDict['0'] = number1
        number2 = random.randrange(0, 9)
        ccDict['1'] = number2
        number3 = random.randrange(0, 9)
        ccDict['2'] = number3
        number4 = random.randrange(0, 9)
        ccDict['3'] = number4
        number5 = random.randrange(0, 9)
        ccDict['4'] = number5
        number6 = random.randrange(0, 9)
        ccDict['5'] = number6
        number7 = random.randrange(0, 9)
        ccDict['6'] = number7
        number8 = random.randrange(0, 9)
        ccDict['7'] = number8
        controlNumber = random.randrange(0, 9)
        ccDict['8'] = controlNumber

        letter1 = random.choice(alfabeto)
        numberOfLetter1 = alfabetoDict[letter1]
        ccDict['9'] = numberOfLetter1

        letter2 = random.choice(alfabeto)
        numberOfLetter2 = alfabetoDict[letter2]
        ccDict['10'] = numberOfLetter2

        lastNumber = random.randrange(0, 9)
        ccDict['11'] = lastNumber
        if generatevalidCCControlNumber(ccDict):
            thisCC = str(ccDict['0']) + str(ccDict['1']) + str(ccDict['2']) + str(ccDict['3']) + str(ccDict['4']) + str(ccDict['5']) + str(ccDict['6']) + str(ccDict['7']) + str(ccDict['8']) + letter1 + letter2 + str(ccDict['11'])
            if checkCCExists(thisCC): 
                ccs[thisCC] = thisCC
                workDone = False
                return thisCC



# generate a valid portuguese nif inexistent at the moment
def generateNif ():
    workDone = True
    while workDone:
        thisNifPrefix = random.choice(nifPrefix)

        nif2number = random.randrange(0, 9)
        nif3number = random.randrange(0, 9)
        nif4number = random.randrange(0, 9)
        nif5number = random.randrange(0, 9)
        nif6number = random.randrange(0, 9)
        nif7number = random.randrange(0, 9)
        nif8number = random.randrange(0, 9)

        thisNifPrefixCheck = int(thisNifPrefix) * 9
        nif2numberCheck = int(nif2number) * 8
        nif3numberCheck = int(nif3number) * 7
        nif4numberCheck = int(nif4number) * 6
        nif5numberCheck = int(nif5number) * 5
        nif6numberCheck = int(nif6number) * 4
        nif7numberCheck = int(nif7number) * 3
        nif8numberCheck = int(nif8number) * 2
        
        total = int(thisNifPrefixCheck) + int(nif2numberCheck) + int(nif3numberCheck) + int(nif4numberCheck) + int(nif5numberCheck) + int(nif6numberCheck) + int(nif7numberCheck) + int(nif8numberCheck)
        divisao = total % 11
        
        if int(divisao) == 0:
            thisNifFinalValue = 0
        elif int(divisao) == 1:
            thisNifFinalValue = 0
        else:
            thisNifFinalValue = 11 - int(divisao)
        
        thisFinalNif = str(thisNifPrefix) + str(nif2number) + str(nif3number) + str(nif4number) + str(nif5number) + str(nif6number) + str(nif7number) + str(nif8number) + str(thisNifFinalValue)
        
        if checkNifExists(int(thisFinalNif)):
            workDone = False
            nifs[thisFinalNif] = thisFinalNif
            return thisFinalNif

# generate a name from specific gender
def generateName (gender):
    workDone = True
    while workDone:
        selectedName = random.choice(names)
        if selectedName['gender'] == gender:
            return selectedName['name']

# generate a last name
def generateLastName ():
    workDone = True
    while workDone:
        selectedName = random.choice(lastnames)
        return selectedName['name']

# generating process
def generatePerson(firstNamesNumber, lastNamesNumber, gender):
    fullName = []
    count = 0
    while int(count) < int(firstNamesNumber):
        fullName.append(generateName(gender))
        count += 1

    count = 0
    while int(count) < int(lastNamesNumber):
        fullName.append(generateLastName())
        count += 1

    name = ""
    for x in fullName:
        name = name + " " + x
    
    thisNif = generateNif()
    thisCC = generateCC()
    thisAge = generateAges()
    thisUsername = generateUsername(name, thisAge)
    thisEmail = generateEmail(name, thisUsername, thisAge[2])
    thisPassword = generatePassword()
    thisCreditCard = generateCreditCard()
    thisAltura = generateAltura()
    thisPeso = generatePeso()

    finalDate = str(thisAge[0]) + "/" + str(thisAge[1]) + "/" + str(thisAge[2])
    entry = {'nif': thisNif, 'name': name, 'cc': thisCC, 'birthdate': finalDate, 'username': thisUsername, 'email': thisEmail, 'password': thisPassword, 'creditCard': thisCreditCard, 'altura': thisAltura, 'peso': thisPeso, 'gender': gender}
    personInfos.append(entry)
    
# starting generate process
def startGenerating (numberOfPersons, womenNumber, menNumber):
    print("Generating your data, please wait...")
    #generating womens
    count = 0
    while int(count) < int(womenNumber):
        iteratedNumberofFN = random.choice(firstName)
        iteratedNumberofLN = random.choice(lastName)
        generatePerson(iteratedNumberofFN, iteratedNumberofLN, 'F')
        count += 1
        sys.stdout.write("\r%d%% done" % int(count/(float(numberOfPersons))*100))
        sys.stdout.flush()
    
    #generating mens
    countMens = 0
    while int(countMens) < int(menNumber):
        iteratedMenNumberFN = random.choice(firstName)
        iteratedMenNumberLN = random.choice(lastName)
        generatePerson(iteratedMenNumberFN, iteratedMenNumberLN, 'M')
        countMens += 1
        sys.stdout.write("\r%d%% done" % int((count+countMens)/(float(numberOfPersons))*100)) 
        sys.stdout.flush()
    print("")

    choice = raw_input("Wich format do you wish to export? (1-CSV       2-JSON      3-HTML      4-TXT)")
    if choice == "1":
        filenameToSave = raw_input("Name of the CSV file to export?  ")
        exportToCsv(filenameToSave)
    elif choice == "2":
        filenameToSave = raw_input("Name of the JSON file to export?   ")
        exportToJson(filenameToSave)
    elif choice == "3":
        filenameToSave = raw_input("Name of the HTML file to export?  ")
        exportToHtml(filenameToSave)
    elif choice == "4":
        filenameToSave = raw_input("Name of the TXT file to export?  ")
        exportToTxt(filenameToSave)

# function that loads to an array all names from csv files
# ask the number of new person data to generate 
# and from those how many are women
def startMenu ():
    loadNames()
    numberOfPersons = raw_input("How many persons you need? ")
    womenNumber = raw_input("From those %s persons how many will be woman? " % numberOfPersons)
    if int(womenNumber) > int(numberOfPersons):
        print("Error! You selected more womens then all persons")
    else:
        menNumber = int(numberOfPersons) - int(womenNumber)
        print("you will have %s mens and %s womens" %(menNumber, womenNumber))
        startGenerating(numberOfPersons, womenNumber, menNumber)

startMenu()
