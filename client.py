import requests


# response = requests.get('http://127.0.0.1:5000/advertisement/1/')


# response = requests.post('http://127.0.0.1:5000/advertisement/',
#                          json={
#                              'title': 'Приветствие 4',
#                              'description': 'Привет, мир!',
#                              'owner': 'Евгений',
#                          }
#                          )

response = requests.delete('http://127.0.0.1:5000/advertisement/4/')

print(response.status_code)
print(response.text)