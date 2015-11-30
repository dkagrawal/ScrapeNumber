import scrapy

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class MeowItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
