import operator
import requests
from api.model import JsTestTask


class ResponseStatusCodeException(Exception):
    pass

class ApiClient:

    def __init__(self):
        self.session = requests.Session()

    def _request(self, method, url, headers=None, data=None, expected_status=200, params=None):
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')
        return response

    def get_search(self, name, sort_by):
        url = f'https://www.lenvendo.ru/api/js-test-task/?search={name}&sort_field={sort_by}'
        response = self._request(method='GET', url=url, expected_status=200).json()
        products = []
        for item in response['products']:
            products.append(JsTestTask(item['name'], item['image'], item['price']))
        return products

    def check_name(self, answer, name):
        return all([True if name in item.name else False for item in answer])

    def check_sorted(self, products):
        return True if products == sorted(products, key=operator.attrgetter('name')) else False



