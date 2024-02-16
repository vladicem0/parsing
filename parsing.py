import requests
from lxml import html


def request(url: str, headers: dict[str, str] = None) -> (requests.get, int):
    try:
        if headers is None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'}
        req = requests.get(url, headers=headers)
        exit_code = int(str(req).split()[1][1:-2])
    except requests.ConnectionError:
        req = -1
        exit_code = -1
    return req, exit_code


def request_to_html(request_source: requests.get, encoding: str = 'UTF-8') -> html:
    html_source = html.fromstring(str(request_source.text.encode(encoding)))
    return html_source


def parsing() -> (list[list[dict[str, str | int | float | list[int]]]], int):
    data_list, exit_code = [], 0
    url = f'https://myanimelist.net/topanime.php'
    req, exit_code = request(url)
    if exit_code != 200:
        return ['empty data'], exit_code

    tree = request_to_html(req)
    table = tree.xpath('//table[@class = "top-ranking-table"]')[0]
    page_list = table.xpath('//tr[@class = "ranking-list"]')[:10]
    i = 0
    for page in page_list:
        print(i)
        i += 1
        page_link = page.xpath('.//h3[@class = "hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"]/a/@href')[0]
        url = str(page_link)
        req, exit_code = request(url)
        if exit_code != 200:
            return ['empty data'], exit_code
        details = request_to_html(req)

        data = {'name': str, 'average_score': float, 'ratings_count': int, 'views_count': int, 'ratings': list}
        ratings_count = details.xpath('//div[@class = "fl-l score"]/@data-user')[0]
        data['ratings_count'] = int(ratings_count.split()[0].replace(',', ''))
        data['name'] = details.xpath('//h1[@class = "title-name h1_bold_none"]/strong/text()')[0]
        data['average_score'] = float(details.xpath('//div[@class = "fl-l score"]/div/text()')[0])

        stat_link = details.xpath('//div[@id = "horiznav_nav"]/ul/li/a/text()')
        for i in range(len(stat_link)):
            if stat_link[i] == 'Stats':
                stat_link = details.xpath('//div[@id = "horiznav_nav"]/ul/li/a/@href')[i]
                break

        url = str(stat_link)
        req, exit_code = request(url)
        if exit_code != 200:
            return ['empty data'], exit_code
        stats_page = request_to_html(req)

        stats = stats_page.xpath('//div[@class = "spaceit_pad"]')
        for i in range(len(stats)):
            if len(stats[i].xpath('.//span[@class = "dark_text"]/text()')) != 0 and \
                    str(stats[i].xpath('.//span[@class = "dark_text"]/text()')[0]) == 'Completed:':
                data['views_count'] = int(stats[i].xpath('.//text()')[1].replace(',', ''))

        score_table = stats_page.xpath('//table[@class = "score-stats"]')
        data['ratings'] = []
        for i in range(10):
            data['ratings'].append(int(score_table[0].xpath('.//small/text()')[i].split()[0].replace('(', '')))

        data_list.append(data)

    return data_list, exit_code
