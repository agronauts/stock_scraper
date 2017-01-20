BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'patrick',
    'password': '',
    'database': 'scrape'
}
# May have trouble with logging in

ITEM_PIPELINES = ['scraper_app.pipelines.LivingSocialPipeline']
