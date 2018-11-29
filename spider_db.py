from urllib import request
import re
from urllib import error

class Spider():
    url = 'https://book.douban.com/top250?start=0'
    root_pattern = '<div class="pl2">([\s\S]*?)</div>'
    url_pattern = r'<a href="(.*?)" .*?>' 
    div_pattern = '<div id="info" class="">([\s\S]*?)</div>'
    name_pattern = r'<span property="v:itemreviewed">(.*?)</span>'
    writer_pattern = r'作者.*?</span>.*?<a.*?>(.*?)</a>'
    pub_house_pattern = r'出版社.*?</span>.*?(.*?)<br/>'
    pub_company_pattern = r'出品方.*?</span>.*?>(.*?)</a>'
    origin_name_pattern = r'原作名.*?</span> (.*?)<br/>'
    interpreter_pattern = r'译者.*?</span>.*?<a.*?>(.*?)</a>'
    pub_time_pattern = r'出版年.*?</span> (.*?)<br/>'
    page_num_pattern = r'页数.*?</span> (.*?)<br/>'
    price_pattern = r'定价.*?</span> (.*?)<br/>'
    bind_pattern = r'装帧.*?</span> (.*?)<br/>'
    ISBN_pattern = r'ISBN.*?</span> (.*?)<br/>'
    content_pattern = r'<div class="intro">(.*?)</div>'
    def __fetch_content(self,url):
        try:
            r = request.urlopen(url)
            # bytes
            htmls = r.read()
            htmls = str(htmls, encoding = 'utf-8')
            return htmls
        except Exception as e:
            print(e)
            print('此页为空！')
           
    def __analysis_url(self,htmls):
        sub_urls = []
        web_html = re.findall(Spider.root_pattern, htmls)
        for html in web_html:
            sub_url = re.findall(Spider.url_pattern,html,re.S)[0]
            sub_urls.append(sub_url)
        return sub_urls

    def __analysis_web(self,url):
        sub_info = {}
        htmls = self.__fetch_content(url)
        if not htmls:
            return None
        name  = self.__handle(Spider.name_pattern,htmls)
        content = self.__handle(Spider.content_pattern,htmls)
        sub_info['作品'] = name
        info_html = re.findall(Spider.div_pattern, htmls)      
        for html in info_html:
            # print(html)
            writer = self.__handle(Spider.writer_pattern,html)
            pub_house = self.__handle(Spider.pub_house_pattern,html)
            pub_company = self.__handle(Spider.pub_company_pattern,html)
            origin_name = self.__handle(Spider.origin_name_pattern,html)
            interpreter = self.__handle(Spider.interpreter_pattern,html)
            pub_time = self.__handle(Spider.pub_time_pattern,html)
            page_num = self.__handle(Spider.page_num_pattern,html)
            price = self.__handle(Spider.price_pattern,html)
            bind = self.__handle(Spider.bind_pattern,html)
            ISBN = self.__handle(Spider.ISBN_pattern,html)
            sub_info['作者'] = writer
            sub_info['出版社'] = pub_house
            sub_info['出品方'] = pub_company
            sub_info['原作名'] = origin_name
            sub_info['译者'] = interpreter
            sub_info['出版年'] = pub_time
            sub_info['页数'] = page_num 
            sub_info['定价'] = price
            sub_info['装帧'] = bind
            sub_info['ISBN'] = ISBN
        sub_info['内容简介'] = content
        a = 1
        return sub_info      
    def __handle(self,pattern,s):
        result = re.findall(pattern,s,re.S)
        if not result:
            return ''
        else:
            result = re.findall(pattern,s,re.S)[0].strip()
            result = result.replace(' ','')
            result = result.replace('\n','')
            result = result.replace('<p>','')
            result = result.replace('</p>','')
            return result

    def __change_page(self, n):
        url = 'https://book.douban.com/top250?start='+str(n)
        return url
    
    def __show(self,infos):
        for x in range(0,len(infos)):
                print("排名"+str(x+1)+':')
                for key,value in infos[x].items():
                    print('{key}:{value}'.format(key = key, value = value))

    def go(self):
        infos = []
        for x in range(0,226,25):
            url = self.__change_page(x)
            htmls = self.__fetch_content(url)
            sub_urls = self.__analysis_url(htmls)
            for sub_url in sub_urls:
                info =self.__analysis_web(sub_url)
                if not info:
                    continue
                infos.append(info)
            self.__show(infos)
        return infos

spider = Spider()
spider.go()
