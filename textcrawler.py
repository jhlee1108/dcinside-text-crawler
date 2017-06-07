from bs4 import BeautifulSoup
import urllib.request
import time
import random
import sys

class TextCrawler:
    def __init__(self, gall_name, page_number):
        self.list_url = 'http://gall.dcinside.com/board/lists/?id=' + gall_name 
        self.view_url = 'http://gall.dcinside.com/board/view/?id=' + gall_name
        self.page_number = page_number

    def crawl(self):
        page = 1
        f = open('data.txt', 'w')

        while page <= self.page_number:
            url_open = urllib.request.urlopen(self.list_url + 
                                                '&page=' + str(page))
            soup = BeautifulSoup(url_open, 'html.parser', 
                                    from_encoding='utf-8')
            notice_list = soup.findAll('td', {'class':'t_notice'})
            subject_list = soup.findAll('td', {'class':'t_subject'})

            for i in range(0, len(notice_list)):    # 공지사항 제거
                if notice_list[0].text == '공지':
                    notice_list.pop(0)
                    subject_list.pop(0)

            for subject in subject_list:    # 제목 저장
                f.write(subject.text + '\n')
                print(subject.text)

            random_number = random.randrange(1,5)
            print('%d page subject crawling complete. %d sec sleep...'\
                    % (page, random_number))
            time.sleep(random_number)

            for notice in notice_list:
                url_open = urllib.request.urlopen(self.view_url +
                                                    '&no=' + str(notice.text) +
                                                    '&page=' + str(page))
                soup = BeautifulSoup(url_open, 'html.parser', 
                                        from_encoding='utf-8')
                content = soup.find('div', {'class':'s_write'})
                content = content.table.tr.td.text

                f.write(content + '\n')     # 본문 저장
                print(content)

                random_number = random.randrange(1,5)
                print('%s content crawling complete. %d sec sleep...'\
                        % (notice.text, random_number))
                time.sleep(random_number)

            page += 1

        f.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('python3 wordcloud.py [GALL_NAME] [PAGE_NUMBER]')
        sys.exit()

    gall_name = str(sys.argv[1])
    page_number = int(sys.argv[2])
    t = TextCrawler(gall_name, page_number)
    t.crawl()
    
