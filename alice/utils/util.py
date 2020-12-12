import urllib.request
import time
import hashlib
import os
from PIL import Image
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# <<<<<<< HEAD
# aliceHome = "../alice/metadata/"
aliceHome = "metadata/"
# =======
# aliceHome = "../alice/metadata/"
# aliceHome = "/metadata/"
# >>>>>>> 2aceb4204566e76706be2f9318f4958189a62fb9
# pokemon_name_list = "pokemon.dat"
# cachename= "cache_pokemon_names.txt"
fav_pokemon_name_list = aliceHome + "pokemon_fav.dat"
ignore_pokemon_name_list = aliceHome + "pokemon_ignore.dat"
# cachename= "cache_pokemon_names_url.txt"
# filename = "wordlist.txt"
cache_json = aliceHome + "json_pokemon.txt"
time_cache_filename = aliceHome + "switch_time.dat"

def load_mons_file(file):
    with open(file) as f:
        content = f.readlines()
    content = [x.strip().lower() for x in content]
    return content

# content = load_mons_file(pokemon_name_list)
# print("Pokemon in Ash's inventory: " + str(len(content)))


# print("Pokemon in Ash's favorites: " + str(len(fav_content)))

# def get_pokemon(poke_url):
#
#     url_temp = "https://www.google.com/searchbyimage?site=search&sa=X&image_url="+poke_url
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#         'From': 'giriprakash93@gmail.com'
#     }
#
#     response = requests.get(url_temp, headers=headers, allow_redirects=True)
#     # print( "Content_length: "+ str(len(response.text)))
#     # x=slice(150000,225000)
#     # strip_text = response.text[x]
#     strip_text = response.text.lower()
#
#     target = list()
#     # print("possible target found: ")
#     for mon in content:
#         if(mon in strip_text):
#             # print(mon)
#             # target.append("p!catch "+mon)
#             target.append(mon)
#     return target


# def save_cache(new_dict):
#     print("Saving pokemon data in cache")
#     dicts_from_file = load_dict_from_file()
#     dicts_from_file.update(new_dict)
#     save_dict_to_file(cachename, dicts_from_file)


# def save_pokemon_data(cachename, new_dict):
#     print("Saving pokemon data in cache")
#     dicts_from_file = {}
#
#     if not os.path.exists(cachename):
#         with open(cachename, 'w'): pass
#
#     with open(cachename,'r',encoding='utf-8') as inf:
#         for line in inf:
#             dicts_from_file.update(eval(line))
#     inf.close()
#
#     dicts_from_file.update(new_dict)
#     save_dict_to_file(cachename, dicts_from_file)


# def save_dict_to_file(cachename, dict):
#     f = open(cachename,'w',encoding='utf-8')
#     f.write(str(dict))
#     f.flush()
#     f.close()

# def load_dict_from_file():
#
#     dicts_from_file = {}
#
#     if not os.path.exists(cachename):
#         with open(cachename, 'w'): pass
#
#     with open(cachename,'r',encoding='utf-8') as inf:
#         for line in inf:
#             dicts_from_file.update(eval(line))
#     inf.close()
#     # for i in dicts_from_file:
#     #     val = str(dicts_from_file[i]).lower()
#     #     dicts_from_file[i] = val
#     # save_dict_to_file(cachename, dicts_from_file)
#     # print("Cached pokemon data: " + str(len(dicts_from_file)))
#     return dicts_from_file


# def get_pokedata_from_file(data):
#
#     dicts_from_file = {}
#
#     if not os.path.exists(data):
#         with open(data, 'w'): pass
#
#     with open(data, 'r', encoding='utf-8') as inf:
#         for line in inf:
#             dicts_from_file.update(eval(line))
#     inf.close()
#     return dicts_from_file

def get_fav_pokemon_list():
    fav_content = load_mons_file(fav_pokemon_name_list)
    return fav_content

def get_ignore_pokemon_list():
    fav_content = load_mons_file(ignore_pokemon_name_list)
    return fav_content

# def execute_spammer():
#     with open(filename) as f:
#         content = f.readlines()
#     content = [x.strip().lower() for x in content]
#     return content


def get_switch_time():

    try:
        with open(time_cache_filename) as f:
            timeInMillisStr = f.readline()
        timeInMillisStr = str(timeInMillisStr).strip()
        return float(timeInMillisStr)
    except FileNotFoundError:
        set_switch_time(time.time())
        return get_switch_time()
    # print(timeInMillisStr)

def set_switch_time(time):

    f = open(time_cache_filename,'w',encoding='utf-8')
    f.write(str(time))
    f.flush()
    f.close()


# def get_hash_from_url(url):
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
#
#     r = requests.get(url, headers = headers, allow_redirects=True)
#     r.raise_for_status()
#     m = hashlib.md5(Image.open(io.BytesIO(r.content)).tobytes())
#     return m.hexdigest()

def get_hash_from_url(url):
    filename = "temp.png"
    # urllib.request.urlretrieve(url, filename)

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')
    filename, headers = opener.retrieve(url, filename)
    f = Image.open(filename)
    f = f.convert('RGB')
    f = f.resize((150,150), Image.ANTIALIAS)
    f.save(filename, quality = 100)
    hash = hashlib.md5(Image.open(filename).tobytes())
    return (hash.hexdigest())

def get_cache():
    with open(cache_json, "r") as json_file:
        data = json.load(json_file)
        return data
