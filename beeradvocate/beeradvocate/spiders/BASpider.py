from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from beeradvocate.items import BeerAdvocateItem
import html2text, re

class BASpider(CrawlSpider):
    name = 'BA'
    allowed_domains = ['beeradvocate.com']
    start_urls = ['http://beeradvocate.com/beer/style']


    rules = (
        # Extract the Style links, but not the top listings for each style
        Rule(SgmlLinkExtractor(allow=('/beer/style/[0-9]+/?(\?start=[0-9]+)?$', ), unique=True)),
        
        # Extract brewery links, but do not process any info - should optimize crawl time?
        Rule(SgmlLinkExtractor(allow=('/beer/profile/[0-9]+/?$', ), unique=True)),
        
        # Extract specific beers and additional reviews for beers but ensure no repeats
        #Rule(SgmlLinkExtractor(allow=('beer/profile/[0-9]+/[0-9]+/?(\?view=beer&sort=&start=[0+9]+)?$'),
        #                       unique=True, follow=True), callback=parse_beer),
        
        # Instead, just take first 25 Reviews. Should be sufficient for decent search
        Rule(SgmlLinkExtractor(allow=('beer/profile/[0-9]+/[0-9]+/?$'),
                               unique=True), callback='parse_beer'),

    )

    def parse_beer(self, response):
        self.log('We\'ve got reviews for a beer at URL: %s' % response.url)

        hxs = HtmlXPathSelector(response)
        
        item = BeerAdvocateItem()
        
        # Simply the url
        item['url'] = response.url
        
        # The part of the titleBar div that is the first set of text
        item['name'] = hxs.select('//div[@class="titleBar"]/h1').re(r'(?<=>)(.*?)(?=<s)')[0]
        
        # The part of the titleBar div inside a span not including the '-' character 
        item['brewery'] = hxs.select('//div[@class="titleBar"]/h1/span/text()').re(r'-\s*(.*)')[0]
        
        # Extract the first and second numbers in the URL
        item['brewery_number'] = re.search(r'(?<=profile/)(.*)(?=/)', response.url).group()
        item['beer_number'] = re.search(r'(?<=[0-9]/)(.*)(?=$)', response.url).group()
        
        # Get the weighted score according to users. Bros score not counted
        item['BA_score'] = hxs.select('//span[@class="BAscore_big"]/text()').extract()[0]
        
        #initialize a html to text converter
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        
        #Extract the style of the beer and ABV. Style is done in very hacky way
        item['style'] = re.search(r'(?<=b>)(.*)', hxs.select('//div[@id="baContent"]/table[1]').re(r'(?<=/style/)(.*?)(?=</b></a>)')[-1]).group()
        try:
            item['ABV'] = hxs.select('//div[@id="baContent"]/table[1]').re(r'([0-9\s]{2}.[0-9]{2})(?=\%)')[-1]
        except IndexError:
            item['ABV'] = '0.0'
        
        #Extract the first page of reviews
        review_list = hxs.select('//div[@id="rating_fullview_content_2"]').re(r'(?<=[0-9]<br><br>)(.*?)(?=<br><br>Serving)')
        review = ""
        for j in review_list:
            review += re.sub('\r', '',re.sub('<[^<]+?>', ' ', j))
        item['reviews'] = review
        return item