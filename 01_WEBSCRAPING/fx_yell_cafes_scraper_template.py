from requests_html import HTMLSession
import datetime

session = HTMLSession()

all_cafes = []
all_page_links = []

def generate_page_links() -> None:
    """
    This function generates the page links which then can be leveraged to scrape properties data using 'scrape_content()' function
    """
    
    for pgno in range(1,11):
        
        page_link = f"https://www.yell.com/ucs/UcsSearchAction.do?keywords=Cafes+And+Coffee+Shops&location=london&scrambleSeed=850094717&pageNum={pgno}"
        all_page_links.append(page_link)
    return

def scrape_content(page_url: str) -> None:
    """
    This function scrapes individual properties from the given page URL.
    Args:
        url (str): page URL to scrape properties
    Returns:
        It returns nothing but adds individual properties into the 'all_shops' list
    """
    
    print(f'Scraping properties from: {page_url}')
    
    current_utc_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%d-%b-%Y %H:%M:%S')
    
    response = session.get(page_url)
    content = response.html.find('div.col-sm-24 article')

    for shop in content:
        
        shop_name = shop.find('h2.businessCapsule--name', first=True).text
        shop_business = shop.find('span.businessCapsule--classification', first=True).text
        
        try:
            business_website = shop.find('a[data-tracking="WL:CLOSED"]', first=True).attrs.get('href')
        except:
            try:
                business_website = shop.find('a[data-tracking="FLE:WL:CLOSED"]', first=True).attrs.get('href')
            except:
                business_website = ''
        
        try:
            telephone_number = shop.find('span.business--telephoneNumber', first=True).text
        except:
            telephone_number = ''
        
        try:
            street_address = shop.find('span[itemprop="address"] span[itemprop="streetAddress"]', first=True).text
        except:
            street_address = ''
        
        address_state = shop.find('span[itemprop="address"] span[itemprop="addressLocality"]', first=True).text
        
        try:
            postal_code = shop.find('span[itemprop="address"] span[itemprop="postalCode"]', first=True).text
        except:
            postal_code = ''
        
        star_rating = shop.find('span.starRating', first=True).attrs.get('title')
        
        shop_details = {
            "shop_name": shop_name,
            "shop_business": shop_business,
            "shop_website": business_website,
            "telephone_number": telephone_number,
            "street_address": street_address,
            "state": address_state,
            "postal_code": postal_code,
            "star_rating": star_rating,
            "last_updated_at_UTC": current_utc_timestamp
        }
        
        all_cafes.append(shop_details)
    return

if __name__ == '__main__':
    
    generate_page_links()
    
    print('\n')
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    
    page_url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords=Cafes+And+Coffee+Shops&location=london&scrambleSeed=850094717&pageNum=3'
    
    scrape_content(page_url)
    
    print('\n')
    print(f'Total properties scraped: {len(all_cafes)}')
    print('\n')
    print(all_cafes)