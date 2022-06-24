import json

import scrapy
from scrapy.loader import ItemLoader
from jewellery_scrapy.items import BreuningItem
from itemloaders.processors import Join, MapCompose, TakeFirst

class BreuningSpider(scrapy.Spider):
    name = 'breuning'
    allowed_domains = ['shop.breuning.de']
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            "breuning.xlsx": {"format": "xlsx"},
            "breuning.csv": {"format": "csv"},
        }
    }

    def start_requests(self):
        urls = [
            # 'https://shop.breuning.de/en/12-solitaire',
            'https://shop.breuning.de/en/65-jewellery',
            'https://shop.breuning.de/en/151-chains',
            'https://shop.breuning.de/en/148-colormix',
            'https://shop.breuning.de/en/141-gifts',
            'https://shop.breuning.de/en/104-men',
            'https://shop.breuning.de/en/149-luxury',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_product_uri)

    def get_product_uri(self, response):
        product_list = response.css('div.products.grid.row a.thumbnail.product-thumbnail')
        for product in product_list:
            yield scrapy.Request(
                url=product.attrib['href'],
                callback=self.parse)

        next_page = response.css('div#js-product-list-bottom nav.pagination a.next').attrib['href']
        #next_page_url  = bottom_toolbar.css('li.item.pages-item-next')
        if next_page and next_page != response.url:
            yield scrapy.Request(
                url=next_page,
                callback=self.get_product_uri)


    def parse(self, response):
        item_loader = ItemLoader(item=BreuningItem(),
                                 default_output_processor=TakeFirst(),
                                 selector=response)

        item_loader.add_css('Product name', 'h1.h1')

        sku = json.loads(response.css('div#product-details').attrib['data-product'])[
            'reference'].split('-')[0]
        item_loader.add_value('SKU', sku)

        item_loader.add_css('Category', 'span[itemprop="name"]')

        item_loader.add_css('Subcategory', 'h1.h1')

        item_loader.add_css('Short Description', 'div#description')

        data_sheet_names = response.css('section.product-features dl').css('dt.name::text').getall()
        data_sheet_values = response.css('section.product-features dl').css(
            'dd.value::text').getall()
        long_description = []
        for name, value in zip(data_sheet_names, data_sheet_values):
            long_description.append(f'{name}: {value}')
        item_loader.add_value('Long Description', long_description)

        item_loader.add_css('Featured Image URL', 'div.wrapper-product-images img::attr(data-image-large-src)')

        item_loader.add_css('Images URLs', 'div.wrapper-product-images img::attr(data-image-large-src)')

        item_loader.add_value('Product URL', response.url)

        yield item_loader.load_item()
