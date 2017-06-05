from textcrawler import TextCrawler
from collections import Counter
from konlpy.tag import Hannanum
import sys
import random
import pytagcloud
import webbrowser

def get_text(gall_name, page_number):
    t = TextCrawler(gall_name, page_number)
    text = t.crawl()

    return text

def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)

    r  = lambda: random.randint(0, 255)
    color = lambda: (r(), r(), r())

    return [{'color': color(), 'tag': n, 'size': c*multiplier}\
                for n, c in count.most_common(ntags)]

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
