# 创建于2017年3月28日 by Zoom

import requests
from bs4 import BeautifulSoup

# 主页网址
HomePage = "http://www.jdlingyu.moe/"
# 网站名称
HomeName = "绝对领域"


def get_menu_tree():
    """
    功能：获取首页菜单树
    :return:菜单树（菜单名、菜单链接）
    """
    pass


def get_articles_of_menu(menu_url):
    """
    根据传入的菜单链接，查到下面所有文章
    :param menu_url:菜单URL
    :return:文章列表（URL、标题、原文章id、阅读数、喜欢数、评论数、最后更新日期）,标签列表（标签名、标签URL）
    """
    pass

