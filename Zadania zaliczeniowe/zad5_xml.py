"""
Korzystając z danych XML:
https://www.w3schools.com/xml/cd_catalog.xml
zawierających kolekcję płyt CD, opracuj program, który wyświetli zestaw utworów i
wykonawców w postaci listy: [(wykonawca1, tytuł1), …].
"""

import xml.etree.ElementTree as ET
import requests

url = 'https://www.w3schools.com/xml/cd_catalog.xml'
resp = requests.get(url)

if resp.status_code != 200:
    print(f"Error: {resp.status_code}")

root = ET.fromstring(resp.content) # Parsowanie danych do XML z odpowiedzi

result = []
cds = root.findall('CD') # Znalezienie elementow potomnych w XML
for cd in cds:
    artist = cd.find('ARTIST').text # Znalezienie okreslonych elementow w XML 
    title = cd.find('TITLE').text
    result.append((artist, title))
print(result)