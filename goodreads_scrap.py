## Search on Goodreads filtered by author

import requests
import csv
from bs4 import BeautifulSoup as bs
import urllib
import os

def scrape_and_run(author_name):
    
    page = requests.get("https://www.goodreads.com/shelf/show/" + author_name)
    soup = bs(page.content, 'html.parser')
    titles = soup.find_all('a', class_='bookTitle')
    smallTexts = soup.find_all('span', class_='greyText smallText')


    image_dir = os.getcwd() + "/images/" + author_name

    ## check if the desire author_name path exists
    ## create a new one if it doesnt
    if not os.path.exists(image_dir):
        print(":: creating file")
        os.makedirs(image_dir)

    with open(author_name + '.csv', 'w') as csvfile:
        fieldnames = ['title', 'author']
        csv_write = csv.DictWriter(csvfile, fieldnames=fieldnames)
        books_save = 0
        print(":: writing in file")

        for title, smallText in zip(titles, smallTexts):

            try:
                print(":: searching online")

                ## single book page
                book_page = requests.get("https://www.goodreads.com" + title['href'])
                soup = bs(book_page.content, 'html.parser')
                # get image id
                image = soup.find('img', id='coverImage')

                title_name = title.get_text()

                save_dir = image_dir + "/" + title_name
                urllib.request.urlretrieve(image['src'], save_dir)

                csv_write.writerow({'title': title_name, 'smallText': smallText.get_text()})
                books_save += 1
                ## error handelling for long file names
            except OSError as exc:
                if exc.errno == 36:
                    print(exc)

        print("%d %s books saved." % (books_save, author_name)) # books count feedback



if __name__ == '__main__':

    ## run ifinite till user tells you to stop
    ## to avoid having to compile again and again
    while True:
        author_name = input("Enter the author_name (or quit to stop): ").lower() # input case lowered
        if(author_name == "quit"):
            break
        else:
            scrape_and_run(author_name)