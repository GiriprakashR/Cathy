import requests
import os

filename = "metadata/pokemon.dat"
cachename= "metadata/cache_pokemon_names.txt"
cachename= "cache_pokemon_names_url.txt"
with open(filename) as f:
    content = f.readlines()
content = [x.strip().lower() for x in content]
print("Pokemons in Ash's inventory: " + str(len(content)))
def get_pokemon(poke_url):

    url_temp = "https://www.google.com/searchbyimage?site=search&sa=X&image_url="+poke_url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'From': 'giriprakash93@gmail.com'
    }

    response = requests.get(url_temp, headers=headers, allow_redirects=True)
    # print( "Content_length: "+ str(len(response.text)))
    # x=slice(150000,225000)
    # strip_text = response.text[x]
    strip_text = response.text

    target = list()
    # print("possible target found: ")
    for mon in content:
        if(mon in strip_text):
            # print(mon)
            target.append("p!catch "+mon)
            target.append(mon)
    return target


def save_cache(new_dict):
    print("Saving pokemon data in cache")
    dicts_from_file = load_dict_from_file()
    dicts_from_file.update(new_dict)
    save_dict_to_file(cachename, dicts_from_file)


def save_pokemon_data(cachename, new_dict):
    print("Saving pokemon data in cache")
    dicts_from_file = {}

    if not os.path.exists(cachename):
        with open(cachename, 'w'): pass

    with open(cachename,'r',encoding='utf-8') as inf:
        for line in inf:
            dicts_from_file.update(eval(line))
    inf.close()

    dicts_from_file.update(new_dict)
    save_dict_to_file(cachename, dicts_from_file)


def save_dict_to_file(cachename, dict):
    f = open(cachename,'w',encoding='utf-8')
    f.write(str(dict))
    f.flush()
    f.close()

def load_dict_from_file():

    dicts_from_file = {}

    if not os.path.exists(cachename):
        with open(cachename, 'w'): pass

    with open(cachename,'r',encoding='utf-8') as inf:
        for line in inf:
            dicts_from_file.update(eval(line))
    inf.close()
    return dicts_from_file

def get_pokedata_from_file(data):

    dicts_from_file = {}

    if not os.path.exists(data):
        with open(data, 'w'): pass

    with open(data, 'r', encoding='utf-8') as inf:
        for line in inf:
            dicts_from_file.update(eval(line))
    inf.close()
    return dicts_from_file
