# -*- coding: utf-8 -*-

__author__ = 'mactalk'

import urllib, urllib2, HTMLParser

#文章列表
article_list = []
#Instapaper 的用户名和密码
username = "username@gmail.com"
password = "password"

#URL 解析器，继承自 HTMLParser
class UrlParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href' and "post" in value and value not in article_list:
                    article_list.append(value)


#根据文章链接获取response
def fetchData(uri):
    request = urllib2.Request(uri)
    request.add_header('Content-Type','text/html;charset=UTF-8')
    request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/33.0.1750.149 Safari/537.36')
    response = urllib2.urlopen(request)
    return response

def main():
    mp = UrlParser()
    #翻页序列
    pages = range(0, 12)
    for page in pages:
        articles = fetchData("http://yinwang0.lofter.com/?page=" + str(page)).read()
        mp.feed(articles.decode('utf-8'))

    for article in article_list:
        params = urllib.urlencode({'username':username, 'password':password, 'url':article, 'auto-title':1})
        pg = urllib2.urlopen("https://www.instapaper.com/api/add", params)
        if str(pg.getcode()) == "201":
            print u"添加成功：" + article
        elif str(pg.getcode()) == "400":
            print u"错误代码400: 错误的请求，看看是不是参数搞错了，"+ article
        elif str(pg.getcode()) == "403":
            print u"错误代码403：无效的用户名和密码，"+ article
        elif str(pg.getcode()) == "500":
            print u"错误代码500：服务器出了点小问题，请稍后再试，"+ article


if __name__ == '__main__':
    main()