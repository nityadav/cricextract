from bs4 import BeautifulSoup
import urllib.request


url_template = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=start;orderbyad=reverse;page=%d;result=1;result=2;result=3;size=10;template=results;type=team;view=innings"


def get_total_boundaries(match_url, inning_num):
    """
    Get total boundaries scored by batsmen in an innings
    :param match_url:
    :param inning_num: 1 or 2
    :return:
    """
    with urllib.request.urlopen(match_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        inning_id = "gp-inning-0%d" % (inning_num - 1)
        inning_soup = soup.find('div', attrs={'id': inning_id})
        header_soup = inning_soup.find('div', attrs={'class': 'wrap header'})
        header_items_soups = header_soup.find_all('div', attrs={'class': 'cell runs'})
        header_items_texts = [i.get_text() for i in header_items_soups]
        try:
            fours_idx = header_items_texts.index("4s")
        except ValueError:
            fours_idx = None
        try:
            sixes_idx = header_items_texts.index("6s")
        except ValueError:
            sixes_idx = None
        batsmen_soup = inning_soup.find_all('div', attrs={'class': 'wrap batsmen'})
        total_boundaries = 0
        for b in batsmen_soup:
            try:
                if fours_idx is not None:
                    four_soup = b.find_all('div', attrs={'class': 'cell runs'})[fours_idx]
                    total_boundaries += int(four_soup.get_text())
                if sixes_idx is not None:
                    six_soup = b.find_all('div', attrs={'class': 'cell runs'})[sixes_idx]
                    total_boundaries += int(six_soup.get_text())
            except:
                pass
    return total_boundaries


out_f = open('odi_boundaries.tsv', 'a')

for page_num in range(730, 811):
    print("Extracting page no. %d" % page_num)
    url = url_template % page_num
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all('tr', attrs={'class': 'data1'})
        for i, r in enumerate(rows):
            columns = r.find_all('td')
            name = columns[0].get_text()
            score = columns[1].get_text()
            overs = columns[2].get_text()
            inn_num = columns[4].get_text()
            result = columns[5].get_text()
            match_uri = soup.find('div', attrs={'id': 'engine-dd' + str(i + 1)}).find('a', text="Match scorecard")['href']
            boundaries = get_total_boundaries("http://stats.espncricinfo.com" + match_uri, int(inn_num))
            record = name + '\t' + score + '\t' + overs + '\t' + inn_num + '\t' + result + '\t' + match_uri + '\t' + str(boundaries)
            out_f.write(record + '\n')

out_f.close()

