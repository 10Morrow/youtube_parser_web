import asyncio
import aiohttp

from django.core.cache import cache
from main_app.models import Video, VideoGroup
from .services import parse_data_by_channel_subs, get_response
from .config import ConfigDict
config = ConfigDict()


async def check_list_by_sub_count(session: aiohttp.ClientSession, one_list: list,
								proxy_auth: aiohttp.BasicAuth = None) -> None:
	"""check subscribers count on video owner's channel
	and return this data if count more than MAX_SUB_COUNT (from config.py)
	result looks like [video_link, video_views, video_channel_link, subscribers_count, is_monetized]"""

	channel_url, views_count, video_url = one_list
	channel_in_cache = cache.get(channel_url)

	if not channel_in_cache:
		try:
			response_text = get_response(session, channel_url, proxy_auth)
		except aiohttp.TooManyRedirects:
			return None
		except aiohttp.ClientPayloadError:
			return None
		filtered_data = parse_data_by_channel_subs(response_text)
		if filtered_data["success"]:
			count, is_monetization = filtered_data["checked_data"]
			cache.set(channel_url, [count, is_monetization], timeout=3600)
	else:
		sub_count = channel_in_cache[0]
		is_monetization = channel_in_cache[1]
		if sub_count < config["max_sub_count"]:
			video_group = VideoGroup.objects.get(identifier=config["identifier"])
			video = Video.objects.create(video_link=video_url, views=views_count, subscribers=sub_count,
										monetized=is_monetization)
			video_group.videos.add(video)


async def gather_chanel_page_data(youtube_data: list) -> None:
	"""returns the finished parsing result, which has been filtered by channel subscribers"""
	try:
		session = aiohttp.ClientSession()
		if config["proxy_login"] and config["proxy_pass"]:
			proxy_auth = aiohttp.BasicAuth(config["proxy_login"], config["proxy_pass"])
			tasks = [check_list_by_sub_count(session, youtube_link, proxy_auth) for youtube_link
					in youtube_data]
		else:
			tasks = [check_list_by_sub_count(session, youtube_link) for youtube_link
					in youtube_data]

		await asyncio.gather(*tasks)
		await session.close()
	except aiohttp.client_exceptions.ServerDisconnectedError:
		await session.close()
