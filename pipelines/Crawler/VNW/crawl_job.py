from utils import *
import argparse
import pandas as pd

if __name__ == '__main__':

    hrefs_path, storing_dir, count, starting_href_id = get_job_crawler_args()
    driver = configure_driver()
    
    hrefs = pd.read_csv(hrefs_path)
    hrefs = hrefs['href'].values
    if count > len(hrefs):
        count = len(hrefs)
    hrefs = hrefs[starting_href_id:starting_href_id+count]
    jobs = []
    #zoom_out(5)
    #time.sleep(5)
    cnt = 0
    for href in hrefs:
        try:
            cnt += 1
            print(cnt)
            driver.get(href)
            if cnt == 1:
                zoom_out(7)
            #write_log(f"Crawling jobs: {href}", ".\\Data\\Vietnamworks\\logs", 'vnw-job-log')

        except KeyboardInterrupt:
            break
        try:
            job = crawl_data(driver)
            #print(len(job))
            jobs.append(job)
        except KeyboardInterrupt:
            break
        except:
            continue

    
    df = pd.DataFrame(jobs, columns=['id', 'crawling_date', 'company_name', 'company_size', 'job_title', 'salary','deadline',\
    'views','region','description','requirements','benefits','posted_date', 'level', 'profession',\
    'skills', 'field', 'resume_language', 'min_yoe', 'nationality',\
    'min_edu_level','gender', 'desired_age', 'marital_status', 'num_of_recruits', 'working_day', 'working_hours', 'location', 'keywords'])
    df['id'] = np.arange(1, len(df)+1)

    save_df_to_csv(df, storing_dir, 'vnw_jobs')
    write_log(f"Crawling jobs complete, total: {len(jobs)}", ".\\Data\\Vietnamworks\\logs", 'vnw-job-log')
    driver.quit()
   