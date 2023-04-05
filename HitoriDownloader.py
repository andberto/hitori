'''
HITORI GAME
Parma, 11/12/19
Andrea Bertogalli

Classe inizialmente usata per velocizzare il testing
si è rivelata una funzionalità interessante
'''

from urllib.request import urlopen, URLError
from socket import timeout
from re import findall,sub
from random import randint, choice
from  os import listdir

DOMAIN = "http://www.menneske.no/hitori/"
PARAMS = "/eng/utskrift.html?number="
puzzle_number = "offline"

def download_puzzle(side: int):
    global puzzle_number
    puzzle_number = str(randint(1,999))
    url = DOMAIN + str(side) + "x" + str(side) + PARAMS + puzzle_number  #compongo url dimensione + random puzzle
    shaped = []
    with urlopen(url) as response: #dato che non vi erano db disponibili: regex per estrarre i dati dalla risposta della richiesta
        response_content = response.read()
        matches = findall(">[1-9]|1[0-7]</td>", str(response_content))
        matches = sub(r"\D","","".join(matches))
        shaped = [list(matches[i:i+side]) for i in range(0, len(matches), side)]
    return shaped #formatto come matrice

def is_reachable():
    try:
        urlopen(DOMAIN, timeout=1)
        return True
    except:
        return False

def get_offline_puzzle(dir):
    global puzzle_number
    puzzle_number = "offline"
    return choice(listdir(dir))

def puzzle_info():
    global puzzle_number
    return puzzle_number

