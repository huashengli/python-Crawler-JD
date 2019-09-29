# -*- coding: utf-8 -*-
import scrapy
#from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import requests,json,re
import time
from lxml import etree

from urllib.parse import unquote

class JdSpider(scrapy.Spider):  #将scrapy.Spider修改为
    name = 'Jd2'
    allowed_domains = ['jd.com','item.jd.com','sclub.jd.com','p.3.cn']
    start_urls = ['https://search.jd.com/Search?keyword=墙纸&enc=utf-8&pvid=9ee4d92400cc494cb60d40abf7031011']


    # redis_key = 'JD'

    def parse(self, response):
        # response返回整个网页
        #列表页
        item = {}
        item['num'] = 2  # 发送一个值，为网页翻页做准备
        item['start_url']=response.url
        yield scrapy.Request(
            item['start_url'],
            callback=self.page_list,
            meta={'item': deepcopy(item)}
        )
    def page_list(self, response):
        item = response.meta['item']
        a = time.time()
        b = '%.5f' % a
        url = 'https://search.jd.com/s_new.php?keyword=%E5%A2%99%E7%BA%B8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=qiang%27zhi&stock=1&page=' + str(item['num']) + '&s=' + str(30*item['num']) + '&scrolling=y&log_id=' + str(b)
        head = {
            'Accept': 'text/html, application/xhtml+xml, */*',
            'referer': 'https://search.jd.com/Search?keyword=%E5%A2%99%E7%BA%B8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=qiang%27zhi&stock=1&page='+str(item['num']-1)+'&s='+str(30*(item['num']-1))+'&click=0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        print("30条信息url地址:"+url)
        r = requests.get(url, headers=head)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        print('html类型：' + str(type(html)))
        All_sort = html.xpath('//div[@class="p-name p-name-type-2"]')#获取列表第1页的产品详情地址
       # print("这是包含产品url:"+str(All_sort.extract()))
        print("parse函数")
        print("All_sort类型："+str(type(All_sort)))#<class 'list'>
        for i in All_sort:
            product_url = i.xpath('./a/@href')   #获取每个墙纸产品详情页地址
            product_url = str(product_url)#list转str
            product_url = re.sub(r'\[|\]|\’|\'', "", product_url)#去除[]和''
            print(product_url)
            print("product_url类型：" + str(type(product_url)))#<class 'str'>

            m = re.match('https:', product_url)  #有些sort_url在获得时就是一个完整的url，通过re匹配判断url是否完整
            if m is None:
                print("不完全的url")
                item['sort_url'] = 'https:'+product_url
                print("这是完全的url:"+item['sort_url'])
            else:
                item['sort_url']=product_url
                print(item['sort_url'])
            sort_name_0 = i.xpath('./a/em/text()')  #获取分类的名称
            sort_name_1=[str(i) for i in sort_name_0]#把list多个值拼接成一个字符串
            sort_name=''.join(sort_name_1)
            item['sort_name'] = sort_name.strip()
           # print(item['sort_url'], item['sort_name'])
            yield scrapy.Request(
                item['sort_url'],
                callback=self.wallpaper_list,
                meta={'item': deepcopy(item)}  # 防止信息被重写
            )
        # 下一页
        # 通过观察猜测，下一页的规律：page为1,3,5...2*a+1,s(大概是商品的数量）大约在50~60的范围，我取最大值，keyword是不同于之前获取的商品名称
        # 所以直接在url中获取。click.......
        keyword = re.compile('keyword=(.*?)&').findall(response.url)  # 获取响应url中的keyword，构造下页的url
        #print("这是:"+keyword)
        print("获取下一页商品列表页")
        if len(keyword) > 0:
            keyword = unquote(keyword[0])
            item['num'] = item['num'] + 2
            b_str = str(keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page=%s&s=%s&click=0'
            next_url = 'https://search.jd.com/Search?keyword=' + b_str
            print("获取下一页地址的参数初始0："+str(item['num']))
            next_page =item['num']
            page_num = 30 * item['num']
            next_url = next_url % (next_page, page_num)
            print("列表页下一页地址"+next_url)
            print('num为：'+str(item['num']) + '时下一页为：' + str(next_page))
            if item['num'] < 201:
                yield scrapy.Request(
                    next_url,
                    callback=self.page_list,
                    meta={'item': deepcopy(item)}
                )





    def wallpaper_list(self,response):
        item = response.meta['item']
        print("wallpaper_list函数")
        item['product_id'] = response.xpath('//div[@class="preview-info"]/div[@class="left-btns"]/a/@data-id').extract_first()
        item['product_brand']=response.xpath('//ul[@id="parameter-brand"]/li/a/text()').extract_first()
        item['shop_name']=response.xpath('//div[@class="mt"]/h3/a/text()').extract_first()
        item['discription_detail']=response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()
        standard=response.xpath('//div[@class="Ptable-item"]/dl/dl[@class="clearfix"]')
        item['standard']=standard.xpath('normalize-space(string(.))').extract()
        yield scrapy.Request(
            "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["product_id"]),
            callback=self.wallpaper_price,
            meta={"item": deepcopy(item)}
        )


    def wallpaper_price(self, response):
        item=response.meta["item"]
        print("wallpaper_price函数")
        item["product_price"]=json.loads(response.body.decode())[0]["p"]
        yield scrapy.Request(
            "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv482&productId={}&score=0&sortType=5&page=%s&pageSize=10".format(item['product_id']),
            callback=self.C_comment,
            meta={'item':deepcopy(item)}
        )




    def C_comment(self,response):
        item = response.meta['item']
        print("c_comment评论函数")
        print("当前产品的id："+str(item['product_id']))
        item['product_href'] = 'https://item.jd.com/' + str(item['product_id'])+'.html'
        if item['product_id'] is None:
            item['product_id'] = response.xpath('//div[@class="preview-info"]/div[@class="left-btns"]/a/@data-id').extract_first()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Referer':'https://item.jd.com/' + str(item['product_id']+'.html')}
        #在获取商品评论时，headers需要添加'Referer':response.url，才能得到网页数据，利用获取的id构造url
        comment_url = str(response.url)
        content_list = []
        for i in range(0,1000):
            a = requests.get(comment_url%str(i),headers=headers)
            print(str(item['product_href']) +'---a的长度'+str(len(a.content)))
            data = a.content.decode('gbk')
            content = re.compile('"content":"(.*?)"').findall(data)
            print(len(content))
            for i in content:
                lr = i.split('<',1)    #去除评论中的网页标签
                # print(lr)
                content_list.append(lr[0])
            if len(content) < 10:
                break
        if len(content_list) == 0:
            item['content'] = ''
        else:
            item['content'] = content_list
        # print(item)
        return item