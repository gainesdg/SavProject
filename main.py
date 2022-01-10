import requests
import time as t
import random
from datetime import datetime


# All this method is doing is generating a list of times to use.
# The list given in the example was sort in increasing order, so I sorted mine as well
def generateTimeList(numTimes):
    ListofTimes = []
    numTimes = int(numTimes) + 1
    for x in range(1, numTimes):
        hours = random.randint(1, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        if hours < 10:
            hoursStr = "0" + str(hours)
        else:
            hoursStr = str(hours)
        if minutes < 10:
            minutesStr = "0" + str(minutes)
        else:
            minutesStr = str(minutes)
        if seconds < 10:
            secondsStr = "0" + str(seconds)
        else:
            secondsStr = str(seconds)
        time = hoursStr + ":" + minutesStr + ":" + secondsStr
        ListofTimes.append(time)
    ListofTimes.sort()
    answer = input("Would you like to see the times generated(Yes or No): ")
    if (answer == "Yes") or (answer == "yes"):
        for time in ListofTimes:
            print(time)
    return ListofTimes


# This method converts the List into a Dictionary as it is faster than a list
def convertListtoDict(TimeList):
    TimeDict = {}
    for time in TimeList:
        hours = int(time[:2])
        minutes = int(time[3:5])
        seconds = int(time[6:])
        if not TimeDict:
            TimeDict[hours] = {minutes: [seconds]}
        else:
            if hours in TimeDict:
                curSlice = str(TimeDict[hours])
                minutesVal = int(curSlice[1:2])
                if minutesVal == minutes:
                    TimeDict[hours][minutes].append(seconds)
                else:
                    dicttoAdd = {minutes: [seconds]}
                    TimeDict[hours].update(dicttoAdd)
            else:
                TimeDict[hours] = {minutes: [seconds]}
    return TimeDict


# This method continuously runs once started, its goal is to make get calls to the specified URL once the time is hit
# To save CPU space, the program will sleep for various amounts of time which is explained more in the ReadMe
def sendCalls(year, month, day, TimeDict):
    print("\n")
    print("Calling method now started, will report successfull calls")
    while True:
        # In this section the values for the current time are acquired
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_time_str = str(current_time)
        curr_hour = int(current_time_str[:2])
        curr_min = int(current_time_str[3:5])
        curr_sec = int(current_time_str[6:])
        # If we get to midnight, the day is over and a new list of times is required
        if curr_hour == 0 and curr_min == 0 and curr_sec == 0:
            print("It is a new day, therefore a new list of times is required, script now ending")
            break
        hour_exist = TimeDict.get(curr_hour)
        # If the current hour is not in the list of times, we have the program sleep until we reach a hour that is in
        # the list of times
        if not hour_exist:
            while (not TimeDict.get(curr_hour)) and (curr_hour < 25):
                curr_hour = curr_hour + 1
            if curr_hour > 23:
                print("All times have been called, script now ending")
                break
            nextHour = datetime(year, month, day, curr_hour, 0, 0)
            hourDiff = nextHour - now
            t.sleep(int(hourDiff.seconds))
        else:
            min_exist = TimeDict[curr_hour].get(curr_min)
            # Now that we have a time in the current hour, we see if the current minute exists and if not
            # we have the program sleep until the next minute in the list
            if not min_exist:
                while (not TimeDict[curr_hour].get(curr_min)) and (curr_min < 60):
                    curr_min = curr_min + 1
                nextMin = datetime(year, month, day, curr_hour, curr_min, 0)
                minDiff = nextMin - now
                t.sleep(int(minDiff.seconds))
            else:
                # Now that we have a time in the current minute, we see if the current second exists and if not
                # we have the program sleep until the second in the list
                while TimeDict[curr_hour][curr_min].count(curr_sec) < 1:
                    curr_sec = curr_sec + 1
                nextSec = datetime(year, month, day, curr_hour, curr_min, curr_sec)
                secDiff = nextSec - now
                secDiff = int(secDiff.seconds)
                if secDiff < 60:
                    t.sleep(secDiff)
                    numCalls = TimeDict[curr_hour][curr_min].count(curr_sec)
                    # Now we send the Get request based on how many instances of the time are present and once the calls
                    # are made we have the method sleep for one second to move on to the next time
                    for z in range(0, numCalls):
                        response = requests.get("http://ifconfig.co")
                        response_code = int(response.status_code)
                        strTime = str(curr_hour) + ":" + str(curr_min) + ":" + str(curr_sec)
                        if response_code == 200:
                            print("Congrats, your call at " + strTime + " was successful")
                        else:
                            print("Sorry, your call at " + strTime + "failed with a status code of " + response_code)
                    t.sleep(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    numTimes = input("How many values would you like in the time list: ")
    TimeList = generateTimeList(numTimes)
    TimeDict = convertListtoDict(TimeList)
    # If you would like to test out a specific time, comment out the above three lines and uncomment the two below
    # The example below would add the times 15:16:15, 15:16:15, 15:16:18, 15:34:21
    #TimeDict = {}
    # TimeDict[15] = {16: [15, 15, 18], 34: [21]}
    now = datetime.now()
    year = now.strftime("%Y")
    year = int(year)
    month = now.strftime("%m")
    month = int(month)
    day = now.strftime("%d")
    day = int(day)
    sendCalls(year, month, day, TimeDict)

    #
