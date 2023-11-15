from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time


def main():
    # 获取配置对象
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('blink-settings=imagesEnabled=false')

    b = webdriver.Chrome(options=options)
    b.get('https://www.xiaohongshu.com/page/topics/61038c5a1a79040001edcb8a?fullscreen=true&naviHidden=yes&xhsshare=CopyLink&appuid=6142c1530000000002024d6a&apptime=1699187449')

    # 定位要删除的元素
    element_to_remove = b.find_element(By.CLASS_NAME, "post-button")
    b.execute_script("arguments[0].remove();", element_to_remove)
    element_to_remove = b.find_element(By.CLASS_NAME, "sticky-bar")
    b.execute_script("arguments[0].remove();", element_to_remove)

    time.sleep(1)
    s_num = 0
    count = 0

    b.find_element(By.CLASS_NAME, 'page-lines').click()
    body = b.find_element(By.TAG_NAME, 'body')

    while 800 > s_num:
        notes = b.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/div[3]/div/div[1]/div[1]').find_elements(By.CLASS_NAME, 'reds-note-card')
        s_num = len(notes)
        body.send_keys(Keys.PAGE_DOWN)

    notes = b.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/div[3]/div/div[1]/div[1]').find_elements(By.CLASS_NAME, 'reds-note-card')
    mainWindow = b.current_window_handle

    with open(r'data\\xhs.txt', 'w', encoding='utf-8') as output_file:

        for link_index in range(s_num):
            try:
                notes[link_index].click()
            except StaleElementReferenceException:
                continue

            time.sleep(2)
            for handle in b.window_handles:
                b.switch_to.window(handle)
                if b.title != '上海CityWalk':
                    break

            if 'RED' not in b.title:
                note = b.find_element(By.XPATH, '//*[@id="detail-desc"]/span[1]')
                note_text = note.text
                output_file.write(f'[{count}] {note_text}\n\n')
                count += 1

            b.close()
            b.switch_to.window(mainWindow)

        print('finish')
        b.quit()


if __name__ == '__main__':
    main()
