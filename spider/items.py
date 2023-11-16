from itemloaders.processors import TakeFirst
from scrapy.item import Field, Item


class RakutenItem(Item):
    crawled_url = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    serves = Field(output_processor=TakeFirst())
    ingredients = Field(output_processor=TakeFirst())
    image_path = Field(output_processor=TakeFirst())
