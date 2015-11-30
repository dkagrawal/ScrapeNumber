# -*- coding: utf-8 -*-
'''Spider for truecaller.com,works only for limited number of searches'''
import scrapy
import re
import os
# provide your own authentication cookies
my_cookies = {"truecaller-session": '******', "user": '*******'}


class TruecallerSpider(scrapy.Spider):

    '''This class contains the spider used for crawling truecaller.com
    For more information,read documentation of scrapy at
    http://doc.scrapy.org/en/latest/
    '''
    name = "truecaller"
    allowed_domains = ["truecaller.com"]
    start_urls = (
        'http://www.truecaller.com/',
    )

    def parse(self, response):
        '''This function authenticates the user
         session using supplied cookies'''
        return scrapy.Request('http://www.truecaller.com/',
                              cookies=my_cookies, callback=self.parsestart)

    def parsestart(self, response):
        '''This function crawls all the numbers
         provided as input.You canRun a for loop for
          more than 1 number,
          but total number of searches is limited'''
        val = response.xpath('/html/body/nav[2]/div[2]/a[6]/text()').extract()
        url = response.url + 'in/' + '**********'
        yield scrapy.Request(url, callback=self.parsename)

    def parsename(self, response):
        # Provides the name of the numbers requested in parsestart
        name = response.xpath('/html/body/main/section/div[2]/div[1]/div[1]\
            /div[2]/div/div[1]/text()').extract()
        number = response.xpath('/html/body/main/section/div[2]/div[1]/\
            div[2]/div[1]/div/div/h1/text()').extract()
        print name + '-' + number
