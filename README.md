beeradvocate_crawl
==================

Crawling beeradvocate and building a search engine for it.

Start local server with 'python manage.py runserver'
Start SOLR search with 'java -jar start.jar' from /apache-solr-3.5.0/example

In order to do a recrawl of beeradvocate, first 'python manage.py flush' and then 'scrapy crawl BA' from /beeradvocate
In order to update scorings, 'python manage.py update_index'
In order to rebuild indexer, 'python manage.py rebuild_index'


In order to build, you need a full solr installation, but replace the example schema.xml with the one provided

In addition, all the requirements in requirements.txt are needed