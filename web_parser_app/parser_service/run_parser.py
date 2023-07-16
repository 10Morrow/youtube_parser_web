import sys
import asyncio
from config import get_config_data
from services import create_word_list
from parsing_by_words_and_views import gather_search_page_data
from final_parsing_by_sub_count import gather_chanel_page_data


def main(identifier, current_user):
	"""start full process of parsing"""
	config = get_config_data(identifier, current_user)
	word_list = create_word_list(config["words_file"])
	for i in range(5000, len(word_list), 5000):
		part_of_words = word_list[i-5000:i]

		if sys.platform == 'win32':
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
		else:
			asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

		parsed_data_from_search_page = asyncio.run(gather_search_page_data(part_of_words))
		if parsed_data_from_search_page:
			asyncio.run(gather_chanel_page_data(parsed_data_from_search_page))
