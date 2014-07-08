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

class Pinterest():

    def __init__(self,email,pwd):

        self.email = encryption(email);
        print self.email
        self.pwd = encryption(pwd);
        self.cookie = cookielib.LWPCookieJar();
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie);
        opener = urllib2.build_opener (cookie_support);
        urllib2.install_opener (opener);

    login_header = {'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language':'en,zh-CN;q=0.8,zh;q=0.6',
					'Connection':'keep-alive',
                    'Content-Length':300,
					'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',                  
                    'Host':'www.pinterest.com',
                    'Origin':'https://www.pinterest.com',
                    'Referer':'https://www.pinterest.com/login/',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
					'X-APP-VERSION':'6757f6e',
					'X-CSRFToken':'HEBgZtoJHmtDGElu8WVIz2wtDU8dPJV5',
					'X-NEW-APP':1,
					'X-Requested-With':'XMLHttpRequest'
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





    def login(self):
        post_data = {'source_url':'/login/',
                     'data':{"options":{"username_or_email":"guitar2009king@163.com","password":"youzhang000@"},"context":{}},
                     'module_path':'App()>LoginPage()>Login()>Button(class_name=primary, text=Log In, type=submit, size=large)'
                     }		

        post_data = urllib.urlencode(post_data,'utf-8');
        post_data = '%7B%22options%22%3A%7B%22username_or_email%22%3A%22guitar2009king%40163.com%22%2C%22password%22%3A%22youzhang000%40%22%7D%2C%22context%22%3A%7B%7D%7Dmodule_path:App()%3ELoginPage()%3ELogin()%3EButton(class_name%3Dprimary%2C+text%3DLog+In%2C+type%3Dsubmit%2C+size%3Dlarge)'
        print "正在登入....";
        ##请求
        req = urllib2.Request (url = 'https://www.pinterest.com/login/',data = post_data,headers = self.login_header);
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
    user = Pinterest('guitar2009king@163.com','youzhang000@');
    user.login();
    user.signin();
