import json

import scrapy
from scrapy.loader import ItemLoader
from jewellery_scrapy.items import BoccadamoItem
from itemloaders.processors import Join, MapCompose, TakeFirst

class BoccadamoSpider(scrapy.Spider):
    name = 'boccadamo'
    allowed_domains = ['boccadamo.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            "boccadamo.xlsx": {"format": "xlsx"},
            "boccadamo.csv": {"format": "csv"},
        }
    }

    def start_requests(self):
        urls = [
            'https://www.boccadamo.com/eu_en/prodotti/man-bracelets?is_ajax=1&p=1&is_scroll=1',
            'https://www.boccadamo.com/eu_en/prodotti/mya-man-bracelets?is_ajax=1&p=1&is_scroll=1'
            #'https://www.boccadamo.com/eu_en/prodotti/mya-man-bracelets#page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_product_uri, meta={'playwright': True})

    def get_product_uri(self, response):
        product_list = response.css('div.category-products div.products a')
        for product in product_list:
            #print(product.attrib['href'])
            yield scrapy.Request(
                url=product.attrib['href'],
                callback=self.parse)

        try:
            next_page = response.css('div.pages a.next.i-next').attrib['href']
        except:
            next_page = False

        #current_page = int(response.css('div.pages li.current::text').get())
        #total_number_pages = int(len(response.css('div.pages li').getall())/2 - 1)
        #next_page = response.css('div.pages a.next.i-next').attrib['href'].split('=')[0] + '=' + str(current_page + 1)



        #print('next_page1', next_page1)
        #print('next_page', next_page)
        #print('current_page', current_page)
        #print('total_number_pages', total_number_pages)
        #print('url', response.url)

        #next_page_url  = bottom_toolbar.css('li.item.pages-item-next')
        if next_page:
            yield scrapy.Request(
                url=next_page + '&is_ajax=1',
                callback=self.get_product_uri,
                meta={'playwright': True}
            )


    def parse(self, response):
        item_loader = ItemLoader(item=BoccadamoItem(),
                                 default_output_processor=TakeFirst(),
                                 selector=response)

        item_loader.add_css('Product name', 'div.product-name')

        # sku = json.loads(response.css('div#product-details').attrib['data-product'])[
        #     'reference'].split('-')[0]
        item_loader.add_css('SKU', 'div.short-description div.std:nth-of-type(3)')

        item_loader.add_value('Category', 'PRODUCTS')

        item_loader.add_value('Subcategory', 'BRACELETS')

        item_loader.add_css('Short Description', 'div.short-description div.std')

        # data_sheet_names = response.css('section.product-features dl').css('dt.name::text').getall()
        # data_sheet_values = response.css('section.product-features dl').css(
        #     'dd.value::text').getall()
        # long_description = []
        # for name, value in zip(data_sheet_names, data_sheet_values):
        #     long_description.append(f'{name}: {value}')
        # item_loader.add_value('Long Description', long_description)
        item_loader.add_css('Long Description',
                            'div.product-shop-inner div:nth-of-type(7)')

        item_loader.add_css('Featured Image URL', 'a.MagicZoom::attr(href)')

        item_loader.add_css('Images URLs', 'div.MagicToolboxSelectorsContainer img::attr(src)')
        
        item_loader.add_value('Product URL', response.url)

        yield item_loader.load_item()
