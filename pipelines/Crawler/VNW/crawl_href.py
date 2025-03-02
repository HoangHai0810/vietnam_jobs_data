from utils import *
import argparse
import pandas as pd

if __name__ == '__main__':

    domain = "https://www.vietnamworks.com/tim-viec-lam/tim-tat-ca-viec-lam"
    driver = configure_driver()
    hrefs = []

    cnt, starting_page = get_href_crawler_args()
    curr_page = starting_page
    result = pd.DataFrame(columns=['id','page','href'])
    while(True):
        try:
            driver.get(f"https://www.vietnamworks.com/viec-lam?" + f"&page={curr_page}")
            time.sleep(2)

            if check_if_ending(driver):
                break
            # Goi ham truot con tro chuot xuong cuoi trang
            smooth_scroll(driver, 5)
            scroll_page(driver)

            hrefs = get_hrefs(driver)
            result = pd.concat([result, pd.DataFrame({'id':range(len(hrefs)), 'page':curr_page, 'href':hrefs})], axis=0, ignore_index=True)
            write_log(f"Appended {len(hrefs)} hrefs from page {curr_page}\n", ".\\Data\\Vietnamworks\\logs", 'vnw-log')
            if curr_page == cnt+starting_page-1:
                break
            curr_page += 1
        except KeyboardInterrupt:
            break
    result['id'] = np.arange(len(result))     
    save_df_to_csv(result, ".\\Data\\Vietnamworks\\hrefs", 'vnw')
    write_log(f"Crawling href complete, total: {len(result)}", ".\\Data\\Vietnamworks\\logs", 'vnw-href-log')