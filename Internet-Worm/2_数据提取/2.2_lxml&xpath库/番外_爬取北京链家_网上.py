import requests
from lxml import etree
import csv
import time
import threading


# 小区具体一页房源信息的抓取，输入为当前页面url,当前爬取页数pa。返回数据为小区房源总数num，该页抓取的房源信息home_list,状态码1或0（1表示成功）
def parse_xiaoqu(url, pa):
    hd = {'Host': 'sh.lianjia.com',
            'Referer': 'https://sh.lianjia.com/ershoufang/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

            }
    r = requests.get(url, headers=hd, timeout=30)
    html = etree.HTML(r.text)
    num = html.xpath('//div[@class="content"]//div[@class="total fl"]/span/text()')[0]
    num = int(num)
    datas = html.xpath('//li/div[@class="info"]')
    print('小区房源总数：', num, '第%d页房源数:' % pa, len(datas))
    print(url)
    if len(datas) == 0:
        return (num, [], 0)  # 服务器无返回数据，状态码返回0
    house_list = []
    for html1 in datas:
        title = html1.xpath('div[@class="title"]/a/text()')
        info = html1.xpath('div[@class="address"]/div[@class="houseInfo"]/text()')
        floor = html1.xpath('div[@class="flood"]/div[@class="positionInfo"]/text()')
        info[0] = info[0].replace('\xa0', '')  # 该条信息中有个html语言的空格符号&nbsp；需要去掉，不然gbk编码会报错，gb18030显示问号
        date = html1.xpath('div[@class="address"]/div[@class="dealDate"]/text()')
        # 30天内成交的进入详情页面抓取
        if date[0] == '近30天内成交':
            p_url = html1.xpath('div[@class="title"]/a/@href')
            r = requests.get(p_url[0], headers=hd, timeout=5)
            html = etree.HTML(r.text)
            price = html.xpath('//div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/span/i/text()')
            unitprice = html.xpath('//div[@class="overview"]/div[@class="info fr"]/div[@class="price"]/b/text()')
            date = html.xpath('//div[@class="house-title LOGVIEWDATA LOGVIEW"]/div[@class="wrapper"]/span/text()')
            # 有的房源信息没有价格信息，显示暂无价格
            if len(price) == 0:
                price.append('暂无价格')
            if len(unitprice) == 0:
                unitprice.append('暂无单价')
            date[0] = date[0].replace('链家成交', '')
            a = [title[0], info[0], floor[0], date[0], price[0], unitprice[0]]
            house_list.append(a)
            print(title[0], info[0], floor[0], date[0], price[0], unitprice[0])
        else:
            price = html1.xpath('div[@class="address"]/div[@class="totalPrice"]/span/text()')
            unitprice = html1.xpath('div[@class="flood"]/div[@class="unitPrice"]/span/text()')
            if len(price) == 0:
                price = ['暂无价格']
            if len(unitprice) == 0:
                unitprice = ['暂无单价']
            a = [title[0], info[0], floor[0], date[0], price[0], unitprice[0]]
            house_list.append(a)
            print(title[0], info[0], floor[0], date[0], price[0], unitprice[0])
    print('                *********************         ', '第%d页完成！' % pa)
    return (num, house_list, 1)


# 抓取某小区所有已成交二手房信息，排重后存入本地csv，输入为小区id，返回抓取到的该小区的房源总数
def crow_xiaoqu(id):
    url = 'https://bj.lianjia.com/chengjiao/c%d/' % int(id)
    h_list = []  # 保存该小区抓取的所有房源信息
    fail_list = []  # 保存第一次抓取失败的页数，第一遍抓取完成后对这些页数再次抓取
    try:
        # 爬取小区第一页信息
        result = parse_xiaoqu(url, 1)
    except:
        # 如果第一页信息第一次爬取失败，sleep2秒再次爬取
        time.sleep(2)
        result = parse_xiaoqu(url, 1)
    # 获取该小区房源总数num
    num = result[0]
    # 如果无数据返回，sleep2秒再爬取一次
    if num == 0:
        time.sleep(2)
        result = parse_xiaoqu(url, 1)
        num = result[0]
    new_list = result[1]
    pages = 1
    for data in new_list:
        if data not in h_list:
            h_list.append(data)
    # 确定当前小区房源页数pages
    if num > 30:
        if num % 30 == 0:
            pages = num // 30
        else:
            pages = num // 30 + 1
    for pa in range(2, pages + 1):
        new_url = 'https://bj.lianjia.com/chengjiao/pg' + str(pa) + 'c' + str(id)
        try:
            result = parse_xiaoqu(new_url, pa)
            status = result[2]
            if status == 1:
                new_list = result[1]
                # 排重后存入h_list
                for data in new_list:
                    if data not in h_list:
                        h_list.append(data)
            else:
                fail_list.append(pa)
        except Exception as e:
            fail_list.append(pa)
            print(e)
    print('   开始抓取第一次失败页面')
    for pa in fail_list:
        new_url = 'https://bj.lianjia.com/chengjiao/pg' + str(pa) + 'c' + str(id)
        print(new_url)
        try:
            result = parse_xiaoqu(new_url, pa)
            status = result[2]
            if status == 1:
                new_list = result[1]
                for data in new_list:
                    if data not in h_list:
                        h_list.append(data)
            else:
                pass
        except Exception as e:
            print(e)
    print('    抓取完成，开始保存数据')
    # 一个小区的数据全部抓完后存入csv
    with open('lianjia_123.csv', 'a', newline='', encoding='gb18030')as f:
        write = csv.writer(f)
        for data in h_list:
            write.writerow(data)
    # 返回抓取到的该小区房源总数
    return (len(h_list))


if __name__ == '__main__':
    counts = 0  # 记录爬取到的房源总数
    now = time.time()
    id_list = []
    with open('xiaoqu_id.csv', 'r')as f:
        read = csv.reader(f)
        for id in read:
            id_list.append(id[0])
    m = 0
    # 可以通过修改range函数的起始参数来达到断点续抓
    for x in range(0, 2990):
        m += 1  # 记录一共抓取了多少个小区
        print('    开始抓取第' + str(m) + '个小区')
        time.sleep(1)
        count = crow_xiaoqu(id_list[x])
        counts = counts + count
        # 打印已经抓取的小区数量，房源数量，所花的时间
        print('     已经抓取' + str(m) + '个小区  ' + str(counts) + '条房源信息', time.time() - now)

