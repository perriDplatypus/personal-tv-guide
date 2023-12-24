# inspired by https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
# import json
import random

import modules.shield
import modules.html
import modules.runtime
import modules.genre


# Open main window
driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')

driver.maximize_window()
# driver.implicitly_driwait(1.0)
# main_window_handle = driver.window_handles[0]


# Wait for user to sign in
input("Sign in, and then press Enter to continue...")


# Scroll to the end of the page
items_in_list = 60
pages = items_in_list // 20
i = 0
for i in range(pages):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)


# Get name, episode number/title, left in season, main show link from main watchlist
show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-show-episode"]')
# len(show_cards)

i = 0
show_card_all_links = []
show_card_full_text = []
for i in range(len(show_cards)):
    show_card_all_links.append(show_cards[i].find_elements(By.TAG_NAME,'a'))
    show_card_full_text.append(show_cards[i].text)

i = 0
show_main_link = []
for i in range(len(show_card_all_links)):
    show_main_link.append(show_card_all_links[i][0].get_dom_attribute('href'))

i = 0
show_name = []
episode_number = []
episode_left_in_season = []
episode_title = []
for i in range(len(show_card_full_text)):
    this_show_elements = show_card_full_text[i].split(sep='\n')
    # show_name.append(this_show_elements[1])
    # episode_number.append(this_show_elements[2])
    # episode_left_in_season.append(this_show_elements[3])
    # episode_title.append(this_show_elements[4])
    show_name.append(this_show_elements[1])
    episode_number.append(this_show_elements[2])
    if this_show_elements[3][0] == "+":
        episode_left_in_season.append(this_show_elements[3])
        episode_title.append(this_show_elements[4])
    else:
        episode_left_in_season.append('')
        episode_title.append(this_show_elements[3])

# show_name
# episode_number
# episode_left_in_season
# episode_title
# show_main_link


# Get genres, runtime, age rating from show pages
# episode_length = []
j = 0
show_genres = []
show_runtime = []
show_age_rating = []
for j in range(len(show_main_link)):
    # from https://www.browserstack.com/guide/selenium-wait-for-page-to-load
    driver.get('https://www.justwatch.com' + show_main_link[j])
    try:
        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="title-info title-info"]'))
        )
    finally:
        time.sleep(1)

    # length_xpath = '//div[@class="detail-infos__value"]'
    # length_text = driver.find_elements(By.XPATH, length_xpath)[3].text
    # length_minutes = int(length_text.split("min")[0])

    # episode_length.append(length_minutes + 15 - (length_minutes % 15))

    title_info = driver.find_element(By.XPATH, '//div[@class="title-info title-info"]')
    detail_infos = title_info.find_elements(By.XPATH,'//div[@class="detail-infos"]')

    k = 0
    title_info_heading = []
    title_info_value = []
    shows_dict = []
    for k in range(len(detail_infos)):
        text = detail_infos[k].text
        if len(text) > 0:
            text_split = text.split(sep='\n')
            split_head = text_split[0]
            split_value = text_split[1]
            title_info_heading.append(split_head)
            title_info_value.append(split_value)

    shows_dict = dict(zip(title_info_heading,title_info_value))
    show_genres.append(shows_dict.get('GENRES'))
    show_runtime.append(shows_dict.get('RUNTIME'))
    show_age_rating.append(shows_dict.get('AGE RATING'))
    
    # show_genres
    # show_runtime
    # show_age_rating


# driver.close()
driver.quit()


# Pull elements together

# show_name
# episode_number
# episode_left_in_season
# episode_title
# show_genres
# show_runtime
# show_age_rating

# data_tuples = list(zip(titles_list[0:],episode_headings_list[0:],episode_names_list[0:],episode_urls[0:],episode_length[0:]))
data_tuples = list(zip(show_name,episode_number,episode_left_in_season,episode_title,show_genres,show_runtime,show_age_rating))
# sorted(data_tuples)

# df = pd.DataFrame(data_tuples, columns=['Show Name','Episode Number','Episodes Remaining','Episode Title','Genres','Runtime','Age Rating'])
# html_string = df.to_html()


# jsonObject = json.dumps(data_tuples)
# print(jsonObject)
# print(type(jsonObject))

# sample = df.sample(2)




# save my work
import modules.data_bin_convert
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples = modules.data_bin_convert.bin_to_data()


# sample = data_tuples

random.shuffle(data_tuples)
# sample




genre_reality, remainder = modules.genre.split_by_genre(data_tuples,"Reality TV")
genre_documentary, remainder = modules.genre.split_by_genre(remainder,"Documentary")
genre_romance, remainder = modules.genre.split_by_genre(remainder,"Romance")
genre_family, remainder = modules.genre.split_by_genre(remainder,"Kids & Family")
genre_comedy, remainder = modules.genre.split_by_genre(remainder,"Comedy")
genre_drama, remainder = modules.genre.split_by_genre(remainder,"Drama")



when_to_start = 11
hours_to_print = 4

html_handle = open("C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\out.html",'+w')
html_handle.write(modules.html.generate_html_start())
html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))



# genre_list = genre_reality
# genre_list = [('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG'),('Making It2', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '144min', 'TV-PG'),('Making It3', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '1244min', 'TV-PG')]

# genre = 'Reality TV'
# hours = 4

html_handle.write(modules.html.generate_html_genre_tds(genre_reality,'Reality TV',hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_documentary, 'Documentary', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_romance, 'Romance', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_family, 'Kids & Family', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_comedy, 'Comedy', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_drama, 'Drama', hours_to_print))

html_handle.write(modules.html.generate_html_end())

html_handle.close()
