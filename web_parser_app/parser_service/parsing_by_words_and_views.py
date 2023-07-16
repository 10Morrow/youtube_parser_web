import asyncio
import aiohttp

from config import ConfigDict
from services import parse_search_page, get_response

youtube_data = [] # list of lists with video_link, video_views, video_channel_link
config = ConfigDict()


async def add_page_data_to_list(session: aiohttp.ClientSession, word: str, proxy_auth: aiohttp.BasicAuth = None) -> None:
	"""parse search page and add to youtube_data list relevant video"""
	global youtube_data
	mode = config["mode"]
	url = f"https://www.youtube.com/results?search_query={word}&sp={mode}"

	try:
		response_text = await get_response(session, url, proxy_auth)
	except aiohttp.TooManyRedirects:
		return None
	except aiohttp.ClientPayloadError:
		return None

	if response_text:
		video_data_list = parse_search_page(response_text)
		if video_data_list["success"]:
			youtube_data += video_data_list["parsed_videos"]


async def gather_search_page_data(word_list: list) -> list:
	"""creating a list of tasks, return list with data from search page"""
	global youtube_data
	session = aiohttp.ClientSession()
	try:

		if config["proxy_login"] and config["proxy_pass"]:
			proxy_auth = aiohttp.BasicAuth(config["proxy_login"], config["proxy_pass"])
			tasks = [asyncio.create_task(add_page_data_to_list(session, word, proxy_auth)) for word
					in word_list]
		else:
			tasks = [asyncio.create_task(add_page_data_to_list(session, word)) for word
					in word_list]

		await asyncio.gather(*tasks)
		await session.close()

		return youtube_data
	except Exception as ex:
		await session.close()
		try:
			return youtube_data
		except:
			return []
