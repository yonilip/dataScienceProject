# -*- coding: utf-8 -*-

import sqlite3
import platform
import os
import shutil
import lda
import datetime
import get_search
import sys
import pprint

DEBUG = False

dst_path = ""
urls_table_dict = {}
keyword_search_terms_table_dict = {}
visits_table_dict = {}
id_set = set()
epsilon = 0.01


def is_english(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def get_history_file():
    global dst_path
    try:
        windows_path_to_history = os.path.join(r"C:\Users", os.getlogin(),
                                               r"AppData\Local\Google\Chrome\User Data\Default\History")
        mac_path_to_history = os.path.join(os.path.expanduser("~"),
                                           r"Library/Application Support/Google/Chrome/Default/History")
        linux_path_to_history = os.path.join(os.path.expanduser("~"), r".config/google-chrome/Default/History")

        if platform.system() == 'Windows':
            path = windows_path_to_history
        elif platform.system() == 'Darwin':
            path = mac_path_to_history
        elif platform.system() == 'Linux':
            path = linux_path_to_history
        else:
            raise Exception

        dst_path = "./History"
        shutil.copy(path, dst_path)
    except:
        exit_if_err()
    return dst_path


def get_tables_as_dicts(history_file_path):
    conn = sqlite3.connect(history_file_path)
    c = conn.cursor()

    keywords_table = "select * from keyword_search_terms"
    '''
    keyword_search_terms(keyword_id INTEGER NOT NULL,
                         url_id INTEGER NOT NULL,
                         lower_term LONGVARCHAR NOT NULL,
                         term LONGVARCHAR NOT NULL);
    '''
    c.execute(keywords_table)
    keywords_tuple_list = c.fetchall()
    print(keywords_tuple_list)
    for t in keywords_tuple_list:
        if is_english(t[3]):  # removes non english queries
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
        if is_english(t[1]):
            urls_table_dict[t[0]] = t[1:]  # id is key, value is rest of tuple

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
        visits_table_dict[t[1]] = t[2:]


def exit_if_err(sizeable_obj=None):
    if not sizeable_obj or len(sizeable_obj) == 0:
        print("You have to search the web using google chrome to get results!")
        sys.exit(1)
    return


def get_todays_topics():
    results = []
    for id, val in keyword_search_terms_table_dict.iteritems():
        last_visit_time = urls_table_dict[id][4]
        # google chromes timestamp is counted in nanosecs from 1,1,1601....
        time_obj = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
        # TODO reset this to today
        if time_obj.strftime('%Y-%m-%d') == datetime.datetime.now().strftime('%Y-%m-%d'):
        # if time_obj.strftime('%Y-%m-%d') == '2017-02-23':
            results.append(val[1])

    exit_if_err(results)

    model = lda.lda(results)
    topics = model.show_topics(formatted=False)
    return topics
    # TODO return stemmed words to original word (maybe find word that contained them


def get_interesting_queries(todays_topics):
    list_of_q = []
    for topic_tuple in todays_topics:
        query = topic_tuple[1][0][0]
        for next_topic in topic_tuple[1]:
            # make sure that not adding itself and that simliarity is over 5%
            if (not next_topic is topic_tuple[1][0]) and (topic_tuple[1][0][1] - next_topic[1]) < epsilon:
                query += " " + next_topic[0]
        if query not in list_of_q:
            list_of_q.append(query)
            # TODO make sure that not creating query that was searched today
    return list_of_q

def main_func():
    try:
        history_file_path = get_history_file()
        get_tables_as_dicts(history_file_path)
        todays_topics = get_todays_topics()
        list_of_q = get_interesting_queries(todays_topics)
        search_res = get_search.search_web(list_of_q, urls_table_dict)
        # print search_res

        os.remove(history_file_path)


        if DEBUG:
            pprint.pprint(todays_topics, indent=4)
            pprint.pprint(list_of_q, indent=4)
            pprint.pprint(search_res, indent=4)
        return search_res
    except:
        exit_if_err()

if __name__ == '__main__':
    main_func()