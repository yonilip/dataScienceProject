# -*- coding: utf-8 -*-

import sqlite3
import platform
import os
import sys
import shutil
import lda
import datetime
import get_search


dst_path = ""
urls_table_dict = {}
keyword_search_terms_table_dict = {}
visits_table_dict = {}
id_set = set()
epsilon = 0.05

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
            # id_set.add(t[1])
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

    # s = set()
    for t in urls_tuple_list:
        # s.add(get_search.reduce_url_to_base_site(t[1]))
        # if t[0] in id_set:
        if is_english(t[1]):
            urls_table_dict[t[0]] = t[1:]  # id is key, value is rest of tuple
    # queries_list = list(c.fetchall())

    # s = set()
    # for k,v in urls_table_dict.iteritems():
    #     s.add(get_search.reduce_url_to_base_site(v[0]))






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
    results = []
    for id, val in keyword_search_terms_table_dict.iteritems():
        last_visit_time = urls_table_dict[id][4]
        time_obj = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
        if time_obj.strftime('%Y-%m-%d') == datetime.datetime.now().strftime('%Y-%m-%d'):
            results.append(val[1])
    model = lda.lda(results)
    topics = model.show_topics(formatted=False)
    return topics
    # TODO return stemmed words to original word (maybe find word that contained them


def get_interesting_queries(todays_topics):
    list_of_q = []
    for topic_tuple in todays_topics:
        query = topic_tuple[1][0][0]
        for next_topic in topic_tuple[1]:
            if (not next_topic is topic_tuple[1][0]) and (topic_tuple[1][0][1] - next_topic[1]) < epsilon:
                query += " " + next_topic[0]
        if query not in list_of_q:
            list_of_q.append(query)
            # TODO make sure that not creating query that was searched today
    return list_of_q


if __name__ == '__main__':
    history_file_path = get_history_file()
    get_tables_as_dicts(history_file_path)
    todays_topics = get_todays_topics()
    list_of_q = get_interesting_queries(todays_topics)
    search_res = get_search.search_web(list_of_q, urls_table_dict)
    print search_res

    os.remove(history_file_path)
