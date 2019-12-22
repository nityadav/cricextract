from bs4 import BeautifulSoup
import urllib2


match_class = {'test': 1, 'odi': 2, 't20': 3}
batting_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=%d;page=%d;template=results;type=bowling"

# id="engine-dd50"


def get_player_aggr(player_html_tr):
    return '\t'.join(map(lambda x: x.get_text(), player_html_tr.find_all('td')))


def aggregates_generator(page_num):
    print("Extracting page no. %d" % page_num)
    url = batting_url % (match_class['odi'], page_num)
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    player_trs = soup.find_all('tr', attrs={'class': 'data1'})
    if player_trs:
        page_num += 1
        return map(get_player_aggr, player_trs)
    else:
        return []


all_records = []
for pg in range(1, 49):
    new_50 = aggregates_generator(pg)
    all_records += new_50

with open('data/players_aggregates/odi/bowling.txt', 'w') as f:
    f.write('\n'.join(all_records))
