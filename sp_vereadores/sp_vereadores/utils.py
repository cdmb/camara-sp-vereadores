import json
import logging

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

BASE_URL = 'http://www.camara.sp.gov.br/vereadores/'
COUNCILLOR_URL_CLASS = '.vereador-name'

COUNCILLOR_ID_BASE_CLASS = '.vereador-entry'
COUNCILLOR_ID_KEY = 'data-id'

COUNCILLOR_JSON_DATA_URL = 'http://www1.camara.sp.gov.br/vereador_json.asp?vereador={}'  # noqa

COUNCILLOR_DATA_DIR = '../data'


def councillors_urls():

    logger.info('Acessing the base url: {!r}'.format(BASE_URL))

    response = requests.get(BASE_URL)

    if not response.status_code == 200:

        logger.warning('Some problem with the base url. Response status_code:'
                       ' {}'.format(response.status_code))

        raise ValueError(
            'Error acessing the url {!r}. Maybe the site is down'.format(
                BASE_URL
            )
        )

    soup = BeautifulSoup(response.text).select(COUNCILLOR_URL_CLASS)

    for item in soup:
        logger.info('Next url: {}'.format(item))
        yield item.a.get('href')


def extract_councillor_id(html):

    soup = BeautifulSoup(html)

    data = soup.select_one(COUNCILLOR_ID_BASE_CLASS)

    councillor_id = data.get(COUNCILLOR_ID_KEY)

    return councillor_id


def generate_json_url(councillor_id):
    return COUNCILLOR_JSON_DATA_URL.format(councillor_id)


class Councillor:

    def __init__(self, url, id):

        self._url = url,
        self._id = id
        self._raw_json = None

    def __call__(self, response):

        logger.info(response)

        self._raw_json = json.loads(response.text)

        self.write_data_as_json()

    @property
    def name(self):
        return self._raw_json['nome'].replace(' ', '-')

    @property
    def json(self):
        return {
            'url': self._url,
            'id': self._id,
            'rawData': self._raw_json
        }

    def write_data_as_json(self):

        with open('{}/{}.json'.format(COUNCILLOR_DATA_DIR, self.name), 'w') as f: # noqa
            f.write(json.dumps(self.json))
