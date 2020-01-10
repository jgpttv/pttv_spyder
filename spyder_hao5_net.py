# 爬取http://www.hao5.net/的数据
from pyquery import PyQuery as pq
# from urllib import parse
from furl import furl
import pymysql

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Connection': 'close'
}


def start(conn):
    url = "http://www.hao5.net/"
    doc = pq(url, encoding="gbk")
    xyous = doc("div.xyou").items()

    for xyou in xyous:
        cy = xyou("div.cy")
        # 类别
        channel_type = cy.text()
        items = xyou("div.cyc ul li a").items()
        for item in items:
            # 频道名称
            channl_name = item.text()

            channl_page_url = url + item.attr("href")
            # print('doc aurl ==', item.attr("href"))
            channl_page = pq(channl_page_url, encoding="gbk")
            embed = channl_page("embed")
            src = embed.attr("src")
            if src != None:
                if "http" in src:
                    channel_source = ""
                    if "vurl=" in src:
                        ps = furl(src)
                        if ps != None:
                            channel_source = ps.args['vurl']

                    elif "f=" in src:
                        ps = furl(src)
                        if ps != None:
                            channel_source = ps.args['f']

                    if channel_source != "" and channel_source != None:
                        # 保存到数据库
                        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                        # 先查询是否存在记录
                        selectsql = 'select count(*) as count  from channels where channel_name = %s'

                        cursor.execute(selectsql, (channl_name,))
                        count = cursor.fetchone()
                        #print("count=",count)
                        if count is None or count['count'] == 0:
                            # 还没有数据，插入数据
                            datasql = 'insert into channels(channel_name,channel_type,channel_source) values (%s,%s,%s)'
                            r = cursor.execute(datasql, (channl_name,channel_type, channel_source))
                            print("插入数据  channl_name == "+channl_name+" channel_type == "+channel_type+"  channel_source == "+channel_source)
                        else:
                            #该频道数据已存在，更改数据
                            datasql = 'UPDATE channels SET channel_source = "%s",channel_type = "%s" WHERE channel_name = "%s"'
                            r = cursor.execute(datasql, (channel_source,channel_type, channl_name))
                            print("修改数据  channl_name == " + channl_name + " channel_type == " + channel_type + "  channel_source == " + channel_source)
                        # 向数据库提交
                        conn.commit()
                        # 关闭（游标、数据库）
                        cursor.close()
                else:
                    print("src 不包括 http src ==  ", src)
    return None
