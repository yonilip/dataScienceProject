from google import search

def search_web(search_list, visited_urls):
    search_dict = {}
    for query in search_list:
        i = 0
        url_list = []
        for url in search(query, stop=10):
            if url not in visited_urls:
                url_list.append(url)
                i += 1
                if i == 3:
                    break
        search_dict[query] = url_list
    return search_dict


# res = search_web(["green tea", "baseball"])
# print(res)
