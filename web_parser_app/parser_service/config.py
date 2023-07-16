from models import PersonSettings

YOUTUBE_FILTERS = {
	"today_four_minuts_plus_by_views_count" : "CAMSBggCEAEYAw%253D%253D",
	"today_by_views_count" : "CAMSBAgCEAE%253D",
	"week_four_minuts_plus_by_views_count" : "CAMSBAgDGAM%253D",
}


class ConfigDict:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)
			cls._instance.state = {}
		return cls._instance

	def __getitem__(self, key):
		return self.state[key]

	def __setitem__(self, key, value):
		self.state[key] = value


def get_config_data(identifier, current_user):
	settings = PersonSettings.objects.get(user=current_user)
	config_data = ConfigDict()

	config_data["words_file"] = settings.words_file
	config_data["min_view_count"] = settings.min_view_count
	config_data["shorts"] = settings.shorts
	config_data["max_sub_count"] = settings.max_sub_count
	config_data["proxy_address"] = settings.proxy_address
	config_data["proxy_login"] = settings.proxy_login
	config_data["proxy_pass"] = settings.proxy_pass
	config_data["mode"] = settings.mode

	config_data["identifier"] = identifier

	return config_data
