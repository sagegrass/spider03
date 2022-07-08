import scrapy


class ImgItem(scrapy.Item):

    img = scrapy.Field()
    number = scrapy.Field()

