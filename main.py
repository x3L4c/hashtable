"""
Alex Carpentieri
001214187
"""

# The overall time complexity of this program is O(n^2)
# The overall space complexity for this program is O(n)

from Hashtable import HashTable
from Package import Package
import datetime
import csv

package_hashtable = HashTable()
distance_index_hashtable = HashTable()


# 18 free: 2, 4, 5, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 39
# same truck T1 or T2(+before 1030): 13, 14, 15, 16, 19, 20
# only t2: 3, 18, 36, 38
# before 1030am: 1, 29, 30, 31, 34, 37, 40
# before 9am: 15
# between 905-1030am: 6, 25
# after 905am: 9, 28, 32


truck1 = [1, 13, 14, 15, 16, 17, 19, 20, 27, 29, 30, 31, 34, 37, 40]  # 15 packages
truck2 = [2, 3, 4, 5, 6, 18, 25, 36, 38]  # 9 packages
truck3 = [7, 8, 9, 10, 11, 12, 21, 22, 23, 24, 26, 28, 32, 33, 35, 39]  # 16 packages

totalDistance = 0
t1Distance = 0
t2Distance = 0
t3Distance = 0

package_amount = 0

time_count = datetime.datetime.strptime('8:00:00', '%H:%M:%S')
time_count2 = datetime.datetime.strptime('9:05:00', '%H:%M:%S')

# Package Hashtable: key = package id, value = Package object
# time complexity: O(n)  time will increase linearly with increased packages
# space complexity: O(n)  space will increase linearly with increased packages
with open('PackageCSV.csv') as csv_file:
    readCSV = csv.reader(csv_file)
    for row in readCSV:
        p = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "At Hub", "")
        package_hashtable.insert(row[0], p)
        package_amount += 1

# Hashtable Distance Index: key = package address, value = index of package in Distance
# time complexity O(n)  time will increase linearly with increased addresses
# Space complexity O(n)  space will increase linearly with increased addresses
with open('AddressCSV.csv') as csv_file:
    readCSV = csv.reader(csv_file)
    for row in readCSV:
        distance_index_hashtable.insert(row[2], row[0])

# create a 2D array of distance values
# time complexity O(n)   time will increase linearly with increased distances
# space complexity O(n)  space will increase linearly with increased distances
file_CSV = open('DistanceCSV.csv')
data_CSV = csv.reader(file_CSV)
list_CSV = list(data_CSV)


# return type int, Gets the Distance Index of a Package using a key
# time complexity: O(1)  the hashtable has a constant look-up time
def distance_index_return(key):
    return distance_index_hashtable.get(package_hashtable.get(str(key)).address)


# return type float, finds the distance between 2 distances using the 2D distance array
# time complexity: O(1)  constant look up time of an array
def find_distance(row_index, column):
    distance = list_CSV[int(row_index)][int(column)]
    if distance == "":
        distance = list_CSV[int(column)][int(row_index)]
    return float(distance)


# return type int, the package to deliver next using nearest neighbor
# time complexity: O(n)   time will increase linearly with the increase of packages in the truck
def nearest_neighbor_package(current_package, truck_list):
    smallest_distance = 100
    next_package = None
    for package in truck_list:
        distance = find_distance(distance_index_return(current_package), distance_index_return(package))
        if distance < smallest_distance:
            smallest_distance = distance
            next_package = package
    return next_package


# return type float, the distance of the closes package
# time complexity: O(n)  time will increase linearly with the amount of packages in the truck
def nearest_neighbor_distance(current_package, truck_list):
    smallest_distance = 100
    for package in truck_list:
        distance = find_distance(distance_index_return(current_package), distance_index_return(package))
        if distance < smallest_distance:
            smallest_distance = distance
    return smallest_distance


# return type int, finds the first package starting from the hub
# time complexity: O(n)  time will increase linearly with the amount of packages in the truck
def start_delivery_package(truck_list):
    smallest_distance = 100
    next_package = None
    for package in truck_list:
        status_enroute(package)
        distance = find_distance(0, distance_index_return(package))
        if distance < smallest_distance:
            smallest_distance = distance
            next_package = package
    return next_package


# return type int, the distance of the next package from hub
# time complexity: O(1)  utilize functions with constant look up times.
def start_delivery_distance(package):
    return find_distance(0, distance_index_return(package))


# return type time, adds the delivery time to old time
def add_time(time, distance):
    delivery_time_minutes = (distance / 18) * 60
    new_time = time + datetime.timedelta(minutes=delivery_time_minutes)
    return new_time


# prints the status of all packages
# time complexity: O(n)   time increases linearly with the increase of packages
def getstatus():
    for package in range(1, package_amount):
        print("Package " + str(package) + package_hashtable.get(str(package)).status)


# changes package status to delivered
# time complexity: O(1)  hashtable lookup and insert have a constant time
# space complexity: O(1)  insert occurs once per function call
def status_delivered(package_id, truck_id):
    package_id = str(package_id)
    package = package_hashtable.get(package_id)
    package.status = "delivered"
    if truck_id == 1 or 3:
        package.time_delivered = str(time_count.time())
    if truck_id == 2:
        package.time_delivered = str(time_count2.time())
    package_hashtable.insert(package_id, package)


# changes package status to en route
# time complexity: O(1)   hashtable look up and insert has a constant time
# space complexity: O(1)  insert occurs once per function call
def status_enroute(package_id):
    package_id = str(package_id)
    package = package_hashtable.get(package_id)
    package.status = "en route"
    package_hashtable.insert(package_id, package)


# handles truck operations: remove delivered packages, updates: time, distance, and status
# time complexity: O(1)  the functions utilized have constant time
def start_truck(truck, distance, count):
    last_delivered = start_delivery_package(truck)
    distance += start_delivery_distance(last_delivered)
    truck1.remove(last_delivered)
    add_time(count, distance)
    # updates the status and delivery time
    status_delivered(last_delivered, truck)


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


elif input_main == "end":
    exit()

lastDelivered = 0

# while there are
# packages in truck 1
# time complexity: O(n^2)  The time will increase quadratically as more packages are added. The first loop, while loop,
# continues while there are packages in the truck, the second loop inside the first loop occurs from the functions
# getstatus, nearest_neighbor_package, nearest_neighbor_distance, start_delivery_package, where each of these functions
# loop through lists of packages. A loop inside of another loop will grow quadratically.
# space complexity: O(n)  space will increase linearly as more packages are added.
while truck1:

    if t1Distance == 0:
        lastDelivered = start_delivery_package(truck1)
        t1Distance += start_delivery_distance(lastDelivered)
        truck1.remove(lastDelivered)
        time_count = add_time(time_count, t1Distance)
        status_delivered(lastDelivered, 1)

    nextDistance = nearest_neighbor_distance(lastDelivered, truck1)
    t1Distance += nextDistance
    lastDelivered = nearest_neighbor_package(lastDelivered, truck1)
    truck1.remove(lastDelivered)

    # placement before added to time_count to determine if package is in the right time.
    if input_main == "2":
        if input_time < add_time(time_count, nextDistance).time():
            break

    time_count = add_time(time_count, nextDistance)
    status_delivered(lastDelivered, 1)
    if not truck1:
        nextDistance = find_distance(0, distance_index_return(lastDelivered))
        t1Distance += nextDistance
        time_count = add_time(time_count, nextDistance)

# time complexity: O(n^2)  The time will increase quadratically as more packages are added. Explanation can be
# found above while loop of truck 1.
# space complexity: O(n)  The space will increase linearly as more packages are added.
while truck2:

    if t2Distance == 0:

        if input_main == "2":
            if input_time < time_count2.time():
                break

        lastDelivered = start_delivery_package(truck2)
        t2Distance += start_delivery_distance(lastDelivered)
        truck2.remove(lastDelivered)
        time_count2 = add_time(time_count2, t2Distance)

        if input_main == "2":
            if input_time < time_count2.time():
                break
        status_delivered(lastDelivered, 2)

    nextDistance = nearest_neighbor_distance(lastDelivered, truck2)
    t2Distance += nextDistance
    lastDelivered = nearest_neighbor_package(lastDelivered, truck2)
    truck2.remove(lastDelivered)

    if input_main == "2":
        if input_time < add_time(time_count2, nextDistance).time():
            break

    time_count2 = add_time(time_count2, nextDistance)
    status_delivered(lastDelivered, 2)
    if not truck2:
        t2Distance += find_distance(0, distance_index_return(lastDelivered))
        t2Distance += nextDistance
        time_count2 = add_time(time_count2, nextDistance)

# time complexity: O(n^2)  The time will go quadratically as more packages are added. Explanation can be found above
# while loop of truck 1.
# space complexity: O(n)  the space will increase linearly as more packages are added.
while truck3:

    if t3Distance == 0:

        if input_main == "2":
            if input_time < add_time(time_count, nextDistance).time():
                break

        lastDelivered = start_delivery_package(truck3)
        t3Distance += start_delivery_distance(lastDelivered)
        truck3.remove(lastDelivered)
        time_count = add_time(time_count, t3Distance)
        status_delivered(lastDelivered, 3)

    nextDistance = nearest_neighbor_distance(lastDelivered, truck3)
    t3Distance += nextDistance
    lastDelivered = nearest_neighbor_package(lastDelivered, truck3)
    truck3.remove(lastDelivered)

    if input_main == "2":
        if input_time < add_time(time_count, nextDistance).time():
            break

    time_count = add_time(time_count, nextDistance)
    status_delivered(lastDelivered, 3)
    if not truck3:
        t3Distance += find_distance(0, distance_index_return(lastDelivered))
        t3Distance += nextDistance
        time_count2 = add_time(time_count, nextDistance)

totalDistance = t1Distance + t2Distance + t3Distance

if input_main == "1":
    print(str(totalDistance) + " miles")


# time complexity: O(n)  time grows linearly with increased packages
if input_main == "2":
    for x in range(1, package_amount + 1):
        if package_hashtable.get(str(x)).status == "delivered":
            print(str(x) + ": " + package_hashtable.get(str(x)).status + " at: " + package_hashtable.get(
                str(x)).time_delivered + " to: " + package_hashtable.get(str(x)).address)
        else:
            print(str(x) + ": " + package_hashtable.get(str(x)).status + " " + package_hashtable.get(str(x)).time_delivered)


if input_main == "3":
    while True:
        input_package_id = input("Enter a package id: ")
        if int(input_package_id) in (range(1, 41)):
            print(package_hashtable.get(input_package_id))
        else:
            print("invalid input")
