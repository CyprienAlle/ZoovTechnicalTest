import datetime
import csv
import random

#Initialize list with the following structure [City Name, Current number of available bikes, Max number of available bikes]
cities_and_bikes = [
    ["Lille", 400, 400], 
    ["Roubaix", 250, 250], 
    ["Boulogne sur Mer", 75, 75], 
    ["Calais", 150, 150], 
    ["Dunkerque", 125, 125]
]

#Variables used to determine if any bikes will break down
bike_breakdown_numbers = [0,1,2,3]
bike_breakdown_probabilities = [0.6, 0.2, 0.1, 0.1]

#Variable used to determine how quickly bikes are repaired
bike_repair_numbers = [0,1,2,3]
bike_repair_probabilities = [0.4, 0.2, 0.2, 0.2]

#Variables used to determine revenue
fix_fee = 1
fee_per_minute = 0.3

#Create list with all dates from relevant time period
numdays = 366
base = datetime.date.fromisoformat("2020-01-01")
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]

#Initialize the data used to create the csv file with the column names
relevant_data = [
    ["Date", "City", "Number of trips", "Number of users", "Bikes available", "Broken bikes", "Repaired bikes",
     "Total duration", "Total distance", "Revenue"]
]

#Loops over the relevant dates and cities to fill the data used to create the csv file
for x in date_list:
    for y in cities_and_bikes:

        #Determine what the upper edge used to determine the number of trips per day is based on the month and the number of available bikes
        if x.month in [6,7,8,9]:
            max_trips = y[1]*4
        elif x.month in [4,5,10,11]:
            max_trips = y[1]*3
        else:
            max_trips = y[1]*2

        trips = random.randint(0,max_trips)

        #Number of users is randomize with boundaries based on number of trips
        users = random.randint(int(trips/3),trips)

        #Logic behind the number of available bikes
        temp_bikes = y[1]

        if temp_bikes < y[2]:
            repaired_bikes = random.choices(bike_repair_numbers, weights = bike_repair_probabilities)[0]
            if temp_bikes + repaired_bikes > y[2]:
                repaired_bikes = y[2] - temp_bikes
                temp_bikes = y[2]
            else:
                temp_bikes += repaired_bikes
        else:
            repaired_bikes = 0

        broken_bikes = random.choices(bike_breakdown_numbers, weights = bike_breakdown_probabilities)[0]
        available_bikes = temp_bikes - broken_bikes

        y[1] = available_bikes    

        #Total duration of all trips (in minutes) 
        duration = round(trips * random.triangular(10,50), 2)

        #Total distance of trip based on duration and a random average speed (in km)
        distance = round(duration * random.triangular(10,20) / 60, 2)

        #Revenue
        revenue = round(trips*fix_fee + duration*fee_per_minute, 2)

        #Add a row to the relevant data list with all the figures generated above
        temp_list = [x, y[0], trips, users, available_bikes , broken_bikes, repaired_bikes, duration, distance, revenue]
        relevant_data.append(temp_list)

#Add all the data from the list created above to the csv file
with open('zoov_test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(relevant_data)
