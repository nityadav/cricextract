from bs4 import BeautifulSoup
import urllib.request


match_class = {'test': 1, 'odi': 2, 't20': 3}
batting_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=%d;filter=advanced;orderby=batted_score;orderbyad=reverse;page=%d;size=200;spanmin2=27+dec+2017;spanval2=span;template=results;type=batting;view=innings"


def get_player_aggr(idx, player_html_tr, soup):
    """
    Extract table info for a single player
    :param player_html_tr: 
    :return: 
    """
    return '\t'.join(map(lambda x: x.get_text(), player_html_tr.find_all('td'))) + '\t' + soup.find('div', attrs={'id': 'engine-dd' + str(idx + 1)}).find('a', text="Match scorecard")['href']


def aggregates_generator(page_num):
    """
    Extract info from the page
    :param page_num: 
    :return: 
    """
    print("Extracting page no. %d" % page_num)
    url = batting_url % (match_class['test'], page_num)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    player_trs = soup.find_all('tr', attrs={'class': 'data1'})
    if player_trs:
        page_num += 1
        return [get_player_aggr(i, p, soup) for i, p in enumerate(player_trs)]
    else:
        return []


with open('data/batting.20180903.txt', 'w') as f:
    for pg in range(1, 7):
        new_rows = aggregates_generator(pg)
        f.write('\n'.join(new_rows) + '\n')

