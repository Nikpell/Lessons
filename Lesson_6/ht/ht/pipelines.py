import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class CustomFilesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['name']}.jpg"

    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        print(results)
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter["image_paths"] = image_paths
        image_paths = [x["path"] for ok, x in results if ok]
        return item
