from api.tests.base import BaseApi


class TestApi(BaseApi):

    def test_get_search(self):
        answer = self.api_client.get_search('Alcatel', 'name')
        assert self.api_client.check_name(answer, 'Alcatel')
        assert self.api_client.check_sorted(answer)
