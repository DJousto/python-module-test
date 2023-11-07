import json
import requests
import re

def getPackaging(value, country_code) :
    country_variations = {
    'pl': {  # Poland
        'Packagings': ['sztuka', 'szt.', 'szt', 'kg', 'g', 'gr' , 'mg', 'l', 'ltr' , 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[s][z][t]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l][t][r]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[s][z][t]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l][t][r]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[s][z][t]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l][t][r]|\d+[,]\d+\s*[l]'
    },
    'fr': {  # France
        'Packagings': ['pcs', 'kg', 'g', 'gr' , 'mg', 'l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[p][c][s]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[s][t][k]|\d+[.]\d+\s*[s][t][ü][c][k]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]'
    },
    'de': {  # Germany
        'Packagings': ['stück', 'stk.', 'stk', 'kg', 'g', 'gr' , 'mg', 'l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[s][t][k]|\d+\s*[s][t][ü][c][k]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[s][t][k]|\d+[.]\d+\s*[s][t][ü][c][k]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[s][t][k]|\d+[,]\d+\s*[s][t][ü][c][k]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'es': {  # Spain
        'Packagings': ['pcs', 'unidad', 'u','kg', 'g', 'gr' , 'mg','l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[s][t][k]|\d+\s*[u][n][i][d][a][d]|\d+\s*[u]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[s][t][k]|\d+[.]\d+\s*[u][n][i][d][a][d]|\d+[.]\d+\s*[u]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[s][t][k]|\d+[,]\d+\s*[u][n][i][d][a][d]|\d+[,]\d+\s*[u]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'it': {  # Italy
        'Pieces': ['pcs', 'pezzi', 'pz','kg', 'g', 'gr' , 'mg', 'l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[p][e][z][z][i]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[p][e][z][z][i]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[p][e][z][z][i]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'uk': {  # United Kingdom
        'Packagings': ['pcs', 'kg', 'g', 'gr' , 'mg', 'l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'us': {  # USA
        'Packagings': ['pcs','lb', 'oz', 'gal', 'qt', 'pt', 'cup', 'fl oz', 'g' , 'gr' ,'mg', 'l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[p][c][s]|\d+\s*[l][b]|\d+\s*[o][z]|\d+\s*[g][a][l]|\d+\s*[q][t]|\d+\s*[p][t]|\d+\s*[c][u][p]|\d+\s*[f][l]\s[o][z]|\d+\s*[m][l]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[l][b]|\d+[.]\d+\s*[o][z]|\d+[.]\d+\s*[g][a][l]|\d+[.]\d+\s*[q][t]|\d+[.]\d+\s*[p][t]|\d+[.]\d+\s*[c][u][p]|\d+[.]\d+\s*[f][l]\s[o][z]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[l][b]|\d+[,]\d+\s*[o][z]|\d+[,]\d+\s*[g][a][l]|\d+[,]\d+\s*[q][t]|\d+[,]\d+\s*[p][t]|\d+[,]\d+\s*[c][u][p]|\d+[,]\d+\s*[f][l]\s[o][z]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'ua': {  # Ukraine
        'Packagings': ['штука', 'шт.', 'шт', 'кг', 'г', 'гр', 'мг', 'л', 'мл'],
        'Regex_space' : '\d+\s*[ш][т][у][к][а]|\d+\s*[ш][т]|\d+\s*[к][г]|\d+\s*[г]|\d+\s*[г][р]|\d+\s*[м][г]|\d+\s*[л]|\d+\s*[м][л]',
        'Regex_dot' : '\d+[.]\d+\s*[ш][т][у][к][а]|\d+[.]\d+\s*[ш][т]|\d+[.]\d+\s*[к][г]|\d+[.]\d+\s*[г]|\d+[.]\d+\s*[г][р]|\d+[.]\d+\s*[м][г]|\d+[.]\d+\s*[л]|\d+[.]\d+\s*[м][л]',
        'Regex_comma' : '\d+[,]\d+\s*[ш][т][у][к][а]|\d+[,]\d+\s*[ш][т]|\d+[,]\d+\s*[к][г]|\d+[,]\d+\s*[г]|\d+[,]\d+\s*[г][р]|\d+[,]\d+\s*[м][г]|\d+[,]\d+\s*[л]|\d+[,]\d+\s*[м][л]'
    },
    'ru': {  # Russia
        'Packagings': ['штука', 'шт.', 'шт','кг', 'г', 'гр', 'мг','л', 'мл'],
        'Regex_space' : '\d+\s*[ш][т][у][к][а]|\d+\s*[ш][т]|\d+\s*[к][г]|\d+\s*[г]|\d+\s*[г][р]|\d+\s*[м][г]|\d+\s*[л]|\d+\s*[м][л]',
        'Regex_dot' : '\d+[.]\d+\s*[ш][т][у][к][а]|\d+[.]\d+\s*[ш][т]|\d+[.]\d+\s*[к][г]|\d+[.]\d+\s*[г]|\d+[.]\d+\s*[г][р]|\d+[.]\d+\s*[м][г]|\d+[.]\d+\s*[л]|\d+[.]\d+\s*[м][л]',
        'Regex_comma' : '\d+[,]\d+\s*[ш][т][у][к][а]|\d+[,]\d+\s*[ш][т]|\d+[,]\d+\s*[к][г]|\d+[,]\d+\s*[г]|\d+[,]\d+\s*[г][р]|\d+[,]\d+\s*[м][г]|\d+[,]\d+\s*[л]|\d+[,]\d+\s*[м][л]'
    },
    'ro': {  # Romania
        'Packagings': ['bucată', 'buc.', 'buc', 'kg' , 'gr', 'g', 'mg','l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[b][u][c]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[b][u][c]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[b][u][c]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'eg': {  # Egypt
        'Packagings': ['قطعة', 'قطع','كغ', 'جم', 'ملغ','لتر', 'مل']
    },
    'no': {  # Norway
        'Packagings': ['stykke', 'stk.', 'stk', 'kg', 'g', 'gr', 'mg','l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[s][t][k]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[s][t][k]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[s][t][k]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    },
    'in': {  # India
        'Packagings': ['pcs', 'kg', 'g', 'gr', 'mg','l', 'ml'],
        'Regex_space' : '\d+\s*[k][g]|\d+\s*[g][r]|\d+\s*[p][c][s]|\d+\s*[m][l]|\d+\s*[m][g]|\d+\s*[g]|\d+\s*[l]',
        'Regex_dot' : '\d+[.]\d+\s*[k][g]|\d+[.]\d+\s*[g][r]|\d+[.]\d+\s*[p][c][s]|\d+[.]\d+\s*[m][l]|\d+[.]\d+\s*[m][g]|\d+[.]\d+\s*[g]|\d+[.]\d+\s*[l]',
        'Regex_comma' : '\d+[,]\d+\s*[k][g]|\d+[,]\d+\s*[g][r]|\d+[,]\d+\s*[p][c][s]|\d+[,]\d+\s*[m][l]|\d+[,]\d+\s*[m][g]|\d+[,]\d+\s*[g]|\d+[,]\d+\s*[l]'
    }
    }
    if '.' in value :
        regex_dot = re.findall(country_variations[country_code]['Regex_dot'], value)
        if regex_dot :
           return regex_dot[0]
    if ',' in value :
        regex_comma = re.findall(country_variations[country_code]['Regex_comma'], value)
        if regex_comma :
           return regex_comma[0]
    regex_space = re.findall(country_variations[country_code]['Regex_space'], value)
    if regex_space :
       return regex_space[0]
    return ''

def getCurrencyIso(country_code) :
    currency = 'None'
    currency_dict = {"ke": "KES","ua": "UAH","pl": "PLN","eg": "EGP","no": "NOK","ro": "RON","fr": "EUR","ru": "RUB","us": "USD","in": "INR","cz": "CZK","af": "AFN","la": "LAK","al": "ALL","lv": "LVL","dz": "DZD","lb": "LBP","ad": "EUR","ls": "LSL","ao": "AOA","lr": "LRD","ag": "XCD","ly": "LYD","ar": "ARS","li": "CHF","am": "AMD","lt": "EUR","au": "AUD","lu": "EUR","at": "EUR","mk": "MKD","az": "AZN","mg": "MGA","bs": "BSD","mw": "MWK","bh": "BHD","my": "MYR","bd": "BDT","mv": "MVR","bb": "BBD","ml": "XOF","by": "BYN","mt": "EUR","be": "EUR","mh": "USD","bz": "BZD","mr": "MRU","bj": "XOF","mu": "MUR","bt": "BTN","mx": "MXN","bo": "BOB","fm": "USD","ba": "BAM","md": "MDL","bw": "BWP","mc": "EUR","br": "BRL","mn": "MNT","bn": "BND","ma": "MAD","bg": "BGN","mz": "MZN","bf": "XOF","mm": "MMK","bi": "BIF","na": "NAD","kh": "KHR","nr": "AUD","cm": "XAF","np": "NPR","ca": "CAD","nl": "EUR","cv": "CVE","nz": "NZD","cf": "XAF","ni": "NIO","td": "XAF","ne": "XOF","cl": "CLP","ng": "NGN","cn": "CNY","no": "NOK","co": "COP","om": "OMR","km": "KMF","pk": "PKR","cd": "CDF","pw": "USD","cg": "XAF","pa": "PAB","cr": "CRC","pg": "PGK","ci": "XOF","py": "PYG","hr": "HRK","pe": "PEN","cu": "CUP","ph": "PHP","cy": "EUR","pl": "PLN","cz": "CZK","pt": "EUR","dk": "DKK","qa": "QAR","dj": "DJF","pr": "USD","dm": "XCD","ro": "RON","do": "DOP","ru": "RUB","tl": "USD","rw": "RWF","ec": "USD","kn": "XCD","sv": "USD","lc": "XCD","gq": "XAF","vc": "XCD","er": "ERN","ws": "WST","ee": "EUR","sm": "EUR","et": "ETB","st": "STN","fj": "FJD","sa": "SAR","ga": "XAF","sn": "XOF","gm": "GMD","rs": "RSD","ge": "GEL","sc": "SCR","gh": "GHS","sl": "SLL","gr": "EUR","sb": "SBD","gd": "XCD","so": "SOS","gl": "DKK","za": "ZAR","gt": "GTQ","es": "EUR","gn": "GNF","lk": "LKR","gw": "XOF","sd": "SDG","gy": "GYD","sr": "SRD","ht": "HTG","sz": "SZL","hn": "HNL","se": "SEK","hk": "HKD","ch": "CHF","hu": "HUF","sy": "SYP","is": "ISK","tj": "TJS","tz": "TZS","id": "IDR","tw": "TWD","ir": "IRR","th": "THB","ie": "EUR","tg": "XOF","il": "ILS","to": "TOP","it": "EUR","tt": "TTD","jm": "JMD","tn": "TND","jp": "JPY","tr": "TRY","jo": "JOD","tm": "TMT","kz": "KZT","tv": "TVD","ug": "UGX","ae": "AED","gb": "GBP","kw": "KWD","us": "USD","kg": "KGS","uy": "UYU"}
    try:
        currency = currency_dict[country_code]
    except :
        raise Exception(f'Currency code not found for: {country_code}')
    return currency

def getUnit(unit_string, lang='eu', regex = True) :
    value = unit_string
    if lang == 'cyrillic' :
       unit_dict = ["Г","г","КГ","кг","Л","л","МЛ","мл",'мг','МГ','Мг','шт','Шт']
       if regex == True :
          value = re.sub('[^a-zA-Z\u0400-\u04FF]+', '', unit_string).strip() # take only cyrillic leters from string 
    if lang == 'eu' :
       unit_dict = ["G","g","KG","Kg","kg","L","l","M","P","ML","Ml","ml",'MG','Mg','mg','Pcs','PCS','SZT','Szt','szt']
       if regex == True :
          value = re.sub('[^a-zA-Z]+', '', unit_string).strip() # take only leters from string 
    if regex == False :
       for v in unit_dict : 
           if v in value :
              print('Unit is : ' + v)
              return v
    if value in unit_dict:
       for v in unit_dict : 
           if v == value :
              print('Unit is : ' + v)
              return v
    print('Unit not found: ' + unit_string)
    return None

def webmonitoring_api_request(website_id, country_prefix, validation = False, isMatched = False, auth_data) :
    headers = {'Content-Type': 'application/json'}
    AUTH_URL = 'https://auth-api.graphee.io/oauth/token'
    response = requests.post(AUTH_URL, headers=headers, data=auth_data)
    try:
        access_token = response.json()['access_token']
    except:
        raise Exception("%ERROR% - webmonitoring-api Authentication error")
    headers = {'Authorization': 'Bearer ' + access_token}
    parameters = {"country" : country_prefix.lower().strip(),"is_downloaded" : False, "page" : "0"}
    response = requests.get('https://webmonitoring-api.graphee.io/websites', headers = headers,  params = parameters)
    if response :
       resp_json = json.loads(response.text)['data']
       for j in resp_json :
           if j["id"] == website_id :
               if isMatched == False :
                   response = requests.get("https://webmonitoring-api.graphee.io/customers/{customerId}/websites/{websiteId}/urls?country={countryISO}".format(customerId = "2", websiteId = j["id"], countryISO = j["country"]["ISO"]), headers = headers)
               else :
                   response = requests.get("https://webmonitoring-api.graphee.io/customers/{customerId}/websites/{websiteId}/urls?country={countryISO}&hasMatch=true".format(customerId = "2", websiteId = j["id"], countryISO = j["country"]["ISO"]), headers = headers)
               if response :
                   return [x['value'] for x in response.json()['data'] if (not(validation) or x['isValid']) ]
               else:
                   raise Exception('%ERROR% - https://webmonitoring-api.graphee.io/customers response error: ' + response.text)
    else :
        raise Exception('%ERROR% - https://webmonitoring-api.graphee.io/websites response error: ' + response.text)



def get_price(price_value: str):
    # check if a given value is a str
    if not price_value:
        raise Exception('No value given')
    if not isinstance(price_value, str):
        raise Exception(f'Expected str, got: {type(price_value)}')
    # call a needed method
    if ',' in price_value and '.' in price_value:
        return round(Price(price_value).comma_point_price(), 2)
    elif ',' in price_value:
        return round(Price(price_value).comma_price(), 2)
    elif '.' in price_value:
        return round(Price(price_value).point_price(), 2)
    else:
        return round(Price(price_value).simple_price(), 2)