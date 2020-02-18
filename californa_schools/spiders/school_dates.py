# -*- coding: utf-8 -*-
import scrapy


class RootSpider(scrapy.Spider):
    name = 'dates'
    allowed_domains = ['publicholidays.us']
    start_urls = ['https://publicholidays.us/school-holidays/california/']

    def parse(self, response):
        for a in response.xpath('//tbody//a'):
            yield scrapy.Request(a.attrib['href'],
                callback=self.parse_district,
                cb_kwargs=dict(district=a.xpath('text()').get()))

    def parse_district(self, response, district):
        for tbody in response.xpath('//tbody'):
            start_date = tbody.xpath('tr/td[span[contains(text(), "First")]]/following-sibling::td/text()')[0].get()
            end_date = tbody.xpath('tr/td[span[contains(text(), "Last")]]/following-sibling::td/text()')[0].get()
            yield {
                'district': district,
                'start': start_date,
                'end': end_date
            }            
