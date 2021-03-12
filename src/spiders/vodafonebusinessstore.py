import json

import logging
import scrapy

from src.domain.product import Product
from src.notifiers.notifierfactory import NotifierFactory


class VodafoneBusinessStore(scrapy.Spider):
    """
    Web spider that gets all the products present at the `Vodafone Business Store of accessories
    <https://www.vodafone.pt/loja/acessorios.html?i_id=ver-todos-acessorios-loja-business&segment=business>`_.

    This spider goes through each page and for each product, it yields it with the necessary information to instantiate
    a :py:class:`src.domain.product.Product`.
    """

    __logger = logging.getLogger(__name__)

    name = 'vodafone_business_store'
    start_urls = ['https://www.vodafone.pt/bin/mvc.do/eshop/catalogs/catalog?collectionPath=&catalogType=Accessory&'
                  'pageModel=%2Floja%2Facessorios.html&filterCatalog=true']

    def parse(self, response):
        """
        Parses a given json response and yields all valid :py:class:`src.domain.product.Product` it can find.

        :param response: argument of type :py:class:`scrapy.http.Response`
        """
        products = json.loads(response.text)['products']

        if not products:
            VodafoneBusinessStore.__logger.warning("Found no products! url='%s'", response.url)
            NotifierFactory.get_notifier(self.settings).warning("Found no products! url='%s'" % response.url)

        URL_HOST = 'https://loja.negocios.vodafone.pt'

        counter = 0

        for raw_product in products:
            for variant in raw_product['variants']:
                pvp = variant['priceCondition']['PVP']
                if not pvp:
                    VodafoneBusinessStore.__logger.info(
                        "Ignoring product because it is only sold in-store. product='%s'", variant)
                    continue

                product = Product(
                    name=variant['name'],
                    price=pvp[0]['price'],
                    url=URL_HOST + variant['pageLink']
                )

                counter += 1
                VodafoneBusinessStore.__logger.debug("Extracted new Product: %s", product)
                yield product

        VodafoneBusinessStore.__logger.info("Finished extraction. Processed %d products.", counter)
