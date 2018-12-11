import matplotlib.pyplot as plt
import csv
'exec(%matplotlib inline)'
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

BASE_URL = 'https://www.coursera.org'


def crawl_course_page(course_page_url):
    try:
        course_page_html = urlopen(course_page_url)
    except HTTPError as e:
        print("Possible 404 page not found error " + course_page_url)
    else:
        course_page_soup = BeautifulSoup(course_page_html, 'html.parser')
        type(course_page_soup)
        course_title = course_page_soup.find('h1',
                                             attrs={
                                                 'class': 'H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz'})
        course_title = course_title.text
        course_ratings = course_page_soup.find('div',
                                               attrs={'class': 'P_gjs17i-o_O-weightNormal_s9jwp5-o_O-fontBody_56f0wi'})
        course_ratings = course_ratings.text
        description = course_page_soup.find('div', attrs={'class': 'content-inner'})
        description = description.text
        instructors = course_page_soup.find_all('div', attrs={'class': 'Instructors'})
        print("Title: ", course_title)
        authors = ''
        for instructor in instructors:
            names = instructor.find_all('h3', attrs={'class': 'H2_1pmnvep-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2'})
            for name in names:
                authors += name.text + ','

        with open(r'courses.csv', 'a', newline='') as csvfile:
            fieldnames = ['title', 'authors', 'ratings', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'title': course_title,
                'authors': authors,
                'ratings': course_ratings,
                'description': description
            })


def crawl_main_page(page_no):
    url = 'https://www.coursera.org/courses?languages=en&query=&indices[test_all_products][page]=' + str(
        page_no) + '&indices[test_all_products][configure][clickAnalytics]=true&indices[test_all_products][configure][hitsPerPage]=' + str(
        page_no) + '&configure[clickAnalytics]=true'
    print(url)
    html = urlopen(url)

    soup = BeautifulSoup(html, 'html.parser')
    type(soup)

    courses = soup.find_all('a', attrs={'class': 'rc-DesktopSearchCard'})
    for link in courses:
        crawl_course_page(BASE_URL + link['href'])


i = 1

while i <= 100:
    crawl_main_page(i)
    i += 1
