from time import sleep
from bs4 import BeautifulSoup
from random import randint
import requests

data = []

def get_data():
    for i in range (1,11):
        response = requests.get(f"http://quotes.toscrape.com/page/{i}/")
        soup = BeautifulSoup(response.text,"html.parser")
        sleep(0.5)
        divs = soup.find_all(class_="quote")
        for div in divs:
            quote = div.span.contents[0]
            author = div.small.contents[0]
            url = div.find("a")["href"]
            data.append([quote,author,url])
    pick()

def pick():
    num = randint(1,len(data))
    q = data.pop(num)
    print("Here's a quote: \n")
    print(f"{q[0]}\n")
    game(q)

def author(q):
    name = q[1].split(" ")
    n = []
    n.append(len(name[len(name)-1]))    #last name lenght (index 0)
    n.append(name[len(name)-1][0])      #first letter last name (index 1)
    return n

def game(q):
    count = 4
    while count > 0:
        answer = input(f"Who said this? Guesses remaining: {count}.")
        if (answer.lower() != q[1].lower()):
            if (count == 4):
                get_bio(q)
                count -= 1
            elif (count == 3):
                n = author(q)
                print(f"Here's a hint: The author's last name is {n[0]} letters long")
                count -= 1
            elif (count == 2):
                print(f"Here's a hint: The author's first letter of his last name is {n[1]}")
                count-=1
            else:
                print(f"It was {q[1]}")
                again()
                break
        else:
            print("You guessed correctly! Congratulations!")
            again()
            break
    else:
        again()

def again():
    reboot = input("Would you like to play again? (y/n)")
    if reboot.lower() == "y":
        pick()
    elif reboot.lower() == "n":
        print("OK! See you next time")
    else:
        again()

def get_bio(q):
    response = requests.get(f"http://quotes.toscrape.com{q[2]}")
    soup = BeautifulSoup(response.text,"html.parser")
    p = soup.find_all("p")[1]
    date = p.find(class_="author-born-date")
    location = p.find(class_="author-born-location")
    print(f"Here's a hint: The author was born on {date.contents[0]} {location.contents[0]}")


get_data()






