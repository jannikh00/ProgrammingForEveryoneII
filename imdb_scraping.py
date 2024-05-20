# Importing
import requests
from bs4 import BeautifulSoup
import time
import re

# Setting start time
start_time = time.time()

# regex for fetching movie urls
regex_1 = "t_[1-9][0-9]?[0-9]?$"

# regex for fetching urls to movie information
regex_2 = "/title/tt[0-9]+/fullcredits/cast"

# Supporting function to filter urls
def filter_url(url, regex_input):
    regex = regex_input
    search = re.search(regex, url)
    if search:
        return True
    else:
        return False

############################### FUNCTION ###############################
def scrape_imdb():

    # bypass the scraping protections of site
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # URL of the IMDB Top 250 movies page
    url1 = "https://www.imdb.com/chart/top/"

    # Send a GET request to the page
    r1 = requests.get(url1, headers=headers)

    # parse html content
    soup1 = BeautifulSoup(r1.text, 'html.parser')

    # finding all <a> tags that contain hrefs to sub pages
    links1 = soup1.find_all('a')

    # list with all created urls, unfiltered
    all_urls = []

    # list with 250 urls to pages with information about actors
    needed_urls = []

    # body for url to movie information
    url2 = "https://www.imdb.com"

    # creating urls to single movies and putting them into all_urls list
    for link in links1:
        href = link.get('href')
        if href and not href.startswith('http'):
            href = url2 + href
            href_2 = href[:38] + 'h' + href[38:]
            all_urls.append(href_2)

    # count for testing purpose
    # cnt = 1
            
    # putting just all needed 250 urls in needed_urls list, based on all_urls list
    for x in all_urls:
        if filter_url(x, regex_1):
            needed_urls.append(x)
            # Testing:
            # print(f"{cnt}. {x}\n")
            # cnt += 1

    # actors dict
    actors = {}

    # list with urls leading to single movie information
    movie_info_urls = []

    # string that gets appended on the single movie url to receive url to the cast information
    appending_string = "fullcredits/cast?ref_=tt_ov_st_sm"

    # filling movie_info_urls list with newly created links to movie info
    for i in needed_urls:
        tmp = i[:37]
        movie_info_urls.append(tmp + appending_string)
    
    '''
    # Testing the results of the loop from above
    cnt = 1
    for i in movie_info_urls:
        print(f"{cnt}. {i}\n")
        cnt += 1
    '''

    # actors dict
    actors = {}

    # filling actors dict with data
    for movie_info in movie_info_urls:
        # Send a GET request to the single movie information urls
        r2 = requests.get(movie_info, headers=headers)

        # parse html content
        soup2 = BeautifulSoup(r2.text, 'html.parser')

        # finding part of the html that conatains the cast list
        links2 = soup2.find_all(class_='cast_list')

        # list with the name of every actor in this movie and the name of the character they play, resetting list with every iteration
        names = []

        # finding all <a>-tags in current 'cast_list' element, pulling out the text of the tags that actually have names
        for i in links2:
            names.extend([a.get_text(strip=True) for a in i.find_all('a') if a.get_text(strip=True)])

        # list with the name of every actor in this movie, leaving out the names of the characters they play
        names2 = names[::2]

        # counting aappearances
        for i in names2:
            if i in actors:
                actors[i] += 1
            else:
                actors[i] = 1  


    # cnt = 1
    # for i in names2:
    #     print(f"{cnt}. {i}")
    #     cnt += 1

    print("\n")

    # new list, sorted and cut down to the top ten
    top_10_items = sorted(actors.items(), key=lambda x: x[1], reverse=True)[:10]

    # printing list
    print("Top ten actors according to appearances in the top 250 movies list:\n")

    cnt = 1
    for key, value in top_10_items:
        print(f"{cnt}. {key}: {value}")
        cnt += 1

'''
    cnt =1
    for key, value in actors.items():
        print(f"{cnt}. {key}: {value}")
        cnt += 1

    #print(links2)

    all_a_tags = [a for element in links2 for a in element.find_all('a')]
    filtered_a_tags = [a for a in all_a_tags if a['href'].startswith('/name/nm')]
    new_list = []

    for a in all_a_tags:
        print(a)

    for a in filtered_a_tags:
        print(a)

    # cutting @ appearances
    new_list = [s.split("\"", 1)[1] if "\"" in s else s for s in filtered_a_tags]

    for i in new_list:

        # html String
        html_content = i

        # BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # try to find an element
        element = soup.find('a')  # no <a>-Tag in html_content

        # check if element was found
        if element is not None:
            print(element.text)
        else:
            print("No Element found.")
'''

'''
    for movie_info in movie_info_urls:
        # Send a GET request to the single movie information urls
        r2 = requests.get(movie_info, headers=headers)

        # parse html content
        soup2 = BeautifulSoup(r2.text, 'html.parser')

        # finding part of the html that conatains the cast list
        links2 = soup2.find_all(class_='cast_list')

        # list with the name of every actor in this movie and the name of the character they play, resetting list with every iteration
        names = []

        # finding all <a>-tags in current 'cast_list' element, pulling out the text of the tags that actually have names
        for i in links2:
            names.extend([a.get_text(strip=True) for a in i.find_all('a') if a.get_text(strip=True)])

        # list with the name of every actor in this movie, leaving out the names of the characters they play
        names2 = names[::2]

        for i in names2:
            if i in actors:
                actors[i] += 1
            else:
                actors[i] = 1

    # cnt = 1
    # for i in names2:
    #     print(f"{cnt}. {i}")
    #     cnt += 1

    print("\n")

    top_10_items = sorted(actors.items(), key=lambda x: x[1], reverse=True)[:10]

    cnt = 1
    for key, value in top_10_items:
        print(f"{cnt}. {key}: {value}")
        cnt += 1
'''
'''
    # liste = []

    # for i in links2:
    #     p_text = soup2.find('a').text
    #     liste.append(p_text)

    # print(liste)

###################
    # for i in needed_urls:
    #     # Send a GET request to the page
    #     r2 = requests.get(i, headers=headers)

    #     # parse html content
    #     soup2 = BeautifulSoup(r2.text, 'html.parser')

    #     # finding all <a> tags that contain hrefs to sub pages
    #     links2 = soup2.find_all('a', href = True)

    #     for j in links2:
    #         href = j['href']
    #         if 'fullcredits/cast?' in href:
    #             tmp = url2 + href
    #             movie_info_urls.append(tmp)
    #             break

    # cnt = 1
    # for k in movie_info_urls:
    #     print(f"{cnt}. {k}")
    #     cnt += 1
#################

        #for i in links2:
            #if filter_url(i, regex_2):
                # liste.append(i)
                # print(f"{cnt}. {x}\n")
                # cnt += 1

'''

'''
        cnt = 1
        for i in all_actor_urls:
            print(f"{cnt}. {i}")
            cnt += 1
'''
'''
        # putting all 250 urls in needed_urls list
        for x in all_actor_urls:
            if filter_url(x, regex_2):
                actor_urls.append(x)
                print(f"{cnt}. {x}\n")
                cnt += 1
'''


############################### TESTS ###############################
if __name__ == "__main__":
    example = scrape_imdb()


# Printing Program Time
print("\nProcess finished: %s seconds\n" % (time.time() - start_time))