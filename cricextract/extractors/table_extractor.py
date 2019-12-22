from bs4 import BeautifulSoup
from cricextract.extractors import Extractor
import urllib.request
import json


class TableExtractor(Extractor):
    @staticmethod
    def make_record(fields, values):
        return {k.strip(): v.strip() for k, v in zip(fields, values) if v.strip()}

    def extract(self, html_content: str):
        html_soup = BeautifulSoup(html_content, "html.parser")
        table_soup = html_soup.find('table', attrs={'class': 'engineTable'})
        thead_soup = table_soup.find('thead')
        fields = [th.get_text() for th in thead_soup.find_all('th')]
        tr_soups = table_soup.find('tbody').find_all('tr')
        records = [self.make_record(fields, [td.get_text() for td in tr.find_all('td')]) for tr in tr_soups]
        return records


def divide(mat: str, pom: str) -> str:
    return "{0:.2f}".format(int(pom)/int(mat.replace('*', '')) * 100)


if __name__ == '__main__':
    ext = TableExtractor()
    url = "http://stats.espncricinfo.com/ci/content/records/283704.html"
    content = urllib.request.urlopen(url).read()
    table = ext.extract(content)
    for r in table:
        r['Percentage'] = divide(r['Mat'], r['Awards'])
    print(json.dumps(table))
