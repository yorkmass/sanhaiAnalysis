import time
import csv
import codecs #解决乱码
import requests
from pyquery import PyQuery as pq
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'Referer':'https://www.zhihu.com/',
    'Cookie':'_zap=19f7d5fd-ad77-4d57-8e30-7367702a627f; d_c0="AHAe2UBrAhOPTqttN0xd7EOOkjToTgg4MPw=|1619359848"; _9755xjdesxxd_=32; __snaker__id=V2HBrXOeoWzQEeeP; YD00517437729195%3AWM_TID=gRu%2Bc5lsNlFFUABBAAZ%2Fp5Q5C790Hn3X; captcha_session_v2="2|1:0|10:1639399736|18:captcha_session_v2|88:TEJPZ1hpRzVwNE5IeUNLeDZMd25YMjc2Y1hMY2p0cXJ2a0h5WENLQ2lFNzV2TGJJMEhRemM5dHpHKzhjRG0vYQ==|d71b8b2225e627c89b0b372519bc60df79674b3c18d8817541faf25a0abc36f4"; gdxidpyhxdE=lWvEJGdNSNYiY6%5CEXxqkZKnkqsA2E5xtCsPT2Jhhp50Pdawl67Ssh331g%2BdqrSlDha5E5uU8i%2F%2F1prcakC0%5C0rjYRRgveVhCMRnTiQhyKuTd9%2F%5CnIh4sa6bmPp0rrG61NQxnuAM2eQ9ypIrncYp5PTwYL9d1QoJxxXaCwK3DrDydkHLy%3A1639400635959; YD00517437729195%3AWM_NI=Lutgu7IYWXmTWZAEs9gbR5u%2FTiZM%2BWQY8SpNHifpQ6sYZ9x6YXpIp2%2Fdu73p%2BXZ5ELU%2FNnKUZcUXZxV5m2Sab01YfzNOsYPv3ByPy8D7zg%2BxBsVsVxt5KHCqpbzDeEZGZkw%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeaebc6ef5e89fb9e57496e78aa3c15a968f9ebaf534b8adae95f062a5b09e93c62af0fea7c3b92a90abbc88f83d8b8799b9f06095868fa6f233a5be9ed6f82598b796aeaa5d9387f8b4f3468cb7aa91d43eb18796dafb3e9b88c0aaf33aedbcbbd8b27ce98896d6c84897f1828fca5f9abd9bb9d97496eba3d3d26ba2f0ffbae5728e91bdbad37ef19eb7b1fc3488e9b688aa7482ad9a94d574b8eb85a9c27bb4beb6a5e84f9a99968cf637e2a3; r_cap_id="ZGIwMzRiZmRhZWJlNDlhNGE1OGRlMmUyODllMmFhNDQ=|1639399740|fb778b35c7d35c7cf963120b90fd8f3bb1badb2a"; cap_id="NWYyOTI2NWI0ZmEwNDNkM2IxYTM3YTVlNWE5ZmM1YjE=|1639399740|5b225c8bf8ba1dee9e93b4fa419642dbcb7ecf4d"; l_cap_id="MGZmOTYyY2M4MGQxNGVmODlkNmNhN2UwNDQ5NzU3ZDM=|1639399740|bdbc72c7f8320f5eca418c23abbd04175460689e"; z_c0=Mi4xM1owWEN3QUFBQUFBY0I3WlFHc0NFeGNBQUFCaEFsVk5WNC1rWWdEMWdpZXhtN0E3QWxuQXF4QkpnQ3A4Tkd4QmJR|1639399767|589149fc4d3fdedb036ff8789cfe55fc3c904d70; _xsrf=f06c3bbf-3df5-4bc3-8df9-e73e3482b249; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1637247592,1639062875,1639062955,1639474210; NOT_UNREGISTER_WAITING=1; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1639474244; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1639474254|1639474209'
}

# Request URL
base_url = "https://www.zhihu.com/api/v4/questions/462403650/answers?"
include = "include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled"
# 获得页面
def get_page(offset):
    page_url = include + '&limit=5&' + 'offset=' + str(offset) + '&platform=desktop&sort_by=default'
    url = base_url + page_url
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
# 时间戳转化为年-月-日 时-分-秒
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
# 解析网页
def parse_page(json):
    if json:
        items = json.get('data')
        for item in items:
            try:
                zhihu = {}
                zhihu['作者'] = item.get('author').get('name')
                zhihu['user_token'] = item.get('author').get('url_token')
                if(len(item.get('content'))>0):
                    zhihu['回答'] = pq(item.get('content') ).text()
                else:
                    zhihu['回答'] = ''
                zhihu['创建时间'] = TimeStampToTime(item.get('updated_time'))
                zhihu['赞同数'] = item.get('voteup_count')
                zhihu['评论数'] = item.get('comment_count')
                yield zhihu
            except IOError:
                print("解析失败")
            else:
                print("写入成功")

if __name__ == '__main__':
    i = 0
    f = codecs.open('知乎三孩.csv', 'w+', 'utf_8_sig')
    f_txt = open('知乎三孩.txt', 'w+', encoding='utf_8')
    fieldnames = ['作者', 'user_token', '回答', '创建时间', '赞同数', '评论数']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        js = get_page(i * 5)  # 根据报文首个回答对应的索引值获取页面
        results = parse_page(js)
        for res in results:
            writer.writerow(res)
            for detail in res.values():
                f_txt.write(str(detail) + '\n')
            f_txt.write('\n' + '*' * 50 + '\n')  # 分隔符
        if js.get('paging').get('is_end'):
            print('finish!')
            break
        print(i)
        i += 1

    f.close()
    f_txt.close()
