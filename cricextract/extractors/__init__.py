from abc import ABC, abstractmethod
import logging
import urllib.request
from retry import retry


class Extractor(ABC):
    @abstractmethod
    def extract(self, html_content: str):
        """
        The method should be overridden to parse and extract the HTML content and return the extracted data
        """
        pass


class Collector(object):
    def __init__(self, extractor: Extractor, params: str, num_pages: int):
        self.hostname = "http://stats.espncricinfo.com/ci/engine/stats/index.html"
        self.params = params
        self.num_pages = num_pages
        self.extractor = extractor

    @retry(delay=2)
    def __get_page_content__(self, page_num):
        url = "{}?{};page={}".format(self.hostname, self.params, page_num)
        return urllib.request.urlopen(url).read()

    def collect(self, output_file):
        with open(output_file, 'w') as output_f:
            for page_num in range(1, self.num_pages + 1):
                logging.info("Extracting page no. {}".format(page_num))
                page_content = self.__get_page_content__(page_num)
                output_f.write(self.extractor.extract(page_content))
