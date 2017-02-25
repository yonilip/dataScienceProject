from google import search

def cookie_func(url):
    return True


def search_web(search_list):
    search_dict = {}
    # query = 'green tea'
    for query in search_list:
        i = 0
        url_list = []
        for url in search(query, stop=10):
            if cookie_func(url):
                url_list.append(url)
                i += 1
                if i == 3:
                    print(i)
                    break
        search_dict[query] = url_list
    return search_dict


res = search_web(["green tea", "baseball"])
print(res)
