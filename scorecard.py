from bs4 import BeautifulSoup
import urllib.request


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
        fours_idx = header_items_texts.index("4s")
        sixes_idx = header_items_texts.index("6s")
        batsmen_soup = inning_soup.find_all('div', attrs={'class': 'wrap batsmen'})
        total_boundaries = 0
        for b in batsmen_soup:
            four_soup = b.find_all('div', attrs={'class': 'cell runs'})[fours_idx]
            six_soup = b.find_all('div', attrs={'class': 'cell runs'})[sixes_idx]
            boundaries = int(four_soup.get_text()) + int(six_soup.get_text())
            total_boundaries += boundaries
    return total_boundaries

url = "https://www.espncricinfo.com/series/19062/scorecard/1168519/ireland-vs-zimbabwe-3rd-odi-zim-in-ireland-and-nl-2019"

print(get_total_boundaries(url, 2))
