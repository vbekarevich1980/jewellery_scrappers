# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags

class BroswayTedoraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __init__(self):
        super().__init__()
        self.fields['Product name'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )
        self.fields['SKU'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )
        self.fields['Category'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=TakeFirst()
        )
        self.fields['Subcategory'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )
        self.fields['Short Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags), output_processor=Join(' ')) # Need to fix to have whitespaces and remove 'Description' word
        self.fields['Long Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: ': '.join(x.split(':'))), output_processor=Join(', '))
        self.fields['Featured Image URL'] = scrapy.Field(output_processor=TakeFirst()

        )
        self.fields['Images URLs'] = scrapy.Field(output_processor=Join(', ')

        )
        self.fields['Product URL'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )


def long_description(description_elements):

    index = len(description_elements) / 2
    list_label = [f"{element.strip()}:" for num, element in enumerate(description_elements) if num < index]
    list_value = [f"{element.strip()}" for num, element in enumerate(description_elements) if num >= index]
    #list_value = [f"{element.strip()}:" if num < index else f"{element.strip}," for num, element in enumerate(description_elements)]
    list  = [f"{label} {value}" for label, value in zip(list_label, list_value)]
    return '; '.join(list)

    #return f"{table_row.css('th::text').strip()}: {table_row.css('td::text').strip()}"


class TedoraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()



    def __init__(self):
        super().__init__()
        self.fields['Product name'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=TakeFirst()
        )
        self.fields['SKU'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )
        self.fields['Category'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=Compose(lambda x: x[2])
        )
        self.fields['Subcategory'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=Join(', ')
        )
        self.fields['Short Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=Join(' ')
        )
        self.fields['Long Description'] = scrapy.Field(
            input_processor=MapCompose(
                remove_tags
            ),
            output_processor=long_description
        )
        # self.fields['Long Description'] = scrapy.Field(
        #     input_processor=MapCompose(
        #         remove_tags
        #     )
        # )
        self.fields['Featured Image URL'] = scrapy.Field(output_processor=TakeFirst()

        )
        self.fields['Images URLs'] = scrapy.Field(output_processor=Join(', ')

        )
        self.fields['Product URL'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )

class BreuningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __init__(self):
        super().__init__()
        self.fields['Product name'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )
        self.fields['SKU'] = scrapy.Field(
            output_processor=TakeFirst()
        )
        self.fields['Category'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=lambda x: x[1]
        )
        self.fields['Subcategory'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, breuning_subcategory),
            output_processor=TakeFirst()
        )
        self.fields['Short Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()), output_processor=TakeFirst())

        self.fields['Long Description'] = scrapy.Field(
            output_processor=Join('; ')
        )
        self.fields['Featured Image URL'] = scrapy.Field(output_processor=TakeFirst()

        )
        self.fields['Images URLs'] = scrapy.Field(output_processor=Join(', ')

        )
        self.fields['Product URL'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )

def breuning_subcategory(value):

    if 'BRACELET' in value.upper():
        return 'BRACELETS'
    elif 'COLLIER' in value.upper():
        return 'COLLIER'
    elif 'RING' in value.upper():
        return 'RINGS'
    elif 'PENDANT' in value.upper():
        return 'PENDANTS'
    elif 'STUD' or 'EARRING' in value.upper():
        return 'STUDS'
    elif 'CHAIN' in value.upper():
        return 'CHAINS'
    else:
        return ''

def breuning_long_description(description_elements):

    index = len(description_elements) / 2
    list_label = [f"{element.strip()}:" for num, element in enumerate(description_elements) if num < index]
    list_value = [f"{element.strip()}" for num, element in enumerate(description_elements) if num >= index]
    #list_value = [f"{element.strip()}:" if num < index else f"{element.strip}," for num, element in enumerate(description_elements)]
    list  = [f"{label} {value}" for label, value in zip(list_label, list_value)]
    return '; '.join(list)

class BoccadamoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    def __init__(self):
        super().__init__()
        self.fields['Product name'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.replace('\n', ' ').strip()),
            output_processor=TakeFirst()
        )
        self.fields['SKU'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.split()[1]),
            output_processor=TakeFirst()
        )
        self.fields['Category'] = scrapy.Field(
            output_processor=TakeFirst()
        )
        self.fields['Subcategory'] = scrapy.Field(
            output_processor=TakeFirst()
        )
        self.fields['Short Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()), output_processor=TakeFirst())

        self.fields['Long Description'] = scrapy.Field(
            input_processor=MapCompose(lambda x: x.replace('<br>', ';'), remove_tags, lambda x: x.strip()),
            output_processor=TakeFirst()
        )
        self.fields['Featured Image URL'] = scrapy.Field(output_processor=TakeFirst()

        )
        self.fields['Images URLs'] = scrapy.Field(output_processor=Join(', ')

        )
        self.fields['Product URL'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )

class GioiapuraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()



    def __init__(self):
        super().__init__()
        self.fields['Product name'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=TakeFirst()
        )
        self.fields['SKU'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.split(':')[-1].strip()),
            output_processor=TakeFirst()
        )
        self.fields['Category'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=gioiapura_category
        )
        self.fields['Subcategory'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=gioiapura_subcategory
        )
        self.fields['Short Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=TakeFirst()
        )
        self.fields['Long Description'] = scrapy.Field(
            input_processor=MapCompose(remove_tags, lambda x: x.strip()),
            output_processor=lambda x: x[-1]
        )
        # self.fields['Long Description'] = scrapy.Field(
        #     input_processor=MapCompose(
        #         remove_tags
        #     )
        # )
        self.fields['Featured Image URL'] = scrapy.Field(
            input_processor=gioiapura_images, output_processor=TakeFirst()
        )
        self.fields['Images URLs'] = scrapy.Field(input_processor=gioiapura_images, output_processor=Join(', ')

        )
        self.fields['Product URL'] = scrapy.Field(
            input_processor=MapCompose(remove_tags),
            output_processor=TakeFirst()
        )

def gioiapura_category(description_elements):

    description = ' '.join(description_elements)
    lines = description.split('\n')
    for line in lines:
        if 'category' in line.lower():
            return line.split(':')[-1].strip().title()

def gioiapura_subcategory(description_elements):
    description = ' '.join(description_elements)
    lines = description.split('\n')
    for line in lines:
        if 'subcategory' in line.lower():
            return line.split(':')[-1].strip().title()

def gioiapura_images(images):
    images_zoom = []
    for img in images:
        images_zoom.append(img.replace('_ico.', '_zoom.'))
    return images_zoom
