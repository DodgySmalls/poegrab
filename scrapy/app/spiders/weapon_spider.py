import scrapy

class WeaponSpide(scrapy.Spider):
    name = "weapon"
    allowed_domains = ["pathofexile.com"]
    start_urls = [
        "http://www.pathofexile.com/item-data/weapon"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)