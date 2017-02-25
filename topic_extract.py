# -*- coding: utf-8 -*-

import sqlite3
import platform
import os
import sys
import shutil

import datetime


dst_path = ""
urls_table_dict = {}
keyword_search_terms_table_dict = {}
visits_table_dict = {}
id_set = set()

def is_english(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def get_history_file():
    global dst_path
    windows_path_to_history = os.path.join(r"C:\Users", os.getlogin(), r"AppData\Local\Google\Chrome\User Data\Default\History")
    mac_path_to_history = os.path.join(os.path.expanduser("~"), r"Library/Application Support/Google/Chrome/Default/History")
    linux_path_to_history = os.path.join(os.path.expanduser("~"), r".config/google-chrome/Default/History")

    path = ""
    if platform.system() == 'Windows':
        path = windows_path_to_history
    elif platform.system() == 'Darwin':
        path = mac_path_to_history
    elif platform.system() == 'Linux':
        path = linux_path_to_history
    # else:
    #     print "What kind of weird system are you using?"
    #     sys.exit(1)

    # dst_path = os.path.join("./", os.path.dirname(path))
    dst_path = "./History"
    shutil.copy(path, dst_path)
    return dst_path


def get_tables_as_dicts(history_file_path):
    conn = sqlite3.connect(history_file_path)
    c = conn.cursor()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # q = "select term from urls, keyword_search_terms " \
    #     "where id=url_id and " \
    #     "instr(datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), " \
    #     "'unixepoch'), {date}) > 0".format(date=date)
    q = "select term from urls, keyword_search_terms " \
        "where id=url_id and " \
        "instr(datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), " \
        "'unixepoch'), {date}) > 0".format(date=date)

    keywords_table = "select * from keyword_search_terms"
    '''
    keyword_search_terms(keyword_id INTEGER NOT NULL,
                         url_id INTEGER NOT NULL,
                         lower_term LONGVARCHAR NOT NULL,
                         term LONGVARCHAR NOT NULL);
    '''
    c.execute(keywords_table)
    keywords_tuple_list = c.fetchall()
    for t in keywords_tuple_list:
        if is_english(t[3]):  # removes non english queries
            id_set.add(t[1])
            keyword_search_terms_table_dict[t[1]] = t[2:]


    url_table = "select * from urls"
    c.execute(url_table)
    urls_tuple_list = c.fetchall()

    '''
    urls(id INTEGER PRIMARY KEY,
         url LONGVARCHAR,
         title LONGVARCHAR,
         visit_count INTEGER DEFAULT 0 NOT NULL,
         typed_count INTEGER DEFAULT 0 NOT NULL,
         last_visit_time INTEGER NOT NULL,
         hidden INTEGER DEFAULT 0 NOT NULL,
         favicon_id INTEGER DEFAULT 0 NOT NULL)
    '''
    for t in urls_tuple_list:
        if t[0] in id_set:
            urls_table_dict[t[0]] = t[1:]  # id is key, value is rest of tuple
    # queries_list = list(c.fetchall())



    visits_table = "select * from visits"
    '''visits(id INTEGER PRIMARY KEY,
              url INTEGER NOT NULL,
              visit_time INTEGER NOT NULL,
              from_visit INTEGER,
              transition INTEGER DEFAULT 0 NOT NULL,
              segment_id INTEGER,
              visit_duration INTEGER DEFAULT 0 NOT NULL);
    '''
    c.execute(visits_table)
    for t in c.fetchall():
        if t[1] in id_set:
            visits_table_dict[t[1]] = t[2:]


def get_todays_topics():
    for id, val in keyword_search_terms_table_dict.iteritems():
        last_visit_time = urls_table_dict[id][4]
        time_obj = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
        if time_obj.strftime('%Y-%m-%d') == datetime.datetime.now().strftime('%Y-%m-%d'):
            print val[1]



if __name__ == '__main__':
    history_file_path = get_history_file()
    get_tables_as_dicts(history_file_path)
    get_todays_topics()

    os.remove(history_file_path)
