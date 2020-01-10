import spyder_hao5_net
import pymysql


conn = pymysql.connect("localhost","root","123456","pttv_spider_channel")
try:
    #启动hao5_net Spyder
    spyder_hao5_net.start(conn)
except Exception as e:
    print('except: Exception ', e)
finally:
    conn.close()  # 关闭连接
