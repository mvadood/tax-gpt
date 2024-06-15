# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import json


class TaxscrapyPipeline:

    def open_spider(self, spider):
        self.file_index = 1


    def process_item(self, item, spider):
        directory = "output_files"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, f'output_{self.file_index}.json')
        with open(filename, 'w') as f:
            f.write(json.dumps(dict(item)) + "\n")

        self.file_index += 1

        return item
