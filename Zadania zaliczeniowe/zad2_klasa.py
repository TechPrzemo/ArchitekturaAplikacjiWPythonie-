"""
Napisz klasę, która będzie implementować generator kolejnych n potęg liczby a.
Użyj metod magicznych __iter__() i __next__().
Liczby n i a powinny być parametrami wejściowymi generatora.
"""

class Power_Generation:
    def __init__(self, a, n):
        self.number = a
        self.power = n
        self.index = 0
    
    #Definiuje co ma sie dziac gdy obiekt klasy jest iterowany    
    def __iter__(self):
        return self #Powinna zwracac iterator, ktory bedzie uzywany do iteracji przez obiekt
    
    #Definiuje co ma byc zwrocone przy wywolaniu next() na obiekcie klasy
    def __next__(self): #Trzeba recznie obsluzyc wyjatek StopIteration w magicznej metodzie next
        if self.index > self.power:
            raise StopIteration
        square_number = self.number ** self.index
        self.index +=1
        return square_number
    
my_generator = Power_Generation(2,10)
for power in my_generator:
    print(power)