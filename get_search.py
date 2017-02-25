from google import search

undesired_sites = ['wikipedia', 'facebook', 'twitter', 'instagram']


def reduce_url_to_base_site(url):
    try:
        url = url[url.index(r'://') + 3:]
        url = url[:url.index(r'/')]
    except Exception as e:
        pass  # uninteresting since not a url
    return url


def get_visited_links(urls_table_dict):
    visited_urls = set()
    for k,v in urls_table_dict.iteritems():
        visited_urls.add(reduce_url_to_base_site(v[0]))
    return visited_urls


def search_web(search_list, urls_table_dict):
    visited_urls = get_visited_links(urls_table_dict)

    search_dict = {}
    for query in search_list:
        i = 0
        url_list = []
        for url in search(query, stop=10):
            if reduce_url_to_base_site(url) not in visited_urls and all(s not in url for s in undesired_sites):
                url_list.append(url)
                i += 1
                if i == 3:
                    break
        search_dict[query] = url_list
    return search_dict


# res = search_web(["green tea", "baseball"])
# print(res)
