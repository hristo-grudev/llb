import scrapy

from scrapy.loader import ItemLoader
from ..items import LlbItem
from itemloaders.processors import TakeFirst


class LlbSpider(scrapy.Spider):
	name = 'llb'
	start_urls = ['https://www.llb.li/en/llb/media/media-communiques/media-communiques']

	def parse(self, response):
		post_links = response.xpath('//section[@class="entry entry--blog"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="h2"]/text()').get()
		description = response.xpath('//div[@class="sc-richtext"]//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="blog__datetime"]//text()').get()

		item = ItemLoader(item=LlbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
