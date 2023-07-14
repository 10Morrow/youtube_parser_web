import os
import datetime
import csv
import json
from json import JSONDecodeError
from bs4 import BeautifulSoup

from config import MIN_VIEW_COUNT, MAX_SUB_COUNT, SHORTS, JSON_FILE, VIDEO_FOLDER_NAME


def json_dump(data):
    with open(JSON_FILE, "w") as write_file:
        json.dump(data, write_file)


def json_load():
    if os.path.isfile(JSON_FILE):
        with open(JSON_FILE, "r") as read_file:
            data = json.load(read_file)
        return data
    else:
        with open(JSON_FILE, "w") as file:
            file.write("{}")
        return {}


def write_data(data_list: list, count: int) -> None:
    """write parsed data in .csv file"""
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    if os.path.isdir(VIDEO_FOLDER_NAME):
        with open(f"{VIDEO_FOLDER_NAME}/videos_{cur_time}_part_{count}.csv", mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow(["Video link", "Views count", "Channel link", "subscribers count", "monetization"])
            file_writer.writerows(data_list)
    else:
        os.makedirs(VIDEO_FOLDER_NAME)
        write_data(data_list, count)


def saver(data):
    with open("video_information", "w") as file:
        json.dump(data, file)


def create_word_list(word_file: str) -> list:
    """return list of words from your file with english words"""
    with open(word_file) as file:
        word_list = file.readlines()
    word_list = [line.rstrip() for line in word_list]
    return word_list


def parse_web_page_by_our_settings(response_text: str) -> dict:
    """parse html code (response_text) of page with videos and return list of needed data"""
    parsed_video_data = []

    soup = BeautifulSoup(response_text, 'lxml')
    search = soup.find_all('body')[0]
    res_search = search.find_all('script')

    try:
        data = "".join(res_search[-6].text.split(' = ')[1:])
        json_result = json.loads(data[:-1])
    except JSONDecodeError:
        return {"success": False}

    try:
        content_result = json_result['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']
        result_of_section = content_result['contents'][0]['itemSectionRenderer']
    except KeyError:
        return {"success": False}

    for i in range(len(result_of_section['contents'])):
        try:
            section_post = result_of_section['contents'][i]
            if "videoRenderer" in section_post:
                video_information = section_post['videoRenderer']
            elif "backgroundPromoRenderer" in section_post:
                return {"success": False}
            elif "didYouMeanRenderer" in section_post or \
                    "showingResultsForRenderer" in section_post or \
                    "infoPanelContainerRenderer" in section_post:
                return {"success": False}
            elif "searchPyvRenderer" in section_post:
                return {"success": False}
            else:
                continue
            video_link_type = video_information['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']

        except KeyError as ex:
            continue

        if 'shorts' in video_link_type:
            if not SHORTS:
                continue

        video_link = f"https://www.youtube.com{video_link_type.split('&')[0]}"

        try:
            if video_information['viewCountText']['simpleText'] == "No views":
                video_views = 0
            else:
                video_views = int(
                    video_information['viewCountText']['simpleText'].split(' ')[0].replace(u'\xa0', u'').replace(',', ''))
        except JSONDecodeError as ex:
            continue
        except ValueError as ex:
            continue

        try:
            video_channel_link = 'https://www.youtube.com' + str(
                video_information['longBylineText']['runs'][0]['navigationEndpoint']['commandMetadata'][
                    'webCommandMetadata']['url'])
        except:
            continue

        if video_views > MIN_VIEW_COUNT:
            parsed_video_data.append([video_link, video_views, video_channel_link])
    return {"success": True, "parsed_videos": parsed_video_data}


def check_channel_link(cache, channel_link):
    if channel_link not in cache:
        return False

    return cache[channel_link]


def save_needed_data(data):
    with open("new_file.txt", "w") as file:
        for i in data:
            file.write("\n\n\n")
            file.write(str(i))


def parse_data_by_channel_subs(response_text, one_list, cache, channel_url):
    soup = BeautifulSoup(response_text, 'lxml')
    search = soup.find_all("script")
    if not search:
        return {"success": False}

    try:
        needed_element = ["var ytInitialData = " in str(block) for block in search]
        index = needed_element.index(True)
        data = str(search[index]).split("var ytInitialData = ")[-1].split(";</script>")[0]
        json_data = json.loads(data)
    except JSONDecodeError as ex:
        return {"success": False}

    try:
        count = json_data["header"]["c4TabbedHeaderRenderer"]["subscriberCountText"]["simpleText"].split(' ')[0]
        if 'K' in count:
            count = count[:-1]
            count = float(count) * 1000
        elif 'M' in count:
            count = count[:-1]
            count = float(count) * 1000000
        else:
            count = int(count)
    except KeyError as ex:
        count = 0

    try:
        is_monetization = json_data["responseContext"]["serviceTrackingParams"][0]["params"][3]["value"]
    except KeyError:
        is_monetization = "unknown"

    cache[channel_url] = [count, is_monetization]
    json_dump(cache)

    if count < MAX_SUB_COUNT:
        one_list.append(int(count))
        one_list.append(is_monetization)
        return {"success": True, "checked_data": one_list}
    else:
        return {"success": False}
