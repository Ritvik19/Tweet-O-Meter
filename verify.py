import requests, bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1)'
}

def verify_google_news(tag):
    try:
        parameters = {
            'q': tag,
            'hl': 'en-IN',
            'gl': 'IN',
            'ceid': 'IN%3Aen'
        }
        url = "https://news.google.com/search"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('.VDXfz')
            if len(elems) > 0:
                r = requests.get('https://news.google.com'+elems[0].get('href')[1:], headers=headers,
                                 allow_redirects=True, timeout=60)
                if r.status_code == requests.codes.ok:
                    return bs4.BeautifulSoup(r.text, 'lxml').select('a')[-1].get('href')
                else:
                    return ''
            else:
                return ''
        else:
            return ''
    except:
        return ''
    
def verify_indian_express(tag):
    try:
        parameters = {
            's': tag
        }
        url = "https://indianexpress.com"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('a.m-block-link__anchor')
            return elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verify_the_hindu(tag):
    try:
        parameters = {
            'q': tag,
            'order': 'DESC',
            'sort': 'publishdate'
        }
        url = "https://www.thehindu.com/search"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('a.story-card75x1-text')
            return elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verify_ani(tag):
    try:
        parameters = {
            'query': tag,
        }
        url = "https://www.aninews.in/search"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('a.read-more.full-story')
            return "https://www.aninews.in"+elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verify_hindustan_times(tag):
    try:
        parameters = {
            'q': tag,
        }
        url = "https://www.hindustantimes.com/search"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('.media-body .media-heading  a')
            return elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verify_india_today(tag):
    try:
        url = f"https://www.indiatoday.in/topic/{tag}"
        res = requests.get(url, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('.views-row-odd.itg-search-list  a')
            return elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verify_ndtv(tag):
    try:
        parameters = {
            'searchtext': tag,
        }
        url = "https://www.ndtv.com/search"
        res = requests.get(url, params=parameters, headers=headers, timeout=60)
        if res.status_code == requests.codes.ok:
            ressoup = bs4.BeautifulSoup(res.text, 'lxml')
            elems = ressoup.select('li p a')
            return elems[0].get('href') if len(elems) > 0 else ''
        else:
            return ''
    except:
        return ''
    
def verification_score(tag):
    results =[]
    results.append(verify_google_news(tag))
    results.append(verify_ani(tag))
    results.append(verify_hindustan_times(tag))
    results.append(verify_india_today(tag))
    results.append(verify_indian_express(tag))
    results.append(verify_ndtv(tag))
    results.append(verify_the_hindu(tag))
    score = sum([int(bool(x)) for x in results])*100//7
    return score, results    