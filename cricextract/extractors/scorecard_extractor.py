import json
import urllib.request
import os
from bs4 import BeautifulSoup
from retry import retry

from cricextract.extractors import Extractor


class ScorecardExtractor(Extractor):
    def __init__(self, num_innings):
        self.num_innings = num_innings

    def _make_batting_record(self, fields, values):
        # make the key as `result` if it is empty
        return {"result" if not k else k: v for k, v in self._make_record(fields, values).items()}

    def __make_bowling_record(self, fields, values):
        return self._make_record(fields, values)

    def _extract_batting_section(self, inning_soup):
        batting_soup = inning_soup.find('div', attrs={'class': 'scorecard-section batsmen'})
        header_soup = batting_soup.find('div', attrs={'class': 'wrap header'})
        fields = [field_soup.get_text() for field_soup in header_soup.find_all('div')]
        batsmen_soup = batting_soup.find_all('div', attrs={'class': 'wrap batsmen'})
        battings = []
        for batsman_soup in batsmen_soup:
            values = [self._get_id_or_text(values_soup) for values_soup in batsman_soup.find_all('div')]
            battings.append(self._make_batting_record(fields, values))
        return battings

    def _extract_bowling_section(self, inning_soup):
        bowling_soup = inning_soup.find('div', attrs={'class': 'scorecard-section bowling'})
        header_soup = bowling_soup.find('thead')
        fields = [field_soup.get_text() for field_soup in header_soup.find_all('th')]
        bowlings = []
        for bowler_soup in bowling_soup.find('tbody').find_all('tr'):
            values = [self._get_id_or_text(values_soup) for values_soup in bowler_soup.find_all('td')]
            bowlings.append(self.__make_bowling_record(fields, values))
        return bowlings

    def extract(self, html_content: str):
        scorecard_soup = BeautifulSoup(html_content, "html5lib")
        pom = self._get_id_or_text(
            scorecard_soup.find('a', attrs={'class': 'gp__cricket__player-match__player__detail__link'}))
        match = {'pom': pom, 'innings': []}
        for inning_num in range(self.num_innings):
            inning_soup = scorecard_soup.find('div', attrs={'id': "gp-inning-0{}".format(inning_num)})
            match['innings'].append({'batting': self._extract_batting_section(inning_soup),
                                     'bowling': self._extract_bowling_section(inning_soup)})
        return match


class OdiScorecardExtractor(ScorecardExtractor):
    def __init__(self):
        super(OdiScorecardExtractor, self).__init__(2)


@retry(delay=2)
def get_page_content(scorecard_url):
    # return urllib.request.urlopen("http://stats.espncricinfo.com{}".format(scorecard_uri)).read()
    return urllib.request.urlopen(scorecard_url).read()


if __name__ == '__main__':
    ext = OdiScorecardExtractor()
    sc = ext.extract(get_page_content("http://stats.espncricinfo.com/ci/engine/match/566939.html"))
    print(json.dumps(sc))
    # existing_scorecards = {i.split('.')[0] for i in os.listdir("/Users/nitin/Projects/cricket/cricextract/data/scorecards")}
    # with open("/Users/nitin/Projects/cricket/cricextract/data/all_odis.json") as all_odis_f:
    #     all_odis = json.load(all_odis_f)
    #     for odi in all_odis:
    #         uri = odi['Match scorecard']
    #         odi_id = uri.split("/")[-1].split('.')[0]
    #         if odi_id in existing_scorecards:
    #             continue
    #         print("Getting scorecard for {}".format(odi_id))
    #         page_content = get_page_content(uri)
    #         scorecard = ext.extract(page_content)
    #         with open(os.path.join("/Users/nitin/Projects/cricket/cricextract/data/scorecards", "{}.json".format(odi_id)), "w") as out_f:
    #             json.dump(scorecard, out_f)
