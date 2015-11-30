# -*- coding: utf-8 -*-
'''code for copying all phone numbers in your system
 from indian-mobile-directory at toolsmeow.in'''
import scrapy
from numberstalk.items import MeowItem
import os


class MeowSpider(scrapy.Spider):

    '''class used for crawling the phone number directory'''
    name = "meow"
    start_urls = (
        'http://www.toolsmeow.in/indian-mobile-directory/',
    )

    def parse(self, response):
        '''the address in xpath represents the links
         for various states,they are further crawled
          using scrapy.Request to get the required numbers'''
        for sel in response.xpath('/html/body/div[2]/div/\
                                 div[1]/div[2]/div/div[4]/a/@href'):
            url = response.urljoin(sel.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        '''this function creates the directory for all
         states and continues the crawling process'''
        dirname = response.url[:-1].replace(
            'http://www.toolsmeow.in/indian-mobile-directory/location/', '')
        os.makedirs('state/' + dirname)
        for links in response.xpath('/html/body/div[2]/div/div[1]/div[2]/div'):
            url = links.xpath('a/@href').extract()
            text = links.xpath('a/text()').extract()
        for i in range(len(url)):
            request = scrapy.Request(
                str(url[i]), callback=self.parsesecondlast)
            # meta is used to provide additional parameters,i.e state & service
            # provider of mobile no.
            request.meta['state'] = dirname
            blank = ''
            request.meta['provider'] = blank.join(
                str(text[i]).split(' series ')[1].split(' '))
            yield request

    def parsesecondlast(self, response):
        '''Another level in crawling,the web pages contains all
         numbers of format 9593******'''
        state = response.meta['state']
        provider = response.meta['provider']
        for links in response.xpath('/html/body/div[2]/div/\
                                   div[1]/div[2]/div/div[1]/a/@href'):
            url = links.extract()
            print url
            request = scrapy.Request(str(url), callback=self.parsefinal)
            request.meta['state'] = state
            request.meta['provider'] = provider
            yield request

    def parsefinal(self, response):
        '''finally,all the numbers are crawled and
         stored into seperate files according to
        service provider.'''
        path = 'state/' + \
            response.meta['state'] + '/' + response.meta['provider'] + '.txt'
        print path
        if not os.path.isfile(path):
            f = open(path, 'w')
            f.close()

        f = open(path, 'a+')
        for links in response.xpath('/html/body/div[2]/div/div[1]/\
                                   div[2]/div/div[1]/a/text()'):
            text = links.extract()
            f.write(str(text) + '\n')
        f.close()
