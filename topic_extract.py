import sqlite3
import platform
import os
import sys
from datetime import datetime


def get_history_file():
    windows_path_to_history = os.path.join(r"C:\Users", os.getlogin(), r"AppData\Local\Google\Chrome\User Data\Default\History")
    mac_path_to_history = r"~/Library/Application\ Support/Google/Chrome/Default/History"
    linux_path_to_history = r"~/.config/google-chrome/Default/History"

    if platform.system() == 'Windows':
        return windows_path_to_history
    elif platform.system() == 'Darwin':
        return mac_path_to_history
    elif platform.system() == 'Linux':
        return linux_path_to_history
    else:
        print "What kind of weird system are you using?"
        sys.exit(1)


def get_todays_queries(history_file_path):
    conn = sqlite3.connect(history_file_path)
    c = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d')
    q = "select term from urls, keyword_search_terms " \
        "where id=url_id and " \
        "instr(datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), " \
        "'unixepoch'), {date}) > 0".format(date=date)
    c.execute(q)
    queries_list = list(c.fetchall())


if __name__ == '__main__':
    history_file_path = get_history_file()
    queries_list = get_todays_queries(history_file_path)