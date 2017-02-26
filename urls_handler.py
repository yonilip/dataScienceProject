from google import search
import webbrowser
import os

from topic_extract import main_func

queries_list = main_func()
url_list = []


def search_urls(queries):
    for query in queries:
        urls_for_query = []
        for url in search(query, stop=10):
            if len(urls_for_query) >= 3:
                break
            urls_for_query.append(url)
        url_list.append(urls_for_query)

if __name__ == '__main__':
    search_urls(queries_list)

    for query_list in url_list:
        for url in query_list:
            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

    os.system("taskkill /F /IM chrome.exe")


