import csv
from sHashtable import HashTable
from Package import Package
import datetime

PackageHashtable = HashTable()
DistanceIndexHashtable = HashTable()
timedeliveryHT = HashTable()


truck1 = [1,2,4,5,7,8,10,11,12,17,21,22,23,24,26,27,29,30]
truck2 = [3, 18, 36, 38,6,25,28,32,9]
truck3 = [30,31,33,34,35,37,39,40,13,14,15,16,19,20]

totalDistnace = 0
t1Distance = 0
t2Distance = 0
t3Distance = 0

numberofpackages = 0

timecount = datetime.datetime.strptime('8:00:00', '%H:%M:%S')
timecount2 = datetime.datetime.strptime('8:00:00', '%H:%M:%S')

# Package Hashtable: key = package id, value = Package object
with open('packageCSV.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    for row in readCSV:
        p = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "At Hub", "")
        PackageHashtable.insert(row[0], p)
        numberofpackages += 1

# Hashtable Distance Index: key = package address, value = index of package in Distance
with open('reAddressCSV.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    for row in readCSV:
        DistanceIndexHashtable.insert(row[2], row[0])

# create a 2D array of distance values
file_CSV = open('DistanceCSV.csv')
data_CSV = csv.reader(file_CSV)
list_CSV = list(data_CSV)


# #returns an address of a package with a key
# def getAddress(self, key):
#     return PackageHashtable.get(key).address
#
#
# #returns distance index from a given address
# def getDistanceIndex(self, address):
#     return DistanceIndexHashtable.get(address)


# Gets the Distance Index of a Package using a key
# returns int
def getDistanceIndex(key):
    return DistanceIndexHashtable.get(PackageHashtable.get(str(key)).address)


# returns float, finds the distance between 2 locations using the 2D distance array
def find_distance(rowindex, column):
    distance = list_CSV[int(rowindex)][int(column)]
    if distance == "":
        distance = list_CSV[int(column)][int(rowindex)]
    return float(distance)


# returns int, which package to deliver next using nearest neighbor
def nearest_neighborPackage(currentPackage, truckList):
    smallestDistance = 100
    nextPackage = None
    for package in truckList:
        distance = find_distance(getDistanceIndex(currentPackage), getDistanceIndex(package))
        if distance < smallestDistance:
            smallestDistance = distance
            nextPackage = package
    return nextPackage


# returns float, distance of the closes package
def nearest_neighborDistance(currentPackage, truckList):
    smallestDistance = 100
    for package in truckList:
        distance = find_distance(getDistanceIndex(currentPackage), getDistanceIndex(package))
        if distance < smallestDistance:
            smallestDistance = distance
    return smallestDistance


# returns int, finds the first package starting from the hub
def start_deliveryPackage(truckList):
    smallestDistance = 100
    nextPackage = None
    for package in truckList:
        statusenroute(package)
        distance = find_distance(0, getDistanceIndex(package))
        if distance < smallestDistance:
            smallestDistance = distance
            nextPackage = package
    return nextPackage


# returns float, the distance to the first package from the hub
# def start_deliveryDistance(truckList):
#     smallestDistance = 100
#     for package in truckList:
#         distance = find_distance(0, getDistanceIndex(package))
#         if distance < smallestDistance:
#             smallestDistance = distance
#     return smallestDistance

# returns int, distance of the next package from hub
def start_deliveryDistance(package):
    return find_distance(0, getDistanceIndex(package))


# returns time, finds the time the package was delivered
def addTime(time, distance):
    deliverytimeminutes = (distance / 18) * 60
    newtime = time + datetime.timedelta(minutes=deliverytimeminutes)
    return newtime


# takes in user input a time and a package/all.
# prints out the status of a package at time.
# def lookup():
#     while True:
#         #get time from user and format to a time object.
#         input_time = datetime.datetime.strptime(input("Enter a time (08:00): "), "%H:%M").time()
#
#         packageinput = input("Enter a package ID or 'end': ")
#         print(PackageHashtable.get(packageinput))
#         if packageinput.__contains__("end"):
#             break


def getstatus():
    for package in range(1, numberofpackages):
        print("Package "+ package + PackageHashtable.get(str(package)).status)


#changes package status to delivered
def statusdelivered(packageid, trucknum):
    packageid = str(packageid)
    package = PackageHashtable.get(packageid)
    package.status = "delivered"
    if trucknum == 1 or 3:
        package.timedelivered = str(timecount.time())
    if trucknum == 2:
        package.timedelivered = str(timecount2.time())
    # PackageHashtable.delete(packageid)
    PackageHashtable.insert(packageid, package)


#changes package status to enroute
def statusenroute(packageid):
    packageid = str(packageid)
    package = PackageHashtable.get(packageid)
    package.status = "enroute"
    # package.timedelivered = str(timecount.time())
    PackageHashtable.insert(packageid, package)


def starttruck(truck, distance, count):
    lastDelivered = start_deliveryPackage(truck)
    distance += start_deliveryDistance(lastDelivered)
    truck1.remove(lastDelivered)
    count = addTime(count, distance)
    # updates the status and delivery time
    statusdelivered(lastDelivered)


# first input from user
while True:
    input_main = input("1: Total distance traveled\n"
                       "2: Package status at a given time\n"
                       "3: Individual package status\n"
                       "or 'end' to exit\n\n"
                       "Enter: ")
    if input_main in ("1", "2", "3", "end"):
        break
    else:
        print("invalid input")


if input_main == "2":
    while True:
        try:
            input_time = datetime.datetime.strptime(input("Enter a time (08:00): "), "%H:%M").time()
        except:
            print("invalid input")
        else:
            break


elif input_main == "3":
    while True:
        input_packageid = input("Enter a package id: ")
        if input_packageid in (range(1, 40)):
            break
        else:
            print("invalid input")


elif input_main == "end":
    exit()




count = 0

lastDelivered = 0

while truck1 != []:

    if t1Distance == 0:
        lastDelivered = start_deliveryPackage(truck1)
        t1Distance += start_deliveryDistance(lastDelivered)
        truck1.remove(lastDelivered)
        timecount = addTime(timecount, t1Distance)
        statusdelivered(lastDelivered, 1)


    nextDistance = nearest_neighborDistance(lastDelivered, truck1)
    t1Distance += nextDistance
    lastDelivered = nearest_neighborPackage(lastDelivered, truck1)
    truck1.remove(lastDelivered)

    # placement before added to timecount to determine if package is in the right time.
    if(input_main == "2"):
        if (input_time < addTime(timecount, nextDistance).time()):
            break

    timecount = addTime(timecount, nextDistance)
    statusdelivered(lastDelivered, 1)
    if truck1 == []:
        nextDistance = find_distance(0, getDistanceIndex(lastDelivered))
        t1Distance += nextDistance
        timecount = addTime(timecount, nextDistance)




while truck2 != []:

    if t2Distance == 0:

        if input_main == "2":
            if input_time < timecount2.time():
                break

        lastDelivered = start_deliveryPackage(truck2)
        t2Distance += start_deliveryDistance(lastDelivered)
        truck2.remove(lastDelivered)
        timecount2 = addTime(timecount2, t2Distance)

        if input_main == "2":
            if input_time < timecount2.time():
                break
        statusdelivered(lastDelivered, 2)

    nextDistance = nearest_neighborDistance(lastDelivered, truck2)
    t2Distance += nextDistance
    lastDelivered = nearest_neighborPackage(lastDelivered, truck2)
    truck2.remove(lastDelivered)

    if (input_main == "2"):
        if (input_time < addTime(timecount2, nextDistance).time()):
            break

    timecount2 = addTime(timecount2, nextDistance)
    statusdelivered(lastDelivered, 2)
    if truck2 == []:
        t2Distance += find_distance(0, getDistanceIndex(lastDelivered))
        t2Distance += nextDistance
        timecount2 = addTime(timecount2, nextDistance)



while truck3 != []:

    if t3Distance == 0:

        if (input_main == "2"):
            if (input_time < addTime(timecount, nextDistance).time()):
                break

        lastDelivered = start_deliveryPackage(truck3)
        t3Distance += start_deliveryDistance(lastDelivered)
        truck3.remove(lastDelivered)
        timecount = addTime(timecount, t3Distance)
        statusdelivered(lastDelivered, 3)

    nextDistance = nearest_neighborDistance(lastDelivered, truck3)
    t3Distance += nextDistance
    lastDelivered = nearest_neighborPackage(lastDelivered, truck3)
    truck3.remove(lastDelivered)

    if (input_main == "2"):
        if (input_time < addTime(timecount, nextDistance).time()):
            break

    timecount = addTime(timecount, nextDistance)
    statusdelivered(lastDelivered, 3)
    if truck3 == []:
        t3Distance += find_distance(0, getDistanceIndex(lastDelivered))
        t3Distance += nextDistance
        timecount2 = addTime(timecount, nextDistance)

# print(timecount.time())


# PackageHashtable.print()
# lookup()
totalDistnace = t1Distance + t2Distance + t3Distance

if (input_main == "1"):
    print(totalDistnace)

if (input_main == "2"):
    for x in range(1, numberofpackages+1):
        print(str(x) + ": " + PackageHashtable.get(str(x)).status + " " + PackageHashtable.get(str(x)).timedelivered)

