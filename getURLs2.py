#!/usr/bin/env python
# coding=utf-8
import urllib
import time
import re

#第一步 获取维基百科内容
#http://zh.wikipedia.org/wiki/程序设计语言列表
temp4="https://zh.wikipedia.org/w/index.php?title=Category:%E4%B8%AD%E5%9B%BD%E7%94%B5%E5%BD%B1%E6%BC%94%E5%91%98&pagefrom=Yi%E6%98%93%0A%E6%98%93%E7%83%8A%E5%8D%83%E7%8E%BA#mw-pages"
temp="https://zh.wikipedia.org/w/index.php?title=Category:%E9%A6%99%E6%B8%AF%E7%94%B7%E6%AD%8C%E6%89%8B&pagefrom=%E7%8E%8B%E5%96%9C#mw-pages"
content = urllib.urlopen(temp).read()
open('wikipedia.html','w+').write(content)
print 'Start Crawling pages!!!'


#第二步 获取网页中的所有URL
#从原文中"0-9"到"参看"之间是A-Z各个语言的URL
start=content.find(r'王喜')
end=content.find(r'龐景峰')
cutcontent=content[start-1:end+1]
#print cutcontent
link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", cutcontent)
print 'URL Successed! ',len(link_list),' urls.'

#第三步 下载每个程序URL静态文件并获取Infobox对应table信息
#国家：http://zh.wikipedia.org/wiki/阿布哈茲
#语言：http://zh.wikipedia.org/wiki/ActionScript
info=open('infobox.txt','w')
info.write('****************获取程序语言信息*************\n\n')
j=1
wr = open('personBD.txt','w')
for url in link_list:
    if url.find('wiki')>=0 : # or url.find('index.php')>=0:
        #下载静态html
        wikiurl='http://zh.wikipedia.org'+str(url)
        print urllib.unquote(wikiurl)
        person = urllib.urlopen(wikiurl).read()
        #print person
        name=str(j)+' person.html'
        #注意 需要创建一个country的文件夹 否则总报错No such file or directory
        open(r'person/'+name,'w+').write(person) #写方式打开+没有即创建
        #获取title信息
        title_pat=r'(?<=<title>).*?(?=</title>)'
        title_ex=re.compile(title_pat,re.M|re.S)
        title_obj=re.search(title_ex, person) #language对应当前语言HTML所有内容
        title=title_obj.group()
        #获取内容'C语言 - 维基百科，自由的百科全书' 仅获取语言名
        middle=title.find(r'-')
        info.write('【person  '+title[:middle]+'】\n')
        print title[:middle]

        bday_pat = r'<span .*?bday.*?>(.*?)</span>'
        bday_ex=re.compile(bday_pat,re.M|re.S)
        bday = re.findall(bday_ex, person)
        for item in bday:
            print item
            wr.write(title[:middle-1]+','+ item + ','+urllib.unquote(wikiurl + '\n'))
            break

        #设置下载数量
        j=j+1
        time.sleep(1)
        #if j==20:
        #    break;
    else:
        print 'Error url!!!'
else:
    print 'Download over!!!'
