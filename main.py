

from numba import jit, cuda
import names
import datetime
from datetime import date
import random
from numba import vectorize
import multiprocessing as mp

#cpupool = mp.Pool(mp.cpu_count())


# @jit(target="Cuda")
def gen(maxnum):
    people = []
    for num in range(0, maxnum):
        name = names.get_full_name()
        namearr = name.split(" ")
        email = namearr[0][0] + namearr[1]
        email = email + randomdigs(4)
        email = email.lower()
        password = topassword(randomdate(2000))
        people.append(email + " " + password)
        # return email, password
    return people


# @jit(target="Cuda")
def randomdate(startyear):
    start_dt = date.today().replace(day=1, month=1, year=startyear).toordinal()
    end_dt = date.today().replace(day=31, month=12, year=startyear + 15).toordinal()
    random_day = date.fromordinal(random.randint(start_dt, end_dt))
    return random_day


def randomdigs(length):
    string = ""
    for num in range(length):
        string = string + str(random.randint(0, 9))
    return string


#@vectorize(['int64(int64,int64)'], target='cuda')
def randomdigsgpu(length, randomnums=0):
    for num in range(length):
        randomnums = randomnums + (random.randint(0, 9) * (10 ** (length - num)))
    return randomnums


# @jit(target="Cuda")
def topassword(doty):
    doty = str(doty)
    dayarr = doty.split("-", 3)
    password = dayarr[1] + dayarr[2] + dayarr[0]
    return password


def check(array, checkval, index):
    if array[index] == checkval:
        return True
    else:
        return False


def crack(array):
    import time
    starttime = time.time()
    index = -1
    for element in array:
        elarr = element.split(" ")
        email = elarr[0]
        index += 1
        start_date = datetime.date(2000, 1, 1)
        end_date = datetime.date(2015, 12, 31)
        delta = datetime.timedelta(days=1)
        while start_date <= end_date:
            # print(start_date)
            password = topassword(start_date)
            if check(array, email + " " + password, index) == True:
                print("Found one! Email: " + email + " and password is " + password)
                break
            else:
                # print(start_date)
                start_date += delta
                continue
    print("Finished in: " + str(time.time()-starttime) + " seconds.")

#print(topassword(randomdate(2000)))
#print(randomdigs(4))
crack(gen(1000))
##print(randomdigsgpu(num))
