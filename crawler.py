# -*- coding: utf-8 -*-

import urlparse
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import datetime

class Crawler:

    def __init__(self, infomation):
        # self.GuestID = id 
        self.start_url = infomation['start_url']
        self.uri_pattern = infomation['uri_pattern']
        self.day_pattern = infomation['day_pattern']
        self.page_pattern = infomation['page_pattern']
        self.list_contents_containner = infomation['list_contents_containner']


        self.title_pattern = infomation['title_pattern']
        self.contents_pattern = infomation['contents_pattern']
        self.article_time_pattern = infomation['article_time_pattern']

        self.urls = []
        self.visited_urls = []

        self.articles = []

        self.count_parsed_article = 0

        self.urls.append(self.start_url)
        self.visited_urls.append(self.start_url)
        
    def __del__(self):  
         pass

    # 기사 URL 크롤링 
    def article_url_crawling(self):
        htmlText = urllib2.urlopen(self.start_url).read()
        soup = BeautifulSoup(htmlText)

        #기사를 담고있는 container가 있으면 해당 container 추출 (다른 기사 제거 하기 위함 )
        if  self.list_contents_containner is not None:
            soup = soup.find(id=self.list_contents_containner)
  

        for tag in soup.findAll('a', href = True):
            tag['href'] = urlparse.urljoin(self.start_url, tag.get('href'))
            article__url = [m.group(0) for m in re.finditer(self.uri_pattern, tag['href'])]      
            if len(article__url) != 0 and tag['href'] not in self.visited_urls:
                self.visited_urls.append(tag['href'])
    

    # 기사 내용 파싱 
    def article_parsing(self):
        article = {}
        for index in range(self.count_parsed_article + 3, len(self.visited_urls)):
            print self.visited_urls[index]
            htmlText = urllib2.urlopen(self.visited_urls[index]).read()
           
            soup = BeautifulSoup(htmlText)

            article['title'] = soup.find(self.title_pattern['tag'], attrs=self.title_pattern['attrs']).text.strip()
            
            #기사 content에 제거할 element가 있으면 제거 
            if 'remove_tags' in self.contents_pattern:
                article['content'] = soup.find(self.contents_pattern['tag'], attrs=self.contents_pattern['attrs'])
                for remove_tag in self.contents_pattern['remove_tags']:
                    for remove in article['content'].findAll(remove_tag['tag'], attrs=remove_tag['attrs']):
                        remove.extract()
                article['content'] = article['content'].text.strip()
            else:
                article['content'] = soup.find(self.contents_pattern['tag'], attrs=self.contents_pattern['attrs']).text.strip()    

            #기사 time 추출 
            if 'sub_contents' in self.article_time_pattern:
                article['time'] = soup.find_all(self.article_time_pattern['tag'], attrs=self.article_time_pattern['attrs'])[0].find(self.article_time_pattern['sub_contents']['tag']).text.strip()
            else:
                article['time'] = soup.find_all(self.article_time_pattern['tag'], attrs=self.article_time_pattern['attrs'])[0].text.strip()

            print article['time']
            print article['title']
            print article['content']
            print ''
    



naver = Crawler({
    'start_url' : 'http://sports.news.naver.com/sports/index.nhn?category=kbo&ctg=news',
    'uri_pattern' : 'http://sports.news.naver.com/sports/index.nhn\?category=kbo&ctg=news&mod=read&office_id=[^&]+&article_id=',
    'page_pattern' : '&page=2',
    'day_pattern' : '&date=20140717',
    'list_contents_containner' : None,
    'title_pattern' : {
        'tag' : 'h4',
        'attrs' : {
            'class' : 'tit_article'
        }
    }, 
    'contents_pattern' : {
        'tag' : 'div',
        'attrs' : {
            'id' : 'naver_news_20080201_div'
        },
        'remove_tags' : [{
            'tag' : 'div',
            'attrs' : {
                'class' : 'link_news'
            }}, {
            'tag' : 'table',
            'attrs' : {

            }} 
        ]
    }, 
    'article_time_pattern' : {
        'tag' : 'span',
        'attrs' : {
            'class' : 'time'
        }
    } 
})

naver.article_url_crawling()
naver.article_parsing()

nate = Crawler({
    'start_url' : 'http://sports.news.nate.com/baseball/recent',
    'uri_pattern' : 'http://sports.news.nate.com/view/.*\?mid=.*',
    'page_pattern' : '&page=2',
    'day_pattern' : '&date=20140717',
    'list_contents_containner' : 'cntArea',
    'title_pattern' : {
        'tag' : 'h3',
        'attrs' : {
            'class' : 'viewTite'
        }
    }, 
    'contents_pattern' : {
        'tag' : 'div',
        'attrs' : {
            'id' : 'articleContetns'
        },
        'remove_tags' : [{
            'tag' : 'script',
            'attrs' : {
            }}, {
            'tag' : 'div',
            'attrs' : {
                'id' : 'newsmediaBanner'
            }} 
        ]
    }, 
    'article_time_pattern' : {
        'tag' : 'dl',
        'attrs' : {
            'class' : 'articleInfo' # need
        },
        'sub_contents' : {
            'tag' : 'em',
        }
    } 
})
nate.article_url_crawling()
nate.article_parsing()


#다음은 기사를 동적으로 불러와서 포기.
"""
daum = Crawler({
  'start_url' : 'http://sports.media.daum.net/sports/baseball/news/breaking/',
  'uri_pattern' : 'http://sports.media.daum.net/v/[^?]*',
  'page_pattern' : '&page=2',
  'day_pattern' : '&date=20140717',
  'list_contents_containner' : 'cMain'
  })

daum.craw()
"""