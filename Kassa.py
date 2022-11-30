class Kassa():
    def __init__(self, tTimeComePersons, pPersons):
        #init params
        self.tTimeComePersons = tTimeComePersons # Через каждый случайный период времени в сек. прихода людей - t [1, t]
        self.pPersons = pPersons # Приход людей - p [1, p]
        
        #Call Function
    def printTest(self):
        print(self.tTimeComePersons + self.pPersons)