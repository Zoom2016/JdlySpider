
import requests
from bs4 import BeautifulSoup
import time
import urllib
import re

__author__ = 'zoom'

url_home = 'http://www.jdlingyu.moe/'
url_model = 'http://www.jdlingyu.moe/page/'
header = {'User-Agent':'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 50.0.2661.102 Safari / 537.36'}


def get_all_articles():
    """
    请求所有文章
    :return:文章列表
    """
    #抓取首页内容
    content = requests.get(url_home, headers=header).content

    soup = BeautifulSoup(content, "html.parser")

    #分析总页数
    page_nums = soup.find_all('a', {'class': 'page-numbers'})
    page_max = int(page_nums[-2].get_text().strip())
    print(page_max)
    article_list = list()
    for page_index in range(page_max):
        page_url = url_model + '%d' % (page_index + 1)
        content = requests.get(page_url, headers=header).content
        soup = BeautifulSoup(content,'html.parser')
        post_list = soup.find_all('div', {'class': 'pin-coat'})
        [article_list.append(post.a.get('href')) for post in post_list]
        # time.sleep(2000)

    return article_list

def get_photos_by_article(article_url):
    """
    查找当前文章下所有图片
    :param article_url:
    :return:图片列表（图片名，URL）
    """
    content = requests.get(article_url, headers=header).content

    soup = BeautifulSoup(content, "html.parser")


    main_body = soup.find_all('div', {'class': 'main-body'})[0]
    photos = main_body.p.find_all('a')
    photo_list = list()
    [photo_list.append(p.get('href')) for p in photos]
    return photo_list

    pass


def download_photos(photo, path=None):
    """
    下载图片到本地
    :param photo:图片字典（name,url）
    :param path:本地，默认当前路径下jdly文件夹
    :return:
    """
    photo_name = re.findall(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}.jpg', photo)[0]
    # photo_name = re.findall(r'\(*.jpg)', photo)[0]
    local_path = 'E:\\workspace\\github\\JdlySpider\\jdly_pic\\' + photo_name
    urllib.request.urlretrieve(photo, local_path)
    pass


if __name__ == '__main__':
    # articles = get_all_articles()
    # get_photos_by_article('http://www.jdlingyu.moe/27164/')
    # download_photos('http://www.jdlingyu.moe/wp-content/uploads/2016/02/2017-03-30_19-38-31.jpg')
    # [download_photos(get_photos_by_article(a_url)) for a_url in articles]

    for a in get_all_articles():
        for p in get_photos_by_article(a):
            download_photos(p)