import json
import aiohttp

from django.core.cache import cache
from json import JSONDecodeError
from bs4 import BeautifulSoup

from .config import ConfigDict
config = ConfigDict()


def create_word_list(word_file_path: str) -> list:
    """return list of words from your file with english words"""
    with open(word_file_path) as file:
        word_list = file.readlines()
    word_list = [line.rstrip() for line in word_list]
    return word_list


async def get_response(session: aiohttp, url: str, proxy_auth: aiohttp) -> object:
    proxy_address = config["proxy_address"]
    if proxy_auth:
        async with session.get(url=url, proxy=f"http://{proxy_address}",
                               proxy_auth=proxy_auth) as response:
            response_text = await response.text()
    else:
        async with session.get(url=url) as response:
            response_text = await response.text()
    return response_text


def parse_search_page(response_text) -> dict:
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

    for section_post in result_of_section['contents']:
        try:
            if "videoRenderer" in section_post:
                video_information = section_post['videoRenderer']
            elif "backgroundPromoRenderer" in section_post:
                continue
            elif "didYouMeanRenderer" in section_post or \
                    "showingResultsForRenderer" in section_post or \
                    "infoPanelContainerRenderer" in section_post:
                continue
            elif "searchPyvRenderer" in section_post:
                continue
            else:
                continue
            video_link_type = video_information['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']

        except KeyError as ex:
            continue

        try:
            if video_information['viewCountText']['simpleText'] == "No views":
                video_views = 0
            else:
                ###
                video_views = int(
                    video_information['viewCountText']['simpleText'].split(' ')[0].replace(u'\xa0', u'').replace(',', ''))
                ###

        except JSONDecodeError as ex:
            continue
        except ValueError as ex:
            continue

        if video_views < config["min_view_count"]:
            continue

        if 'shorts' in video_link_type:
            if not config["shorts"]:
                continue
        ###
        video_link = f"https://www.youtube.com/embed{video_link_type.split('&')[0]}"
        if cache.get(video_link):
            continue
        else:
            cache.set(video_link, 1, timeout=3600)
        ###

        try:
            ###
            video_channel_link = 'https://www.youtube.com' + str(
                video_information['longBylineText']['runs'][0]['navigationEndpoint']['commandMetadata'][
                    'webCommandMetadata']['url'])
            ###
        except:
            continue

        parsed_video_data.append([video_link, video_views, video_channel_link])
    return {"success": True, "parsed_videos": parsed_video_data}


def parse_data_by_channel_subs(response_text):
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
        is_monetization = False

    if count < config["max_sub_count"]:
        return {"success": True, "checked_data": [int(count), is_monetization]}
    else:
        return {"success": False}
