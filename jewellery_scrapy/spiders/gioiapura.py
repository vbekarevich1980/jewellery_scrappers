import scrapy
from scrapy.loader import ItemLoader
from jewellery_scrapy.items import GioiapuraItem
from itemloaders.processors import Join, MapCompose, TakeFirst

class GioiapuraSpider(scrapy.Spider):
    name = 'gioiapura'
    allowed_domains = ['gioiapura.it']
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            "gioiapura.xlsx": {"format": "xlsx"},
            "gioiapura.csv": {"format": "csv"},
        }
    }

    def start_requests(self):
        urls = [
            'https://www.gioiapura.it/en/disney-B90.htm',
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.get_product_uri,
                meta={'proxy': None}
            )

    def get_product_uri(self, response):
        product_list = response.css('div.products-list__item a.prodotto-box__image::attr(href)').getall()

        for uri in product_list:
            yield scrapy.Request(
                url='https://www.gioiapura.it' + uri,
                callback=self.parse)

        next_page = response.css('nav.nav--pagination.nav--pagination-next a.button--bold.nav__next')
        if next_page:
            yield scrapy.Request(
                url=next_page.attrib['href'],
                callback=self.get_product_uri)



    def parse(self, response):
        item_loader = ItemLoader(item=GioiapuraItem(),
                                 default_output_processor=TakeFirst(),
                                 selector=response)

        item_loader.add_css('Product name', 'h1.prodotto__nome')


        item_loader.add_css('SKU', 'div.prodotto__codice')


        item_loader.add_css('Category', 'div.prodotto__descrizione-content.prodotto__tab-content')

        item_loader.add_css('Subcategory', 'div.prodotto__descrizione-content.prodotto__tab-content')

        item_loader.add_css('Short Description', 'div.prodotto__descrizione-content.prodotto__tab-content')
        item_loader.add_css('Long Description', 'div.prodotto__descrizione-content.prodotto__tab-content')
        #item_loader.add_css('Long Description', 'div#caratteristicheBox div.prodotto__descrizione-content.prodotto__descrizione-content--caratteristiche prodotto__tab-content div')
        item_loader.add_css('Featured Image URL', 'div.prodotto__immagini-pager-wrap a img::attr(data-src)')
        item_loader.add_css('Images URLs', 'div.prodotto__immagini-pager-wrap a img::attr(data-src)')
        #item_loader.add_css('Images URLs', 'div#prodotto__immagini-pager-wrap div.owl-item.active img::attr(src)')
        item_loader.add_value('Product URL', response.url)

        yield item_loader.load_item()
