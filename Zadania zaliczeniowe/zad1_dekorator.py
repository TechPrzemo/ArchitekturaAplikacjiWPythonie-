"""
Napisz dekorator funkcji, który będzie logował informację o nazwie i typie wszystkich
parametrów wejściowych funkcji dekorowanej w postaci:
{<nazwa_parametru>: <typ_danych>, …}.
"""

import functools

def info_logging(decorative_func):
    @functools.wraps(decorative_func)
    def indoor_function(*args, **kwargs):
        for i, items in enumerate(args):
            print(f"{{arg {i+1}: {type(items)}}} ")
        for key, value in kwargs.items():
            print(f"{{<{key}>: {type(value)}}} ")
        result = f"\nOriginal result: {decorative_func(*args, **kwargs)}" #Decorative function should return original values
        return result
    return indoor_function

@info_logging
def decorative_function(*args, **kwargs):
    return *args, *kwargs


#Main program
if __name__ == "__main__":

    #Examples 
    t = 1,2,3,4,5
    i = 6
    list = ["item1", "item2"]
    
    print(decorative_function(t,i, list,  imie = "Jan", nazwisko = "Kowalski", wiek = 30, miasto = "Warszawa"))

        



 
