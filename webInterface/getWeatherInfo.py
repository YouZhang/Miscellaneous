#!/usr/bin/env python
#coding=utf-8
import urllib ,sys
import re

class ch2pinyin(object):

    mapping = {14678: 'pian', 14345: 'qu', 12300: 'xiao', 10254: 'zuo',
               18447: 'fou', 10256: 'zun', 16401: 'kuang', 16403: 'kuan',
               10260: 'zui', 10262: 'zuan', 16407: 'kuai', 16412: 'kua',
               10270: 'zu', 18463: 'feng', 12320: 'xiang', 10274: 'zou',
               16419: 'ku', 16423: 'kou', 10281: 'zong', 14379: 'qin',
               16429: 'keng', 18478: 'fen', 14384: 'qie', 16433: 'ken',
               15369: 'ming', 10296: 'zi', 12346: 'xian', 14399: 'qiao',
               16448: 'ke', 10307: 'zhuo', 16452: 'kao', 10309: 'zhun',
               14407: 'qiang', 16459: 'kang', 16465: 'kan', 10322: 'zhuang',
               18446: 'fu', 16470: 'kai', 10328: 'zhuan', 10329: 'zhuai',
               16474: 'ka', 10331: 'zhua', 14429: 'qian', 18526: 'fa',
               18448: 'fo', 14353: 'qiu', 14355: 'qiong', 19235: 'cui',
               19479: 'chou', 17433: 'hun', 19484: 'chong', 14368: 'qing',
               14594: 'qia', 16427: 'kong', 16647: 'jun', 18696: 'er',
               18697: 'en', 12556: 'xi', 16657: 'jue', 18490: 'fei',
               18710: 'e', 10519: 'zhu', 16664: 'juan', 18722: 'duo',
               10533: 'zhou', 14630: 'qi', 12585: 'wu', 18731: 'dun',
               18735: 'dui', 10544: 'zhong', 16689: 'ju', 12594: 'wo',
               14645: 'pu', 14654: 'po', 12607: 'wen', 16706: 'jiu',
               16708: 'jiong', 14663: 'ping', 18763: 'dou', 14668: 'pin',
               14670: 'pie', 15416: 'meng', 14674: 'piao', 18773: 'dong',
               18774: 'diu', 10587: 'zhi', 16733: 'jing', 18783: 'ding',
               18183: 'gen', 19515: 'cheng', 19531: 'che', 17468: 'huang',
               18501: 'fang', 12359: 'xia', 13387: 'shuo', 15436: 'me',
               17487: 'huai', 12802: 'wei', 18518: 'fan', 18952: 'die',
               14857: 'pi', 10764: 'zheng', 18961: 'diao', 10315: 'zhui',
               16915: 'jin', 14871: 'peng', 14873: 'pen', 10780: 'zhen',
               12829: 'wan', 12831: 'wai', 18977: 'dian', 14882: 'pei',
               11014: 'zha', 10790: 'zhe', 14889: 'pao', 12039: 'xuan',
               14894: 'pang', 10800: 'zhao', 12849: 'tuo', 12852: 'tun',
               11358: 'ying', 14902: 'pan', 12858: 'tui', 19003: 'deng',
               14908: 'pai', 19006: 'de', 10815: 'zhang', 14914: 'pa',
               12871: 'tu', 13068: 'tiao', 16970: 'jiao', 12875: 'tou',
               14926: 'nuo', 19023: 'dang', 10832: 'zhan', 14929: 'nuan',
               14930: 'nv', 14933: 'nu', 10838: 'zhai', 16983: 'jiang',
               12888: 'tong', 14937: 'nong', 14941: 'niu', 19038: 'dan',
               19224: 'cuo', 19249: 'cong', 15435: 'mei', 17185: 'jian',
               12067: 'xiu', 15141: 'nen', 13095: 'teng', 13096: 'te',
               20265: 'bai', 12074: 'xiong', 14123: 'ri', 13060: 'ting',
               15109: 'ning', 15110: 'nin', 13063: 'tie', 11018: 'zeng',
               11019: 'zen', 11020: 'zei', 15117: 'nie', 15119: 'niao',
               11024: 'ze', 15121: 'niang', 19218: 'da', 13076: 'tian',
               15128: 'nian', 19227: 'cun', 11038: 'zao', 11041: 'zang',
               13091: 'ti', 15140: 'neng', 11045: 'zan', 19238: 'cuan',
               15143: 'nei', 15144: 'ne', 19242: 'cu', 19243: 'cou',
               11052: 'zai', 15149: 'nao', 15150: 'nang', 11055: 'za',
               15153: 'nan', 17202: 'jia', 13107: 'tao', 15158: 'nai',
               11067: 'yun', 15165: 'na', 19263: 'chuo', 13120: 'tang',
               11077: 'yue', 19270: 'chun', 14135: 'ren', 15180: 'mu',
               15183: 'mou', 19281: 'chuang', 13138: 'tan', 14137: 're',
               19288: 'chuan', 11097: 'yuan', 13147: 'tai', 20283: 'ba',
               19261: 'ci', 18239: 'ga', 20295: 'ang', 19275: 'chui',
               15377: 'mie', 13400: 'shuan', 15362: 'mo', 15363: 'miu',
               13318: 'ta', 17417: 'ji', 19467: 'chu', 13326: 'suo',
               15375: 'min', 13329: 'sun', 17427: 'huo', 19289: 'chuai',
               15385: 'miao', 13340: 'sui', 13343: 'suan', 15394: 'mian',
               11303: 'yu', 13356: 'su', 17454: 'hui', 13359: 'sou',
               15408: 'mi', 19976: 'bing', 13367: 'song', 15448: 'mao',
               15419: 'men', 11324: 'you', 19525: 'chen', 13383: 'si',
               12812: 'wang', 17482: 'huan', 11339: 'yong', 11340: 'yo',
               13391: 'shun', 13395: 'shui', 19540: 'chao', 13398: 'shuang',
               17496: 'hua', 13404: 'shuai', 13406: 'shua', 19990: 'biao',
               13611: 'shou', 12838: 'wa', 15454: 'mang', 19715: 'chang',
               15625: 'man', 17676: 'hu', 19725: 'chan', 15631: 'mai',
               11536: 'yin', 17683: 'hou', 16942: 'jie', 15640: 'ma',
               19739: 'cha', 17692: 'hong', 19741: 'ceng', 17697: 'heng',
               19746: 'ce', 15652: 'luo', 17701: 'hen', 17703: 'hei',
               15659: 'lun', 19756: 'cang', 15661: 'lue', 15667: 'luan',
               18996: 'di', 19774: 'cai', 19775: 'ca', 15681: 'lv',
               17730: 'hao', 17733: 'hang', 19784: 'bu', 11604: 'ye',
               15701: 'lu', 17752: 'han', 13658: 'shi', 15707: 'lou',
               19805: 'bo', 17759: 'hai', 12860: 'tuan', 20036: 'ben',
               15944: 'liang', 14921: 'ou', 19018: 'dao', 12597: 'weng',
               19212: 'dai', 14928: 'nue', 20051: 'bei', 17922: 'ha',
               11781: 'yao', 15878: 'long', 13831: 'sheng', 17928: 'guo',
               17931: 'gun', 19982: 'bin', 15889: 'liu', 19986: 'bie',
               11798: 'yang', 13847: 'shen', 17947: 'gui', 17950: 'guang',
               15903: 'ling', 20002: 'bian', 13859: 'she', 17961: 'guan',
               15915: 'lin', 17964: 'guai', 13870: 'shao', 15920: 'lie',
               17970: 'gua', 13878: 'shang', 11831: 'yan', 20026: 'bi',
               15933: 'liao', 20032: 'beng', 17988: 'gu', 13894: 'shan',
               11847: 'ya', 13896: 'shai', 17997: 'gou', 16216: 'kuo',
               13905: 'sha', 13906: 'seng', 13907: 'sen', 11861: 'xun',
               15958: 'lian', 15959: 'lia', 13914: 'sao', 11867: 'xue',
               18012: 'gong', 13917: 'sang', 19728: 'chai', 14922: 'o',
               13601: 'shu', 19751: 'cao', 14083: 'san', 18181: 'geng',
               20230: 'bao', 14087: 'sai', 18184: 'gei', 14090: 'sa',
               14092: 'ruo', 14094: 'run', 14097: 'rui', 20242: 'bang',
               14099: 'ruan', 18201: 'ge', 12058: 'xu', 16155: 'li',
               14109: 'ru', 16158: 'leng', 14112: 'rou', 20257: 'ban',
               18211: 'gao', 16169: 'lei', 14122: 'rong', 16171: 'le',
               18220: 'gang', 14125: 'reng', 19763: 'can', 16180: 'lao',
               18231: 'gan', 12089: 'xing', 16187: 'lang', 14140: 'rao',
               18237: 'gai', 18741: 'duan', 14145: 'rang', 12099: 'xin',
               20292: 'ao', 14149: 'ran', 14151: 'qun', 16202: 'lan',
               16205: 'lai', 14159: 'que', 20304: 'an', 16212: 'la',
               17721: 'he', 12120: 'xie', 14170: 'quan', 16220: 'kun',
               20317: 'ai', 20319: 'a', 16393: 'kui', 19500: 'chi',
               18756: 'du', 11589: 'yi', 13910: 'se', 15139: 'ni'}

    def get_num(self,ch_ch):
        s = ch_ch.strip();
        length = len(s);
        index_list = [];
        i = 0;
        while( i < length ):
            s_temp1 = ord(s[i]);
            if( s_temp1 < 160 ):
                index = s_temp1;
                index_list.append(index);
                i = i + 1;
            else:
                s_temp2 = ord(s[i+1]);
                index = abs(s_temp1 * 256 + s_temp2 - 65536);
                index_list.append(index);
                i = i + 2;
        return index_list;
        
    def dict_index(self,index_list):
        result = [];
        start1 = len(index_list);
        start2 = len( self.mapping );
        keys = self.mapping.keys();
        keys.sort();

        re = '';
        for i in range ( 0,start1,1):
            index_item = index_list[i];
            for j in range ( 0,start2,1):
                mapping_item = keys[j];
                if( index_item <= 160 ):
                    temp = chr(index_item);
                    re = re + temp;
                    result.append(temp);
                    break;
                elif( index_item <= mapping_item ):
                    re = re + self.mapping[mapping_item]; 
                    result.append(self.mapping[mapping_item]);
                    break;
        return result,re;

def weather_info():
    
    instance = ch2pinyin();
    provice=raw_input('input a province:').replace(' ','');   
    num = instance.get_num(provice);
    pro_list,pro_pinyin = instance.dict_index(num);
    ##print pro_list,pro_pinyin;
    major = raw_input('input a major:').replace(' ','');
    num = instance.get_num(major);  
    maj_list1,maj_pinyin1 = instance.dict_index(num);
    ##print maj_list1,maj_pinyin1;
    url="http://qq.ip138.com/weather/"+pro_pinyin +'/'+maj_pinyin1+'.htm'
    ##print url

    try:
        wetherhtml=urllib.urlopen(url)
    except:
        print "网络不稳定啊...."
        sys.exit(1);
    result=wetherhtml.read().decode('GB2312','ignore').encode('utf-8','ignore');

    if( '文件没有找到' in result ):
        print "输入的地区不存在啊..";
        sys.exit();
    else:
        f=file('weather.txt','w')
        f.write(result)
        f.close()
        
    result = result.decode('utf-8','ignore');

    pattern='Title.*<b>(.*)</b>'
    Title=re.search(pattern,result).group(1)

    pattern='>(\d*-\d*-\d*.+)<'
    date=re.findall(pattern,result)

    pattern='<br/>(.*)</td>';
    weather=re.findall(pattern,result)

    pattern = '<td>(\d{1,2}.+\d{1,2}.)</td>'
    temperature=re.findall(pattern,result)

    pattern='<td>(.{2,8})</td>'
    wind_temp =re.findall(pattern,result)
    wind = wind_temp[7:14];

    pattern = '<li>(.*)</li>'
    code =re.findall(pattern,result)

    for item in code:
        print "%35.30s"%item;
            
    print "%35.30s"%Title,""
    length=len(date)

    for i in range(length):
        print '%30.20s'%date[i],'%s'%weather[i],\
        '%10s'%temperature[i],'%10s'%wind[i];

if __name__ == '__main__':
    weather_info(); 
