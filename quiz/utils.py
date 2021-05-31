import requests


def get_json():

    with requests.Session() as s:
        try:
            data = s.get(
                "https://opentdb.com/api.php?amount=10&type=multiple").json()
            modified_data = data.get('results')
            print(modified_data)
            return modified_data
        except:
            print("error occured in fetching questions")
