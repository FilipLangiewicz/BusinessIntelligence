import zipfile

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd


def create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass,
                                 scheme='http', plugin_path=None):
    """Creates a proxy authentication extension for Chrome."""
    if plugin_path is None:
        plugin_path = 'proxy_auth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "{scheme}",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details, callbackFn) {{
            callbackFn({{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }});
        }},
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def scrape(URL, USER, PASS):
    """Setup driver and scrape TripAdvisor page."""
    from seleniumwire import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options

    # 🔧 Create extension
    plugin_file = create_proxy_auth_extension(
        proxy_host="pr.oxylabs.io",
        proxy_port=7777,
        proxy_user=USER,
        proxy_pass=PASS
    )

    chrome_options = Options()
    chrome_options.add_extension(plugin_file)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((
            By.XPATH,
            '//*[contains(@data-test-attribute, "all-results-section")]'
        ))
    )

    try:
        driver.find_element(
            By.XPATH,
            '//button[contains(text(), "Accept")]'
        ).click()
    except NoSuchElementException:
        pass

    driver.find_element(
        By.XPATH,
        '//button//*[contains(text(), "Show more")]'
    ).click()
    driver.implicitly_wait(5)

    page_source = driver.page_source
    driver.quit()
    return page_source


def parse(html):
    """Parse HTML and extract restaurant data."""
    soup = BeautifulSoup(html, 'html.parser')
    listings = []

    for listing in soup.select('[data-test-attribute="location-results-card"]'):
        title = listing.select_one('.FGwzt')
        rating = listing.select_one('title')
        reviews = listing.select_one('.yyzcQ')
        href = listing.select_one('a').get('href')

        listings.append({
            'title': title.text,
            'rating': float(rating.text.split(' ')[0]),
            'reviews': int(reviews.text.replace(',', '')),
            'link': 'https://www.tripadvisor.com' + href
        })

    return listings


def save_to_csv(data, filename):
    """Save data to CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    URL = 'https://www.tripadvisor.com/Search?q=restaurants+in+new+york'
    USER = 'jakombajn'
    PASS = ''

    html = scrape(URL, USER, PASS)
    results = parse(html)
    save_to_csv(results, 'restaurants.csv')