import scrapy
from scrapy.loader import ItemLoader
from jewellery_scrapy.items import BroswayTedoraItem
from itemloaders.processors import Join, MapCompose, TakeFirst

class BroswaySpider(scrapy.Spider):
    name = 'brosway'
    allowed_domains = ['brosway.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            "brosway.xlsx": {"format": "xlsx"},
            "brosway.csv": {"format": "csv"},
        }
    }

    def start_requests(self):
        urls = [
            'https://www.brosway.com/en/necklaces',
            'https://www.brosway.com/en/bracelets',
            'https://www.brosway.com/en/earrings',
            'https://www.brosway.com/en/rings',
            'https://www.brosway.com/en/beads',
            'https://www.brosway.com/en/watches',
            'https://www.brosway.com/en/anklets',
            'https://www.brosway.com/en/accessories',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_product_uri)

    def get_product_uri(self, response):
        product_list = response.css('li.item.product.product-item')
        for product in product_list:
            yield scrapy.Request(
                url=product.css(
                    'a.product.photo.product-item-photo'
                ).attrib['href'],
                callback=self.parse)

        bottom_toolbar = response.css('div.toolbar-wrapper-bottom')
        next_page = bottom_toolbar.css('li.item.pages-item-next')
        if next_page:
            yield scrapy.Request(
                url=next_page.css('a.action.next').attrib['href'],
                callback=self.get_product_uri)
        #
        # print(next_page)
        # ref = next_page.css('a.action.next').attrib['href']
        # print(ref)


    def parse(self, response):
        item_loader = ItemLoader(item=BroswayTedoraItem(),
                                 default_output_processor=TakeFirst(),
                                 selector=response)

        item_loader.add_css('Product name', 'span.base')


        item_loader.add_css('SKU', 'div.product.attribute.sku div.value')


        item_loader.add_css('Category', 'div.product-info-topbar')

        item_loader.add_value('Subcategory', '')

        item_loader.add_css('Short Description', 'div.product-section.description-section.accordion-section div.accordion-content p')
        #item_loader.add_css('Long Description', 'div.product-section.additional-section.accordion-section')
        item_loader.add_css('Long Description', 'div.product-section.additional-section.accordion-section div.accordion-content div.more-info-data')
        item_loader.add_css('Featured Image URL', 'div#product-gallery>div.images-container_child.product-gallery-image a::attr(href)')
        item_loader.add_css('Images URLs', 'div.images-container_child.product-gallery-image a::attr(href)')
        item_loader.add_value('Product URL', response.url)

        yield item_loader.load_item()
