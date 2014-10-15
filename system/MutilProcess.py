from multiprocessing import Process
import os

def myget(url):
    print os.getpid(),url

if __name__ == '__main__':
    plist=[]
    for i in ['www.sina.com.cn','www.163.com','www.baidu.com','www.cnblogs.com','www.qq.com','www.douban.com']:
        proc=Process(target=myget,args=(i,))
        plist.append(proc)
    for proc in plist: proc.start()
    for proc in plist: proc.join()
