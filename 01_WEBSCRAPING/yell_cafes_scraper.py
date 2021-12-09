import pandas as pd
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from fx_yell_cafes_scraper_template import *

def main() -> None:
    """
    This function loops though each of the page and scrapes all the student properties
    """
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_content, all_page_links)
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    cafes_df = pd.DataFrame(all_cafes)
    cafes_df.to_csv('yell_london_cafes_raw_data.csv', encoding='utf-8', index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "YELL LONDON CAFES SCRAPER"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    start_time = datetime.now()
    
    print('\n\n')
    print(ascii_art_title)
    print('Scraping cafes and coffee shops across London...')
    
    generate_page_links()
    
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('Scraping cafe shop details from each page...')
    print('\n')
    
    main()
    
    end_time = datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All cafes & coffee shops scraped...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total properties collected: {len(all_cafes)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping Completed !!!')