import requests


if __name__ == '__main__':

    # response = requests.post('http://127.0.0.1:5000/advertisement/',
    #                          json={
    #                              'title': 'Приветствие 1',
    #                              'description': 'Привет, мир!',
    #                              'owner': 'Евгений',
    #                              'email': 'e-vareniev@yandex.ru',
    #                          }
    #                          )

    # response = requests.get('http://127.0.0.1:5000/advertisement/1/')
    # response = requests.delete('http://127.0.0.1:5000/advertisement/4/')
    #

    response = requests.post('http://127.0.0.1:5000/spam/')
    # response = requests.get('http://127.0.0.1:5000/spam/fd3197cf-4920-4f7a-a5f0-206738050612')
    print(response.status_code)
    print(response.text)
