#coding=utf-8
import cookielib,sys;
import urllib2;
import urllib;
import string;

def encryption(code):
        from_code = '!-#$%^&*()qwertyuiopasdfghjklzxcvbnm';
        to_code = '1234567890abcdefghijklmnopqrstuvwxyz';
        mapping = string.maketrans (from_code,to_code);
        code_encry = code.translate(mapping);
        return code_encry;

class xiami():

    login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
##                    'Accept-Encoding':'gzip,deflate,sdch',    #这个编码有问题,不要加;
                    'Accept-Language':'zh-CN,zh;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Host':'www.xiami.com',
                    'Origin':'http://www.xiami.com',
                    'Referer':'http://www.xiami.com/member/login',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
                    };
    signin_header = {'Accept':'*/*',
                     'Accept-Language':'zh-CN,zh;q=0.8',
                     'Connection':'keep-alive',
                     'Content-Length':0,
                     'Content-Type':'application/x-www-form-urlencoded',
                     'Host':'www.xiami.com',
                     'Origin':'http://www.xiami.com',
                     'Referer':'http://www.xiami.com/',
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',   #useragent是关键
                     'X-Requested-With':'XMLHttpRequest'
                     }
    email = '';
    pwd = '';
    cookie = None;
    cookie_file = './cookie.dat';


    def __init__(self,email,pwd):

        self.email = encryption(email);
        print self.email
        self.pwd = encryption(pwd);
        self.cookie = cookielib.LWPCookieJar();
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie);
        opener = urllib2.build_opener (cookie_support);
        urllib2.install_opener (opener);


    def login(self):
        post_data = {'email':self.email,
                     'password':self.pwd,
                     'done':'%2F',
                     'validate':5,
                     'submit':'%E7%99%BB+%E5%BD%95'
                     }
        post_data = urllib.urlencode(post_data);
##        print post_data;
        print "正在登入....";
        ##请求
        req = urllib2.Request (url = 'http://www.xiami.com/member/login',data = post_data,headers = self.login_header);
        result = urllib2.urlopen(req).read();
        self.cookie.save(self.cookie_file);
        result = str(result).decode('utf-8').encode('gbk','ignore');
        if('Email 或者密码错误' in result ):
            print "用户名或密码错误";
            sys.exit(1);
        elif('验证码' in result):
            print '居然要输入验证码'
            self.login();
        else:
            print "登入成功，请稍等....";

    def signin(self):
        post_data = {};
        post_data = urllib.urlencode(post_data);
        print "正在签到...";
        req = urllib2.Request (url = 'http://www.xiami.com/task/signin',data= post_data,headers = self.signin_header)
        result = urllib2.urlopen(req).read();
        result = str(result).decode('utf-8').encode('gbk','ignore');
        self.cookie.save(self.cookie_file);
        try:
            result = int(result);
        except ValueError,e:
            print '签到失败';
            sys.exit(2);
        except:
            print "因为不明原因签到失败";
            sys.exit(3);
        print "签到成功";
        print self.email,'已经连续签到..',result,'天';


if __name__ == '__main__':
    user = xiami('email','password');
    user.login();
    user.signin();
