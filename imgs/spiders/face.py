import scrapy
from ..items import ImgItem
from base64 import b64decode
from ..settings import Q_START
from ..settings import Q_END


class FaceSpider(scrapy.Spider):
    name = 'face'

    def start_requests(self):
        base_url = "aHR0cHM6Ly9xbG9nbzQuc3RvcmUucXEuY29tL3F6b25lLw=="
        for number in range(Q_START, Q_END):
            url = b64decode(base_url).decode() + str(number) + "/" + str(number) + "/" + "640"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"number": number}
            )

    def parse(self, response):
        item = ImgItem()
        item["number"] = response.meta["number"]
        item["img"] = response.body
        yield item
