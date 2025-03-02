import time
import json
import pandas as pd
import argparse
import time
import re
import datetime
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
import pyautogui
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def scroll_until_button_found(driver, css_selector, scroll_pause_time=1.5, scroll_amount=300):
    def is_button_present():
        try:
            return driver.find_element(By.CSS_SELECTOR, css_selector).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    time.sleep(2)

    count = 0
    while True:
        count+=1
        # Kiểm tra xem button đã xuất hiện chưa
        if is_button_present():
            #print(f"Đã tìm thấy button với selector: {css_selector}")
            return True

        # Cuộn trang
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(scroll_pause_time)
        
        # Đợi để trang load
        try:
            WebDriverWait(driver, scroll_pause_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print("Timeout khi đợi trang load")

        # Kiểm tra xem đã cuộn đến cuối trang chưa
        if count == 10:
            print("Đã cuộn đến cuối trang mà không tìm thấy button.")
            return False
    

def get_href_crawler_args():
    parser = argparse.ArgumentParser(description="Href Crawler Tool")
    parser.add_argument("-c", "--count", type=int, default=500,
                        help="Number of items to crawl (default: 10)")
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="Starting page number (default: 1)")

    args = parser.parse_args()
    cnt = args.count
    starting_page = args.start
    return cnt, starting_page

def get_job_crawler_args():
    parser = argparse.ArgumentParser(description="Job Crawler Tool")

    parser.add_argument("-f", "--file", type=str, default=".\\Data\\Vietnamworks\\hrefs\\vnw-20240923-123926.csv",
                        help="Href file to crawl")
    parser.add_argument("-d", "--dir", type=str, default=".\\Data\\Vietnamworks\\jobs",
                        help="Directory to save job data")
    parser.add_argument("-c", "--count", type=int, default=10000,
                        help="Number of items to crawl (default: 10000)")
    parser.add_argument("-s", "--start", type=int, default=0,
                        help="Starting href number (default: 0)")

    args = parser.parse_args()
    file = args.file
    dir = args.dir
    cnt = args.count
    starting_href_id = args.start
    return file, dir, cnt, starting_href_id

def configure_driver():
    webdriver_path = ".\\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def check_if_ending(driver):
    try:
        check = driver.find_element(By.CSS_SELECTOR, "h2[class='title']").text
        #print("Not find")
        if check:
            return 1
        return 0
    except:
        return 0
import pyautogui    
def zoom_out(count = 5):
    # Đợi một chút để đảm bảo trình duyệt đã mở hoàn toàn
    time.sleep(0.5)
    
    # Thực hiện thao tác Ctrl và dấu trừ 3 lần để thu nhỏ
    for _ in range(count):
        pyautogui.hotkey('ctrl', '-')
        time.sleep(0.5)

def zoom_in(count = 5):
    # Đợi một chút để đảm bảo trình duyệt đã mở hoàn toàn
    time.sleep(2)
    
    for _ in range(count):
        pyautogui.hotkey('ctrl', '+')
        time.sleep(0.5)

def scroll_page(driver):
    # Cuộn đến cuối trang
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Đợi một chút để trang load thêm nội dung (nếu có)
    time.sleep(0.5)

def smooth_scroll(driver, scroll_count=5):

    actions = ActionChains(driver)
    for _ in range(scroll_count):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)
        #print("Scroll: ", _)

def write_log(data, folder_path, prefix = 'vnw-log'):
    cur_datetime = datetime.datetime.now()
    cur_datetime = cur_datetime.strftime('%Y%m%d')
    file_name = f'{prefix}-{cur_datetime}.csv'
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'a') as f:
        f.write(f"{data}\n")
        f.write(f"{datetime.datetime.now()}\n")
        f.write("-"*50)
        f.write("\n")
        print(f"Write log to {file_path}")

def save_df_to_csv(df, folder_path, prefix = 'vnw'):
    cur_datetime = datetime.datetime.now()
    cur_datetime = cur_datetime.strftime('%Y%m%d-%H%M%S')
    file_name = f'{prefix}-{cur_datetime}.csv'
    file_path = os.path.join(folder_path, file_name)

    df.to_csv(file_path, index=False)
    print(f"Save data to {file_path}")

def get_job_info(driver, title):
    try:
        data = driver.find_element(By.XPATH, f"//label[text()='{title}']/following-sibling::p").text
    except:
        data = ''
    return data

def crawl_data(driver):

    time.sleep(2)
    smooth_scroll(driver, 2)

    # Ten cong viec
    ten_cv = driver.find_element(By.CSS_SELECTOR, "h1[class='sc-df6f4dcb-0 bsKseP'][name='title']").text
    
    # Ten cong ty
    try:
        ten_cty = driver.find_element(By.CSS_SELECTOR, "div[class='sc-37577279-3 drWnZq'] > a[name='label']").text
    except:
        ten_cty = ''

    #  Kich thuoc cong ty
    try:
        kich_thuoc = driver.find_elements(By.CSS_SELECTOR, "div[class='sc-37577279-0 joYsyf'] span[class='sc-df6f4dcb-0 bgAmOO']")
        for d in kich_thuoc:
            if 'nhân viên' in d.text.lower():
                # Tìm kiếm mẫu số-số hoặc số trước từ "nhân viên"
                match = re.search(r'(\d+(?:-\d+)?)\s*nhân viên', d.text.lower())
                if match:
                    kich_thuoc = match.group(1)
    except:
        kich_thuoc = ''
    # Luong
    luong = driver.find_element(By.CSS_SELECTOR, "span[class='sc-df6f4dcb-0 iOaLcj'][name='label']").text
    
    # thoi han, luot xem va khu vuc
    panel = driver.find_element(By.CSS_SELECTOR, "div[id='vnwLayout__row'][class='sc-b8164b97-0 dnguBj']")
    thlxkv = panel.find_elements(By.CSS_SELECTOR, "div[id='vnwLayout__col']")
    thoi_han = thlxkv[0].text
    luot_xem = thlxkv[1].text
    khu_vuc = thlxkv[2].text

    # Mo ta va yeu cau cong viec
    mo_ta = ''
    yeu_cau = ''
    # Click de mo rong tab mo ta cong 
    # try:
    #     mo_ta_cv_btn = "button[type='button'][aria-label='Xem đầy đủ mô tả công việc']"
    #     #if scroll_until_button_found(driver, mo_ta_cv_btn):
    #     driver.find_element(By.CSS_SELECTOR, mo_ta_cv_btn).click()
    #     # Mo ta cong viec
    #     mo_ta = driver.find_elements(By.CSS_SELECTOR, "div[class='sc-4913d170-6 hlTVkb']")[0].text
    #     # Yeu cau cong viec
    #     yeu_cau = driver.find_elements(By.CSS_SELECTOR, "div[class='sc-4913d170-6 hlTVkb']")[1].text
    # except:
    #     pass
    
    # Phuc loi
    phuc_loi = []
    phuc_loi_panel = driver.find_element(By.CSS_SELECTOR, "div[class='sc-c683181c-0 fRBraR']")
    # Check co button "Xem thêm" hay khoong?
    try:
        xt_btn = phuc_loi_panel.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label='Xem thêm']")
        xt_btn.click()
        time.sleep(1)
    except:
        #print('Da hien thi toan bo phuc loi')
        pass
    # Lay tat ca cac phuc loi
    try:
        phuc_loi_list = phuc_loi_panel.find_elements(By.CSS_SELECTOR, "div[class='sc-c683181c-0 fRBraR'] div[id='vnwLayout__col']")
        for pl in phuc_loi_list:
            ten_phuc_loi = pl.find_element(By.CSS_SELECTOR, "div[class='sc-c683181c-3 crDTPK']").text
            chi_tiet_phuc_loi = pl.find_element(By.CSS_SELECTOR, "div[class='sc-c683181c-5 dhUHMk']").text
            phuc_loi_dict = {ten_phuc_loi:chi_tiet_phuc_loi}
            phuc_loi.append(phuc_loi_dict)
    except:
        #print('Khong co phuc loi')
        phuc_loi = []
        pass
    #Thong tin viec lam
    # Click vao xem them thong tin viec lam
    xem_them_vl_panel = driver.find_element(By.CSS_SELECTOR, "div[class='sc-7bf5461f-0 dHvFzj']")
    
    if scroll_until_button_found(driver, "div[class='sc-7bf5461f-0 dHvFzj'] button[type='button'][aria-label='Xem thêm']",1.5,200):
        button_xem_them_viec_lam = xem_them_vl_panel.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label='Xem thêm']")
        button_xem_them_viec_lam.click()
        #print('Da click vao xem them')
   
    ngay_dang = get_job_info(xem_them_vl_panel, "NGÀY ĐĂNG")
    cap_bac = get_job_info(xem_them_vl_panel, "CẤP BẬC")
    nganh_nghe = get_job_info(xem_them_vl_panel, "NGÀNH NGHỀ")
    ky_nang = get_job_info(xem_them_vl_panel, "KỸ NĂNG")
    linh_vuc = get_job_info(xem_them_vl_panel, "LĨNH VỰC")
    ngon_ngu_trinh_bay_ho_so = get_job_info(xem_them_vl_panel, "NGÔN NGỮ TRÌNH BÀY HỒ SƠ")
    so_nam_kinh_nghiem_toi_thieu = get_job_info(xem_them_vl_panel, "SỐ NĂM KINH NGHIỆM TỐI THIỂU")
    quoc_tich = get_job_info(xem_them_vl_panel, "QUỐC TỊCH")
    trinh_do_hoc_van_toi_thieu = get_job_info(xem_them_vl_panel, "TRÌNH ĐỘ HỌC VẤN TỐI THIỂU")
    gioi_tinh = get_job_info(xem_them_vl_panel, "GIỚI TÍNH")
    do_tuoi_mong_muon = get_job_info(xem_them_vl_panel, "ĐỘ TUỔI MONG MUỐN")
    tinh_trang_hon_nhan = get_job_info(xem_them_vl_panel, "TÌNH TRẠNG HÔN NHÂN")
    so_luong_tuyen_dung = get_job_info(xem_them_vl_panel, "SỐ LƯỢNG TUYỂN DỤNG")
    ngay_lam_viec = get_job_info(xem_them_vl_panel, "NGÀY LÀM VIỆC")
    gio_lam_viec = get_job_info(xem_them_vl_panel, "GIỜ LÀM VIỆC")
    # Dia diem lam viec:
    try:
        dia_diem = driver.find_element(By.CSS_SELECTOR, "div[class='sc-a137b890-0 bAqPjv'] p[class='sc-df6f4dcb-0 ioTZSy']").text
    except:
        dia_diem = ''
    #Tu khoa
    tu_khoa = []
    try:
        tu_khoa_panel = driver.find_element(By.CSS_SELECTOR, "div[class='sc-a3652268-0 jlHmIg'] div[class='sc-a3652268-3 esrWRf']")
        tu_khoa_list = tu_khoa_panel.find_elements(By.CSS_SELECTOR, "button")
        for tu in tu_khoa_list:
            tu_khoa.append(tu.text)
    except:
        pass
    write_log("Done", ".\\Data\\Vietnamworks\\logs", 'vnw-log')
    print("Done ", len(tu_khoa))
    return [1, datetime.datetime.now().strftime('%Y%m%d'), ten_cty, kich_thuoc, ten_cv, luong, thoi_han, luot_xem, khu_vuc, mo_ta, yeu_cau, phuc_loi, ngay_dang, cap_bac, nganh_nghe, ky_nang, linh_vuc, \
    ngon_ngu_trinh_bay_ho_so, so_nam_kinh_nghiem_toi_thieu, quoc_tich, trinh_do_hoc_van_toi_thieu, gioi_tinh, do_tuoi_mong_muon,\
    tinh_trang_hon_nhan, so_luong_tuyen_dung, ngay_lam_viec, gio_lam_viec,dia_diem, tu_khoa]

def get_hrefs(driver):
    hrefs = []
    job_ele = driver.find_elements(By.CSS_SELECTOR, "a[class='img_job_card']")
    for ele in job_ele:
        hrefs.append(ele.get_attribute('href'))
    return hrefs


