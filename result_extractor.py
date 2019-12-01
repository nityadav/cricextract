from bs4 import BeautifulSoup
import urllib.request


results_url = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page=%d;template=results;type=aggregate;view=results"


def get_result(idx, result_tr, soup):
    return '\t'.join(map(lambda x: x.get_text(), result_tr.find_all('td'))) + \
           '\t' + soup.find('div', attrs={'id': 'engine-dd' + str(idx + 1)}).find('a', text="Match scorecard")['href']


def aggregates_generator(page_num):
    """
    Extract info from the page
    :param page_num:
    :return:
    """
    print("Extracting page no. %d" % page_num)
    url = results_url % page_num
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    result_trs = soup.find_all('tr', attrs={'class': 'data1'})
    if result_trs:
        page_num += 1
        return [get_result(i, p, soup) for i, p in enumerate(result_trs)]
    else:
        return []


with open('data/results.20190102.txt', 'w') as f:
    for pg in range(1, 49):
        new_rows = aggregates_generator(pg)
        f.write('\n'.join(new_rows) + '\n')

