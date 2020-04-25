from urllib.parse import urlparse, parse_qs, urlencode

import scrapy

from src.domain.product import Product


class VodafoneBusinessStoreSpider(scrapy.Spider):
    name = 'vodafone_business_store_spider'
    start_urls = ['https://loja.negocios.vodafone.pt/cs/Satellite?cid=1423846891501&pageId=1423846891522&pagename=SiteEntryProductCatalog&query=c%3DOnlineStore_C%26categoria%3DSom%26cid%3D1423846891501%26d%3DTouch%26icmp%3Dquicklinks-acessorios-som-3%26pageId%3D1423846891522%26pagename%3DOnlineB2B%252FOnlineStore_C%252FCatalog%252FRenderCatalog%26trid%3D%26ns%3D1%26ajaxRequest%3D1%26null&site=OnlineB2B&tid=1423845689128&hm=1313&trid=&ajaxRequest=1&filters=%7B%22CATGR-CL-OR-filter%22%3A%5B%221423967921535%22%5D%7D&fd=date&ord=1&p=0']

    def next_page(self, current):
        current_url = urlparse(current)
        query = parse_qs(current_url.query)

        # Go to the next page
        query['p'] = [str(int(query['p'][0]) + 1)]

        next_url = current_url._replace(query=urlencode(query, doseq=True))
        return next_url.geturl()

    def is_last_page(self, response):
        pages = response.css('.pagination li a')

        for i, page in enumerate(pages):
            if 'active' == page.attrib.get('class', None):
                return i == len(pages)-1

        return True

    def parse(self, response):
        for selector in response.css('.cost'):
            yield Product(
                name=selector.css('.productName > a')[0].root.text.strip(),
                price=selector.css('.piners > h3')[0].root.text.strip(),
                url=selector.css('.productName > a')[0].root.attrib['href'])

            if not self.is_last_page(response):
                yield scrapy.Request(self.next_page(response.url), self.parse)
