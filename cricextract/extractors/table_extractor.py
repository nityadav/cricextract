from bs4 import BeautifulSoup
from cricextract.extractors import Extractor
from cricextract.extractors import Collector
import json


class TableExtractor(Extractor):
    def __init__(self, table_name, get_scorecards=False):
        self.table_name = table_name
        self.get_scorecards = get_scorecards
        self.html_soup = None

    def _get_scorecard_uri(self, row_num):
        if self.html_soup is not None:
            div_soup = self.html_soup.find('div', attrs={'id': 'engine-dd{}'.format(row_num)})
            a_soups = div_soup.find_all('a')
            for a in a_soups:
                if a.get_text() == "Match scorecard":
                    return a['href']

    def _extract_table_content(self, table_soup):
        thead_soup = table_soup.find('thead')
        fields = [th.get_text() for th in thead_soup.find_all('th')]
        tr_soups = table_soup.find('tbody').find_all('tr')
        rows = []
        for idx, tr in enumerate(tr_soups):
            kv_pairs = self._make_record(fields, [td.get_text() for td in tr.find_all('td')])
            if self.get_scorecards:
                scorecard_uri = self._get_scorecard_uri(idx + 1)
                if scorecard_uri is not None:
                    kv_pairs['Match scorecard'] = scorecard_uri
            rows.append(kv_pairs)
        return rows

    def extract(self, html_content: str):
        self.html_soup = BeautifulSoup(html_content, "html.parser")
        tables = self.html_soup.find_all('table', attrs={'class': 'engineTable'})
        for table_soup in tables:
            table_caption = table_soup.find('caption')
            if table_caption is not None and table_caption.get_text() == self.table_name:
                return json.dumps(self._extract_table_content(table_soup))


if __name__ == '__main__':
    ext = TableExtractor(table_name="Match results", get_scorecards=True)
    params = "class=2;filter=advanced;orderby=start;result=1;result=2;result=3;size=200;template=results;toss=1;type=team;view=results"
    # content = urllib.request.urlopen(url).read()
    # table = ext.extract(content)
    # print(json.dumps(table))
    collector = Collector(extractor=ext, params=params, num_pages=21)
    collector.collect('all_odis.json')
