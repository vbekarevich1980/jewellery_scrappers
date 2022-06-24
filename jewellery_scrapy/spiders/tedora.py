import scrapy
from scrapy.loader import ItemLoader
from jewellery_scrapy.items import TedoraItem
from itemloaders.processors import Join, MapCompose, TakeFirst

class TedoraSpider(scrapy.Spider):
    name = 'tedora'
    allowed_domains = ['tedora.it']
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'FEEDS': {
            "tedora.xlsx": {"format": "xlsx"},
            "tedora.csv": {"format": "csv"},
        }
    }

    def start_requests(self):
        urls = [
            'https://www.tedora.it/en/shop/page/50/',
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.get_product_uri,
                meta={'proxy': None}
            )

    def get_product_uri(self, response):
        product_list = response.css('div.shop-container div.image-zoom-fade a::attr(href)').getall()
        for uri in product_list:
            yield scrapy.Request(
                url=uri,
                callback=self.parse)

        next_page = response.css('ul.page-numbers.nav-pagination.links.text-center a.next.page-number')
        #next_page = bottom_toolbar.css('li.item.pages-item-next')
        if next_page:
            yield scrapy.Request(
                url=next_page.attrib['href'],
                callback=self.get_product_uri)
        #
        # print(next_page)
        # ref = next_page.css('a.action.next').attrib['href']
        # print(ref)


    def parse(self, response):
        item_loader = ItemLoader(item=TedoraItem(),
                                 default_output_processor=TakeFirst(),
                                 selector=response)

        item_loader.add_css('Product name', 'h1.product-title.product_title.entry-title')


        item_loader.add_css('SKU', 'span.sku')


        item_loader.add_css('Category', 'nav.woocommerce-breadcrumb.breadcrumbs.uppercase a')

        item_loader.add_css('Subcategory', 'span.posted_in a')

        item_loader.add_css('Short Description', 'div.product-short-description')
        item_loader.add_css('Long Description', 'table.woocommerce-product-attributes.shop_attributes tr th')
        item_loader.add_css('Long Description', 'table.woocommerce-product-attributes.shop_attributes tr td')
        item_loader.add_css('Featured Image URL', '[data-large_image]::attr(data-large_image)')
        item_loader.add_css('Images URLs', '[data-large_image]::attr(data-large_image)')
        item_loader.add_value('Product URL', response.url)

        yield item_loader.load_item()
