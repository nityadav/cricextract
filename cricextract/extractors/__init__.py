from abc import ABC, abstractmethod
import logging
import urllib.request
from retry import retry


class Extractor(ABC):
    @staticmethod
    def _make_record(fields, values):
        return {k.strip(): v.strip() for k, v in zip(fields, values) if v.strip()}

    @staticmethod
    def _get_id_or_text(text_soup):
        if text_soup is None:
            return None
        if text_soup.name == 'a':
            a_soup = text_soup
        else:
            a_soup = text_soup.find('a')
        if a_soup is not None and a_soup.has_attr('href') and a_soup.attrs['href'].startswith('http'):
            return a_soup.attrs['href'].split("/")[-1].split('.')[0]
        else:
            return text_soup.get_text().strip()

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
    def _get_page_content(self, page_num):
        url = "{}?{};page={}".format(self.hostname, self.params, page_num)
        return urllib.request.urlopen(url).read()

    def collect(self, output_file):
        with open(output_file, 'w') as output_f:
            for page_num in range(1, self.num_pages + 1):
                logging.info("Extracting page no. {}".format(page_num))
                page_content = self._get_page_content(page_num)
                output_f.write(self.extractor.extract(page_content) + "\n")
