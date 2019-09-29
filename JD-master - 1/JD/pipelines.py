# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdPipeline(object):
    def process_item(self, item, spider):
        print(item)
        print("数据的类型："+str(type(item)))
        print('保存数据')
        with open('G:/JDspider/JD-master - 1/JD/data.txt','a+',encoding='utf-8') as f:
            f.write(item['sort_url']+''+item['sort_name']+ ' '+str(item['num'])+' '+str(item['product_id'])+' '+item['product_brand'] +' '+item['shop_name']+' '+str(item['discription_detail'])+' '+str(item['standard'])+' '+str(item['product_price'])+' '+item['product_href']+' '+str(item['content'])+'\n')
        print('保存成功')
        return item
