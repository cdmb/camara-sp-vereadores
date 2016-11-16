import logging

import scrapy

from sp_vereadores import utils


logger = logging.getLogger(__name__)


class SPVereadoresSpider(scrapy.Spider):

    name = 'spvereadores'

    def start_requests(self):

        for url in utils.councillors_urls():

            logger.info('Starting request to the url {!r}'.format(url))

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        url = response.url

        logger.info('Starting parser to the url {!r}'.format(url))

        councillor_id = utils.extract_councillor_id(response.body)

        logger.info('Councillor id: {!r}'.format(councillor_id))

        return scrapy.Request(
            utils.generate_json_url(councillor_id),
            callback=utils.Councillor(url=url, id=councillor_id)
        )
