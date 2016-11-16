import logging

import scrapy

from sp_vereadores import utils


logger = logging.getLogger(__name__)


class SPVereadoresSpider(scrapy.Spider):

    name = 'spvereadores'

    def start_requests(self):

        for url in utils.vereadores_urls():

            logger.info('Starting request to the url {!r}'.format(url))

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        url = response.url

        logger.info('Starting parser to the url {!r}'.format(url))

        vereador_id = utils.extract_vereador_id(response.body)

        logger.info('Vereador id: {!r}'.format(vereador_id))

        return scrapy.Request(
            utils.generate_json_url(vereador_id),
            callback=utils.Vereador(url=url, id=vereador_id)
        )
