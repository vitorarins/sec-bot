import scrapy

class SecSpider(scrapy.Spider):

    name = 'secspider'

    def __init__(self, cik=None, *args, **kwargs):
        super(SecSpider, self).__init__(*args, **kwargs)

        root_url = (
            "https://www.sec.gov/cgi-bin/browse-edgar?"
            "action=getcompany&CIK={cik}&output=atom"
        )

        self.cik = cik
        self.start_urls = [root_url.format(cik=cik)]

    def parse(self, response):
        response.selector.remove_namespaces()
        for company in response.xpath('//company-info'):
            yield {'company': company.xpath('//conformed-name/text()').extract_first()}
