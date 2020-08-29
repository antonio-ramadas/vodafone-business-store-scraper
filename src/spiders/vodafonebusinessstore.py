from urllib.parse import urlparse, parse_qs, urlencode

import logging
import scrapy

from src.domain.product import Product
from src.notifiers.notifierfactory import NotifierFactory


class VodafoneBusinessStore(scrapy.Spider):
    """
    Web spider that gets all the products present at the `Vodafone Business Store of music accessories
    <https://loja.negocios.vodafone.pt/loja/acessorios/catalogo?&categoria=Som&icmp=quicklinks-acessorios-som-3>`_.

    This spider goes through each page and for each product, it yields it with the necessary debugrmation to instantiate
    a :py:class:`src.domain.product.Product`.
    """

    __logger = logging.getLogger(__name__)

    name = 'vodafone_business_store'
    start_urls = ['https://loja.negocios.vodafone.pt/cs/Satellite?cid=1423846891501&pageId=1423846891522&pagename'
                  '=SiteEntryProductCatalog&query=c%3DOnlineStore_C%26cid%3D1423846891501%26d%3DTouch%26icmp%3Debu'
                  '-quicklinks-hploja-acessorios-3%26pageId%3D1423846891522%26pagename%3DOnlineB2B%252FOnlineStore_C'
                  '%252FCatalog%252FRenderCatalog%26trid%3D%26ns%3D1%26ajaxRequest%3D1%26null&site=OnlineB2B&filters'
                  '=%7B%7D&fd=date&ord=1&p=1']

    def next_page(self, current):
        """
        Advances a URL to the next page. This operation is performed by extracting the query parameters `p` from the URL
        and then increase its value by one.

        :param current: str representation of URL.
        :return: str representation of URL pointing to the next page.
        """
        current_url = urlparse(current)
        query = parse_qs(current_url.query)

        # Go to the next page
        query['p'] = [str(int(query['p'][0]) + 1)]

        VodafoneBusinessStore.__logger.debug('Created URL to next page %s', query['p'])

        next_url = current_url._replace(query=urlencode(query, doseq=True))
        return next_url.geturl()

    def is_last_page(self, response):
        """
        Checks if a given response represents a page that is the last one.

        :param response: argument of type :py:class:`scrapy.http.Response`
        :return: True if response represents the last page, False otherwise.
        """
        pages = response.css('.pagination li a')

        for i, page in enumerate(pages):
            if 'active' == page.attrib.get('class', None):
                if i == len(pages)-1:
                    VodafoneBusinessStore.__logger.debug('On the last page.')
                    return True

                VodafoneBusinessStore.__logger.debug('Not on the last page (%i out of %i).', i+1, len(pages))
                return False
        else:
            VodafoneBusinessStore.__logger.warning("Found no pagination! url='%s'", response.url)

        VodafoneBusinessStore.__logger.warning('Active page not found. Assuming it is the last.')

        return True

    def parse(self, response):
        """
        Parses a given web page and extracts all its products from all next pages starting on the given one.

        :param response: argument of type :py:class:`scrapy.http.Response`
        :return: Yields either an extracted :py:class:`src.domain.product.Product` or a :py:class:`scrapy.http.Request`
        """
        selectors = response.css('.cost')

        if len(selectors) == 0:
            VodafoneBusinessStore.__logger.warning("Found no products! url='%s'", response.url)
            NotifierFactory.get_notifier(self.settings).warning("Found no products! url='%s'" % response.url)

        URL_HOST = 'https://loja.negocios.vodafone.pt'

        for selector in selectors:
            url = selector.css('.productName > a')[0].root.attrib['href']

            if not url.startswith(URL_HOST):
                url = URL_HOST + url

            product = Product(
                name=selector.css('.productName > a')[0].root.text.strip(),
                price=selector.css('.piners > h3')[0].root.text.strip(),
                url=url)

            VodafoneBusinessStore.__logger.debug('Extracted new Product: %s', product)
            yield product

            if not self.is_last_page(response):
                VodafoneBusinessStore.__logger.debug("Not on the last page. Going to the next one. url='%s'",
                                                     response.url)
                yield scrapy.Request(self.next_page(response.url), self.parse)
            else:
                VodafoneBusinessStore.__logger.debug('On the last page. Not making further requests or extractions.')
