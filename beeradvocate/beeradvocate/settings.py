# Scrapy settings for beeradvocate project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'beeradvocate'

SPIDER_MODULES = ['beeradvocate.spiders']
NEWSPIDER_MODULE = 'beeradvocate.spiders'

ITEM_PIPELINES = [

'beeradvocate.pipelines.BeerPipeline',


]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'beeradvocate (+http://www.yourdomain.com)'

def setup_django_env(path):
        import imp, os
        from django.core.management import setup_environ
        
        f, filename, desc = imp.find_module('settings', [path])
        project = imp.load_module('settings', f, filename, desc)       
 
        setup_environ(project)
        
        # Add django project to sys.path
        import sys
        sys.path.append(os.path.abspath(os.path.join(path, os.path.pardir)))
        
setup_django_env('/Users/johnurbanik/Documents/beeradvocate_crawl/beeradvocate_crawl/')

