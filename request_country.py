import requests
import json
import csv

file_json = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\country_neighbours.json'
file_csv = '/Users\jeand\OneDrive\Documentos\Programming\Python\Insa\countries.csv'


def request_neighbours(country, username):
    url = 'http://api.geonames.org/neighboursJSON?'
    neighbours = []
    url = url + f'country={country}&username={username}'
    sent_request = requests.get(url)
    print(sent_request)
    if sent_request.status_code == 200:
        response = sent_request.json()
        print(response)
        neighbours_list = response['geonames']
        for i in neighbours_list:
            country_name = i['countryName']
            country_code = i['countryCode']
            neighbours.append((country_name, country_code))
    else: 
        neighbours.append(sent_request.status_code)
    return neighbours


def load_data(file):
        with open(file, newline = "") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            data = {}
            for country, country_code in reader:
                if country_code not in data:
                    data[country_code] = [country]
                else:
                    data[country_code].append(country)
        return data


data = load_data(file_csv)


new_data = {}

for i in data:
    m = i.lower()
    print(str(m))
    try:
        neighbours = request_neighbours(str(m), username = 'romi45')
        new_data[str(m)] = neighbours
    except:
        print('API error')


print('')
print(new_data)

with open(file_json, 'w') as country_neighbours:
    json.dump(new_data, country_neighbours)



