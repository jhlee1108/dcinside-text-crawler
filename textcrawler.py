from bs4 import BeautifulSoup
import urllib.request
import time
import random

class TextCrawler:
    def __init__(self, gall_name, page_number):
        self.list_url = 'http://gall.dcinside.com/board/lists/?id=' + gall_name 
        self.view_url = 'http://gall.dcinside.com/board/view/?id=' + gall_name
        self.page_number = page_number

    def crawl(self):
        page = 1
        text = ''

        while page <= self.page_number:
            url_open = urllib.request.urlopen(self.list_url + 
                                                '&page=' + str(page))
            soup = BeautifulSoup(url_open, 'html.parser', 
                                    from_encoding='utf-8')
            notice_list = soup.findAll('td', {'class':'t_notice'})
            subject_list = soup.findAll('td', {'class':'t_subject'})

            for i in range(0, len(notice_list)):
                if notice_list[0].text == '공지':
                    notice_list.pop(0)
                    subject_list.pop(0)

            for subject in subject_list:
                print(subject.text)
                text += subject.text + '\n'

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

                print(content)
                text += content + '\n'

                random_number = random.randrange(1,5)
                print('%s content crawling complete. %d sec sleep...'\
                        % (notice.text, random_number))
                time.sleep(random_number)

            page += 1

        return text
