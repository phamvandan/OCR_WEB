import json

path_to_error_dict = 'utils/text_correction/rule_base_dict.json'

data = {
	'chuc': 'chức', 'chũc': 'chúc', 'chưc': 'chức', 'chữc': 'chức',
	'ngảy': 'ngày', 'ngãy': 'ngày', 'cáp': 'cấp', 'cãp': 'cấp', 'ghú': 'chú',
	'buỗi': 'buổi', 'băn': 'bắn', 'uỗng': 'uống', 'q§': 'QS', 'đậi': 'đại',
	'quyđịnh': 'quy định',
}


def create_rule_base():
	with open(path_to_error_dict, 'w+') as f:
		json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	create_rule_base()
