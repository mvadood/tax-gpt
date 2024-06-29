import scrapy
from w3lib.html import remove_tags


class TaxSpider(scrapy.Spider):
    name = "tax"
    allowed_domains = ["ato.gov.au"]
    start_urls = ["https://www.ato.gov.au/"]

    def __init__(self, max_depth=1, *args, **kwargs):
        super(TaxSpider, self).__init__(*args, **kwargs)
        self.max_depth = int(max_depth)  # Convert the depth to an integer
        self.visited_urls = set()  # Set to keep track of visited URLs

    def parse(self, response):
        current_depth = response.meta.get('depth', 0)

        page_text = response.xpath(
            "//p[not(ancestor::header) and not(ancestor::*[contains(@id, 'nav')])]//text()").getall()

        page_text = [text.strip() for text in page_text if
                     not ("Traditional Owners and Custodians" in text or "RSS news feeds" in text)]

        page_text = '\n'.join(page_text).strip()
        page_text = remove_tags(page_text)

        yield {
            'url': response.url,
            'text': page_text,
            'depth': current_depth
        }

        self.visited_urls.add(response.url)

        if current_depth < self.max_depth:
            links = response.xpath("//a/@href").getall()
            for link in links:
                if link.startswith('http'):
                    next_page = link
                else:
                    next_page = response.urljoin(link)

                if any(domain in next_page for domain in self.allowed_domains):
                    yield scrapy.Request(next_page, callback=self.parse, meta={'depth': current_depth + 1})
