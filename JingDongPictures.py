#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Doc description: Download Jingdong product pictures 获取京东商品手机类主图片'

__author__='HisenLee' 

# 网络请求
import urllib.request
import urllib.error
# 正则
import re

# 定义一个crawl函数专门负责解析网页，获取图片链接
def crawl(url, page):
	req = urllib.request.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0")
	pageHtml = urllib.request.urlopen(req, timeout=60).read()	
	pageStr = str(pageHtml)
	# 正则解读 .匹配除了\n和\r之外的任意单个字符 +匹配至少一次 .+表示至少有一个任意字符 .+?表示懒惰匹配(最少匹配)
	pattern1 = '<div id="plist".+? <div class="page clearfix">'
	result1 = re.compile(pattern1).findall(pageStr)
	result1 = result1[0]
	# 正则解读 (.+?\.jpg) .+?懒惰匹配至少一个任意字符(保证了不为空串) \.jpg转义.jpg
	pattern2 = '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)'
	imagelist = re.compile(pattern2).findall(result1)
	index = 1
	print("正在下载第" + str(page) + "页，改页一共有 " + str(len(imagelist)) + " 个数据")
	for imageurl in imagelist:		
		imagename = "E:/python/test/" + str(page) + "_" +str(index) + ".jpg"
		imageurl = "http://" + imageurl
		try:
			# 调用urlretrieve 可以直接把远程数据下载到本地
			urllib.request.urlretrieve(imageurl, filename=imagename)			
		except urllib.error.URLError as e:
			if hasattr(e, "code"):
				index+=1
			if hasattr(e, "reason"):
				index+=1
		index+=1

# 取top80页的数据		
for pageIndex in range(1, 79):	
	url = "https://list.jd.com/list.html?cat=9987,653,655&page=" + str(pageIndex)
	crawl(url, pageIndex)
