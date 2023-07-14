import sys
import asyncio
import time
from config import PARTS_COUNT, WORDS_FILE, MODE
from services import create_word_list, write_data
from parsing_by_words_and_views import gather_data
from final_parsing_by_sub_count import finish_data


def main():
	"""start full process of parsing"""

	word_list = create_word_list(WORDS_FILE)
	mode = MODE
	count = 1
	for i in range(PARTS_COUNT, len(word_list), PARTS_COUNT):
		t1 = time.time()
		part_of_words = word_list[i-PARTS_COUNT:i]

		if sys.platform == 'win32':
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
		else:
			asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

		relevant_video_data = asyncio.run(gather_data(part_of_words, mode))
		if relevant_video_data:
			finished_data_list = asyncio.run(finish_data(relevant_video_data))
		else:
			continue

		if finished_data_list:
			write_data(finished_data_list, count)
			t2 = time.time()
			count += 1