from textcrawler import TextCrawler
from collections import Counter
from konlpy.tag import Hannanum
import sys
import random
import pytagcloud
import webbrowser

def get_text(gall_name, page_number):
    t = TextCrawler(gall_name, page_number)
    t.crawl()

    f = open('data.txt', 'r')
    text = f.read()
    f.close()
    
    return text

def get_tags(text, ntags=50, multiplier=2):
    h = Hannanum()
    nouns = h.nouns(text)
    long_nouns = list()
    for n in nouns:
        if len(n) >= 2: # 길이가 2 이상인 명사만 출력
            long_nouns.append(n)

    count = Counter(long_nouns)
    word_list = list()
    for w in count.most_common(ntags):
        if w[1] >= 10:  # 10번 이상 나온 명사만 출력
            print(w)
            word_list.append(w)

    r  = lambda: random.randint(0, 255)
    color = lambda: (r(), r(), r())

    return [{'color': color(), 'tag': n, 'size': c*multiplier}\
                for n, c in word_list]

def draw_cloud(tags, filename, fontname='Noto Sans CJK', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)

def main():
    if len(sys.argv) != 3:
        print('python3 wordcloud.py [GALL_NAME] [PAGE_NUMBER]')
        sys.exit()

    gall_name = str(sys.argv[1])
    page_number = int(sys.argv[2])

    text = get_text(gall_name, page_number)
    tags = get_tags(text)
    draw_cloud(tags, 'wordcloud.png')

main()
