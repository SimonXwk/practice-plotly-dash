import os


def find_raw_csv_path(filename):
	folder = __file__.rsplit(os.sep, 1)[0]
	return os.path.join(folder, 'csv_raw', filename)
