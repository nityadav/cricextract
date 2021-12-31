from bs4 import BeautifulSoup

from cricextract.extractors import SoupExtractor


class SoupTableExtractor(SoupExtractor):
    def extract(self, table_soup: BeautifulSoup):
        """
        :param table_soup: a soup from <table> html
        :return: list of records, where each record is a dict [{},{},...]
        """
        cols = self._get_cols(table_soup.find('thead'))
        tr_soups = table_soup.find('tbody').find_all('tr')
        rows = [self._get_row(tr, cols) for tr in tr_soups]
        return rows

    @staticmethod
    def _get_cols(thead_soup: BeautifulSoup):
        return [th.get_text() for th in thead_soup.find_all('th')]

    @staticmethod
    def _get_row(tr_soup, cols):
        return {cols[idx]: td.get_text() for idx, td in enumerate(tr_soup.find_all('td'))}


if __name__ == '__main__':
    test_table = """<table class="table batsman"><thead class="thead-light bg-light"><tr><th style="width:25%">BATTING</th><th style="width:25%">&nbsp;</th><th style="width:8%">R</th><th style="width:8%" class="text-uppercase">B</th><th style="width:8%">M</th><th style="width:8%">4s</th><th style="width:8%">6s</th><th style="width:10%">SR</th></tr></thead><tbody><tr><td class="batsman-cell text-truncate out"><a data-hover="" class="small" target="_self" rel="" title="View full profile of Aaron Finch" href="/player/aaron-finch-5334">Aaron Finch<!-- -->&nbsp;</a></td><td class="text-left"><span class="cursor-pointer"><i id="caret-35812" class="espn-icon icon-caret-sm2-down-after icon-sm text-danger font-weight-bold small pr-1"></i>c Coleman b Haq</span></td><td class="font-weight-bold">148</td><td>114</td><td>147</td><td>16</td><td>7</td><td>129.82</td></tr><tr><td class="p-0 border-0 d-none out" colspan="9"></td></tr><tr><td class="batsman-cell text-truncate out"><a data-hover="" class="small" target="_self" rel="" title="View full profile of Shaun Marsh" href="/player/shaun-marsh-6683">Shaun Marsh<!-- -->&nbsp;</a></td><td class="text-left"><span class="cursor-pointer"><i id="caret-10129" class="espn-icon icon-caret-sm2-down-after icon-sm text-danger font-weight-bold small pr-1"></i>c Goudie b Wardlaw</span></td><td class="font-weight-bold">151</td><td>151</td><td>184</td><td>16</td><td>5</td><td>100.00</td></tr><tr><td class="p-0 border-0 d-none out" colspan="9"></td></tr><tr><td class="batsman-cell text-truncate out"><a data-hover="" class="small" target="_self" rel="" title="View full profile of Shane Watson" href="/player/shane-watson-8180">Shane Watson<!-- -->&nbsp;</a></td><td class="text-left"><span class="cursor-pointer"><i id="caret-10125" class="espn-icon icon-caret-sm2-down-after icon-sm text-danger font-weight-bold small pr-1"></i>c Goudie b Wardlaw</span></td><td class="font-weight-bold">37</td><td>24</td><td>38</td><td>6</td><td>0</td><td>154.16</td></tr><tr><td class="p-0 border-0 d-none out" colspan="9"></td></tr><tr><td class="batsman-cell text-truncate not-out"><a data-hover="" class="small" target="_self" rel="" title="View full profile of Michael Clarke" href="/player/michael-clarke-4578">Michael Clarke<!-- -->&nbsp;<span>(c)</span></a></td><td class="text-left">not out </td><td class="font-weight-bold">4</td><td>5</td><td>10</td><td>0</td><td>0</td><td>80.00</td></tr><tr><td class="p-0 border-0 d-none not-out" colspan="9"></td></tr><tr><td class="batsman-cell text-truncate not-out"><a data-hover="" class="small" target="_self" rel="" title="View full profile of George Bailey" href="/player/george-bailey-4451">George Bailey<!-- -->&nbsp;</a></td><td class="text-left">not out </td><td class="font-weight-bold">10</td><td>7</td><td>8</td><td>0</td><td>1</td><td>142.85</td></tr><tr><td class="p-0 border-0 d-none not-out" colspan="9"></td></tr><tr class="extras"><td colspan="1">Extras</td><td class="text-left">(b 3, lb 3, nb 1, w 5)</td><td colspan="1" class="text-right font-weight-bold">12</td><td colspan="7" class="text-right"></td></tr></tbody><tfoot><tr class="thead-light bg-light total"><td colspan="1">TOTAL</td><td class="text-left">(50 Ov, RR: 7.24, 195 Mts)</td><td colspan="1" class="text-right font-weight-bold">362<!-- -->/3</td><td colspan="7" class="text-right"></td></tr><tr><td colspan="9"><div><strong>Did not bat: </strong><a data-hover="" class="small" target="_self" rel="" href="/player/adam-voges-8119"><span>Adam Voges<!-- -->,<!-- -->&nbsp;</span></a><a data-hover="" class="small" target="_self" rel="" href="/player/matthew-wade-230193"><span>Matthew Wade<span>&nbsp;†</span>,<!-- -->&nbsp;</span></a><a data-hover="" class="small" target="_self" rel="" href="/player/fawad-ahmed-240609"><span>Fawad Ahmed<!-- -->,<!-- -->&nbsp;</span></a><a data-hover="" class="small" target="_self" rel="" href="/player/mitchell-johnson-6033"><span>Mitchell Johnson<!-- -->,<!-- -->&nbsp;</span></a><a data-hover="" class="small" target="_self" rel="" href="/player/james-faulkner-270484"><span>James Faulkner<!-- -->,<!-- -->&nbsp;</span></a><a data-hover="" class="small" target="_self" rel="" href="/player/clint-mckay-6903"><span>Clint McKay<!-- -->&nbsp;</span></a></div></td></tr><tr><td colspan="9"><div><strong>Fall of wickets<!-- -->: </strong><span>1<!-- -->-<!-- -->246<!-- --> (<!-- -->Aaron Finch<!-- -->, 38.2 ov<!-- -->)</span><span>, <!-- -->2<!-- -->-<!-- -->347<!-- --> (<!-- -->Shaun Marsh<!-- -->, 47.5 ov<!-- -->)</span><span>, <!-- -->3<!-- -->-<!-- -->347<!-- --> (<!-- -->Shane Watson<!-- -->, 47.6 ov<!-- -->)</span></div></td></tr></tfoot></table>"""
    table_soup = BeautifulSoup(test_table, features="html5lib")
    ste = SoupTableExtractor()
    table = ste.extract(table_soup)
    import json
    print(json.dumps(table))
