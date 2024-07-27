"""
Za pomocą API zwracającego informacje dot. uniwersytetów w danym państwie:
http://universities.hipolabs.com/search?country=<nazwa_kraju_eng>
wyświetl nazwy uniwersytetów z 15 wybranych krajów w postaci:
{<nazwa_kraju>: [<nazwa_uniwersytet1>, <nazwa_uniwersytet2>,...], …}.
W celu przyspieszenia pobierania danych, wykorzystaj moduł threading do realizacji
wielowątkowego pobierania informacji.
"""

import requests

from concurrent.futures import ThreadPoolExecutor
import random
import time

COUNTRIES_NUMBER = 15
MAX_THREAD_NUMBER = 16

def fetch_univer_for_country(country):
    url = "http://universities.hipolabs.com/search" 
    country_url = f"{url}?country={country}"
    country_resp = requests.get(country_url)
    return country, [uni_name['name'] for uni_name in country_resp.json()]

def fetch_country():
    url = "http://universities.hipolabs.com/search" 
    univer_resp = requests.get(url)
    universities = univer_resp.json()
    return universities

if __name__ == "__main__":
    start = time.time()
    
    countries = set() #Zapobieganie powtorzeniom
    
    universities = []
    
    with ThreadPoolExecutor(max_workers=MAX_THREAD_NUMBER) as executor:
        thread_results_1 = {executor.submit(fetch_country)}
        
        for result_1 in thread_results_1:
            university_1 = result_1.result()
            universities = university_1
        
    for university in universities:
        country = university['country'] # country to klucz slownika university
        if country:
            countries.add(country)
        
    all_country_list = list(countries)
    random_countries = random.sample(all_country_list, COUNTRIES_NUMBER)
         
    country_universities = {}
    
    with ThreadPoolExecutor(max_workers=MAX_THREAD_NUMBER) as executor:
        for country in random_countries:
            thread_results_2 = {executor.submit(fetch_univer_for_country, country)} #Utworzenie słownika
            
            for result_2 in thread_results_2:
                country, university_2 = result_2.result()
                country_universities[country] = university_2
    
    # for country in random_countries:
    #     country_url = f"{url}?country={country}"
    #     country_resp = requests.get(country_url)
    #     country_universities[country] = [uni_name['name'] for uni_name in country_resp.json()]

    country_count = 0
    all_uni_count = 0
    for country, universities in country_universities.items():
        each_uni_count = 0
        print(f"\nCountry: {country}")
        country_count += 1
        for university in universities:
            print(f"- {university}")
            each_uni_count +=1
            all_uni_count +=1
        print(f"Ilość uniwersytetów w: {country} - {each_uni_count}")
            
    print(f"\nCzas szukania:: {time.time() - start} sekund ") 
    print(f"Ilość państw: {country_count}")
    print(f"Ogolna ilość znalezionych uniwersytetów: {all_uni_count}")
    