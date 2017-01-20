from scrapy.item import Item, Field

class LivingSocialDeal(Item):
    '''Livingsocial container for scraped data'''
    title = Field()
    link = Field()
    location = Field()
    original_price = Field()
    price = Field()
    end_date = Field()
