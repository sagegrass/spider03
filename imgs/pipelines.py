from redis import Redis
from hashlib import md5
from os import mkdir
from os.path import exists, join
from scrapy.exceptions import DropItem


class RedisPipeline:

    def __init__(self, redis_host, redis_port, redis_db, redis_password):
        self.host = redis_host
        self.port = redis_port
        self.db = redis_db
        self.password = redis_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_host=crawler.settings.get("REDIS_HOST"),
            redis_port=crawler.settings.get("REDIS_PORT"),
            redis_db=crawler.settings.get("REDIS_DB"),
            redis_password=crawler.settings.get("REDIS_PASSWORD"),
        )

    def open_spider(self, spider):
        self.redis = Redis(host=self.host, port=self.port, db=self.db, password=self.password)

    def process_item(self, item, spider):
        hash = md5()
        hash.update(item["img"])
        h = hash.hexdigest()
        if not self.redis.sismember("img", h):
            self.redis.sadd("img", h)
            return item
        else:
            return DropItem("already exists")


class ImgsDownloadPipeline:

    def __init__(self, img_path):
        self.img_path = img_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            img_path=crawler.settings.get("IMG_PATH")
        )

    def open_spider(self, spider):
        if not exists(self.img_path):
            mkdir(self.img_path)

    def process_item(self, item, spider):
        if isinstance(item, DropItem):
            return item
        save_path = join(".", self.img_path, str(item["number"]) + ".png")
        with open(save_path, "wb") as f:
            f.write(item["img"])
        return item

