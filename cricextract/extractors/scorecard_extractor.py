from bs4 import BeautifulSoup
from cricextract.extractors import Extractor
import urllib.request
import json


class ScorecardExtractor(Extractor):
    def __init__(self, num_innings):
        self.num_innings = num_innings

    def __make_record__(self, fields, values):
        return {k.strip(): v.strip() for k, v in zip(fields, values) if v.strip()}

    def __make_batting_record__(self, fields, values):
        # make the key as `result` if it is empty
        return {"result" if not k else k: v for k, v in self.__make_record__(fields, values).items()}

    def __make_bowling_record(self, fields, values):
        return self.__make_record__(fields, values)

    def __extract_batting_section__(self, inning_soup):
        batting_soup = inning_soup.find('div', attrs={'class': 'scorecard-section batsmen'})
        header_soup = batting_soup.find('div', attrs={'class': 'wrap header'})
        fields = [field_soup.get_text() for field_soup in header_soup.find_all('div')]
        batsmen_soup = batting_soup.find_all('div', attrs={'class': 'wrap batsmen'})
        battings = []
        for batsman_soup in batsmen_soup:
            values = [values_soup.get_text() for values_soup in batsman_soup.find_all('div')]
            battings.append(self.__make_batting_record__(fields, values))
        return battings

    def __extract_bowling_section__(self, inning_soup):
        bowling_soup = inning_soup.find('div', attrs={'class': 'scorecard-section bowling'})
        header_soup = bowling_soup.find('thead')
        fields = [field_soup.get_text() for field_soup in header_soup.find_all('th')]
        bowlings = []
        for bowler_soup in bowling_soup.find('tbody').find_all('tr'):
            values = [values_soup.get_text() for values_soup in bowler_soup.find_all('td')]
            bowlings.append(self.__make_bowling_record(fields, values))
        return bowlings

    def extract(self, html_content: str):
        scorecard_soup = BeautifulSoup(html_content, "html.parser")
        pom = scorecard_soup.find('a', attrs={'class': 'gp__cricket__player-match__player__detail__link'}).get_text()
        match = {'pom': pom.strip(), 'innings': []}
        for inning_num in range(self.num_innings):
            inning_soup = scorecard_soup.find('div', attrs={'id': "gp-inning-0{}".format(inning_num)})
            match['innings'].append({'batting': self.__extract_batting_section__(inning_soup),
                                     'bowling': self.__extract_bowling_section__(inning_soup)})
        print(json.dumps(match))


if __name__ == '__main__':
    ext = ScorecardExtractor(2)
    url = "https://www.espncricinfo.com/series/8039/scorecard/1144504/india-vs-pakistan-22nd-match-icc-cricket-world-cup-2019"
    content = urllib.request.urlopen(url).read()
    ext.extract(content)
