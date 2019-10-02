import random

import flask
from flask import request, jsonify
from bs4 import BeautifulSoup
import urllib.request
import re
import requests
from itertools import cycle
from fake_useragent import UserAgent, FakeUserAgentError

#find: Get a single match result
#findall: Return all matched results


app = flask.Flask(__name__)
app.config["DEBUG"] = True



# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

url2 = "https://en.wikipedia.org/wiki/Artificial_intelligence"
url = "https://www.dataquest.io/blog/web-scraping-beautifulsoup/"
URL = "https://cashchanger.co/singapore"


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/currency/all', methods=['GET'])
def api_currencies():
    try:
        page = urllib.request.urlopen(url) # conntect to website
    except:
        print("An error occured.")
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    regex = re.compile('^tocsection-')
    content_lis = soup.find_all('li', attrs={'class': regex})
    print(content_lis)
    content = []
    for li in content_lis:
        content.append(li.getText().split('\n')[0])
    print(content)
    return jsonify(content)

    # # Getting the keywords section
    # keyword_section = soup.find(class_="keywords-section")
    # # Same as: soup.select("div.article-wrapper grid row div.keywords-section")
    #
    # # Getting a list of all keywords which are inserted into a keywords list in line 7.
    # keywords_raw = keyword_section.find_all(class_="keyword")
    # keyword_list = [word.get_text() for word in keywords_raw]

@app.route('/api/v1/resources/currency/sell/bestrate/all', methods=['GET'])
def sell_bestrate():
    try:
        # page = urllib.request.urlopen(url) # conntect to website
        r = requests.get(URL)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    best_rate_container = soup.find('div', class_='container bestrate-container')
    # print(best_rate_container.prettify)
    currencies = []

    # bestrate_table = best_rate_container.find_all('div', class_='bestrate')
    for row in best_rate_container.find_all('div', class_='bestrate'):
        print(row.prettify)
        currency = {}
        currency['country_currency'] = row.find('span', class_='country-currency').text
        currency['currency_code'] = row.find('span', class_='currency-code float-left').text
        currency['rate'] = row.find('div', class_='text-big text-center').text
        currencies.append(currency)
    # print(bestrate_table.prettify)


    # regex = re.compile('^tocsection-')
    #     # content_lis = soup.find_all('li', attrs={'class': regex})
    #     # print(content_lis)
    #     # content = []
    #     # for li in content_lis:
    #     #     content.append(li.getText().split('\n')[0])
    #     # print(content)
    #     # return jsonify(content)
    return jsonify(currencies)
    # return 'nyan'

    # # Getting the keywords section
    # keyword_section = soup.find(class_="keywords-section")
    # # Same as: soup.select("div.article-wrapper grid row div.keywords-section")
    #
    # # Getting a list of all keywords which are inserted into a keywords list in line 7.
    # keywords_raw = keyword_section.find_all(class_="keyword")
    # keyword_list = [word.get_text() for word in keywords_raw]


@app.route('/api/v1/resources/currency/buy/bestrate/all', methods=['GET'])
def buy_bestrate():
    # Usage example
    proxies_pool, headers_pool = create_pools()
    current_proxy = next(proxies_pool)
    current_headers = next(headers_pool)
    try:
        # page = urllib.request.urlopen(url) # connect to website
        # r = requests.get(URL)

        # Introduce the proxy and headers in the GET request
        with requests.Session() as req:
            r = req.get(URL, proxies={"http": current_proxy, "https": current_proxy}, headers=current_headers,
                           timeout=30)
    except:
        print("An error occured.")
        # soup = BeautifulSoup(page, 'html.parser')
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify) # gives the visual representation of the parse tree created from the raw HTML content.
    best_rate_container = soup.find('div', class_='container bestrate-container')
    # print(best_rate_container.prettify)
    currencies = []

    # bestrate_table = best_rate_container.find_all('div', class_='bestrate')
    for row in best_rate_container.find_all('div', class_='bestrate'):
        print(row.prettify)
        currency = {}
        currency['country_currency'] = row.find('span', class_='country-currency').text
        currency['currency_code'] = row.find('span', class_='currency-code float-left').text
        currency['rate'] = row.find('div', class_='text-big text-center').text
        currencies.append(currency)
    return jsonify(currencies)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

# Generate the pools
def create_pools():
    url = 'https://www.sslproxies.org/'

    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    with requests.Session() as res:
        proxies_page = res.get(url)

    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))

    headers = [random_header() for ind in range(len(proxies))]  # list of headers, same length as the proxies list

    # This transforms the list into itertools.cycle object (an iterator) that we can run
    # through using the next() function in lines 16-17.
    proxies_pool = cycle(proxies)
    headers_pool = cycle(headers)
    return proxies_pool, headers_pool



def random_header(logger):
    # Create a dict of accept headers for each user-agent.
    accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}

    # Get a random user-agent. We used Chrome and Firefox user agents.
    # Take a look at fake-useragent project's page to see all other options - https://pypi.org/project/fake-useragent/
    try:
        # Getting a user agent using the fake_useragent package
        ua = UserAgent()
        if random.random() > 0.5:
            random_user_agent = ua.chrome
        else:
            random_user_agent = ua.firefox

    # In case there's a problem with fake-useragent package, we still want the scraper to function
    # so there's a list of user-agents that we created and swap to another user agent.
    # Be aware of the fact that this list should be updated from time to time.
    # List of user agents can be found here - https://developers.whatismybrowser.com/.
    except FakeUserAgentError  as error:
        # Save a message into a logs file. See more details below in the post.
        logger.error(
            "FakeUserAgent didn't work. Generating headers from the pre-defined set of headers. error: {}".format(
                error))
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
        random_user_agent = random.choice(user_agents)

    # Create the headers dict. It's important to match between the user-agent and the accept headers as seen in line 35
    finally:
        valid_accept = accepts['Firefox'] if random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
        headers = {"User-Agent": random_user_agent,
                   "Accept": valid_accept}
    return headers






if __name__ == '__main__':
    app.run()
