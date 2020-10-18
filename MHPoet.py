import numpy as np 
import requests
from bs4 import BeautifulSoup

def extractPoem(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    p1 = soup.find_all('div', class_='m1')
    p2 = soup.find_all('div', class_='m2')
    poem = [(p1[i].get_text(), p2[i].get_text()) for i in range(len(p1))]
    return poem

def extractPoems(url_format, no):
    urls = [url_format + str(i) for i in range(1, no + 1)]
    poems = []
    for i in range(len(urls)):
        poems.append(extractPoem(urls[i]))
        print('\b'*20, f'{i+1} done...', end='')
    return poems


def writeToFile(file, poems):
    with open(file, 'w') as f:
        for poem in poems:
            for beyt in poem:
                f.write(beyt[0] + ' E' + '\n')
                f.write(beyt[1] + ' E' + '\n')
    print('Printed in file :)')

def readFromFile(file):
    with open(file, encoding="utf8") as f:
        poems = f.readlines()
    poems = [i.replace('\u200c', ' ') for i in poems]
    return poems

def preprocessWords(unique_words):
    bad_words = []
    for word in unique_words:
        if len(word)==1:
            bad_words.append(word)
    for word in bad_words:
        unique_words.remove(word)
    return unique_words

def count(poems, *words):
    seq = ' '.join(words)
    c = 0
    for poem in poems:
        if poem.find(seq + ' ')!=-1:
            c+=1
    return c

def guessNext(text, N, top, unique_words, poems):
    text_words = text.split()
    last_text_words = text_words[-N+1:]
    no_of_words = len(unique_words)
    probs = dict()
    for word in unique_words:
        temp = last_text_words+ [word]
        num = count(poems, *temp)
        den = count(poems, *last_text_words)
        probs[word] = np.log((num+1) / (den+no_of_words))

    largests = sorted(probs, key=probs.get, reverse=True)[:top]
    new_texts = [text + ' ' + largests[i] for i in range(len(largests))]
    return new_texts, largests

def guessNexts(text_list, N, top, unique_words, poems):
    new_texts = []
    for text in text_list:
        nt, _ = guessNext(text, N, top, unique_words, poems)
        new_texts.extend(nt)
    return new_texts

def completeIt(text_list, N, no, top, unique_words, poems):
    texts = text_list[:]
    for i in range(no):
        texts = guessNexts(texts, N, top, unique_words, poems)
        print(i, texts)
    return texts

if __name__=='__main__':
    hafez_url_format = "http://ganjoor.net/hafez/ghazal/sh"
    saadi_url_format = "https://ganjoor.net/saadi/divan/ghazals/sh"
    #poems = extractPoems(hafez_url_format, 495)
    #writeToFile('Hafez.txt', poems)
    #poems = extractPoems(saadi_url_format, 637)
    #writeToFile('Saadi.txt', poems)
    poems = []
    poems.extend(readFromFile('Saadi.txt'))
    poems.extend(readFromFile('Hafez.txt'))
    unique_words = set([word for poem in poems for word in poem.split()])
    print('Len: ', len(unique_words))
    unique_words = preprocessWords(unique_words)
    print('Len: ', len(unique_words))
    no_of_words = len(unique_words)
    text = 'دوش وقت سحر'
    N = 2
    #new_texts, l = guessNext(text, 2)
    #print(guessNexts([text], 2))
    print(completeIt([text], 2, 4, 2, unique_words, poems))
