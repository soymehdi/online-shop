import requests
import sqlite3
from bs4 import BeautifulSoup
import streamlit as st
import json
import st_display
########################

#----database-filling-------------------------------
def database_filling(soup):
    wrappers = soup.find_all("div", class_="s-item__wrapper")

    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                (name TEXT, price TEXT, location TEXT, image TEXT, link TEXT)''')

    for wrapper in wrappers:
        name = wrapper.find("span", role="heading").text.strip()
        price = wrapper.find("span", class_="s-item__price").text.strip()
        loc = wrapper.find('span', class_="s-item__location")
        img = wrapper.find('div', class_="s-item__image-wrapper")
        image = img.find('img')['src']
        
        a_tag = wrapper.find('a', class_='s-item__link')
        link = a_tag['href']

        
        if name and price:
            loc_text = loc.text.strip() if loc else "Location not found" 
            c.execute("INSERT INTO products (name, price, location, image, link) VALUES (?, ?, ?, ?, ?)", (name, price, loc_text, image, link))

    conn.commit()
    conn.close()

#----streamlit--------------------------------
def streamlit_displayer(products):
    st_display.display(products)

#----reading database--------------------------------
def reading__database():
    with sqlite3.connect('products.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        c.close()
        return products

#----main func--------------------------------
def main():
    #----esential--------------------------------
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=samsung+galaxy+s24&_sacat=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    database_filling(soup) #--> summoning database_filling function
    products = reading__database() #--> summoning reading__database function 
    streamlit_displayer(products)

main()