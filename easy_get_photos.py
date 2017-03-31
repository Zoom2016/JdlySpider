
import requests
from bs4 import BeautifulSoup
import time
import urllib
import re
import os

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
    page_max = 1
    print(page_max)
    article_list = list()
    for page_index in range(page_max):
        page_url = url_model + '%d' % (page_index + 1)
        content = requests.get(page_url, headers=header).content
        soup = BeautifulSoup(content,'html.parser')
        post_list = soup.find_all('div', {'class': 'pin-coat'})
        [article_list.append(post.a.get('href')) for post in post_list]
        # time.sleep(2000)
        print('Colloceting article url - [%d / %d Page]' % (page_index+1, page_max))

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
    print('Photo url is ' + photo)
    # photo_name = re.findall(r'\\(.*)$', photo)[0]
    # photo_name = re.findall(r'\(*.jpg)', photo)[0]
    photo_name = photo.split('/')[-1]

    local_path = os.path.dirname(os.path.realpath(__file__)) + '\\jdly\\' + photo_name
    if not os.path.exists(local_path):
        urllib.request.urlretrieve(photo, local_path)
        print('Download : [%s] is done' % local_path)
    pass


def write_articles_file(articles):
    with open('articles.txt', 'w') as file_object:
        file_object.writelines([article + '\n' for article in articles])


def read_articles_file():
    with open('articles.txt', 'r') as file_object:
        articles = file_object.readlines()
        return [a.strip('\n') for a in articles]

def save_progress(index):
    with open('progress.txt', 'w') as file_object:
        file_object.write(str(index))

def load_progress():
    if not os.path.exists('progress.txt'):
        return -1

    with open('progress.txt', 'r') as file_object:
        index = file_object.read()
        return int(index)

def jdly_hacker():
    # 读取进度
    progress = load_progress()
    a_list = list()
    # 未开始
    if -1 == progress:
        a_list = get_all_articles()
        write_articles_file(a_list)
        print('A new job is started.')
    else:
        all_a_list = read_articles_file()
        # 已完成
        if len(all_a_list) <= progress + 1:
            print('Job was already done.')
            return
        else:
            a_list = all_a_list[progress + 1:]
            print('Job is started at %d' % progress + 1)

    article_num = len(a_list)
    for i, a in enumerate(a_list):
        print('Visiting article - [%d / %d ]. Article url is %s.' % (i+1, article_num, a))
        for p in get_photos_by_article(a):
            download_photos(p)
        save_progress(progress+1+i)

    print('Jod is done.')

if __name__ == '__main__':

    jdly_hacker()