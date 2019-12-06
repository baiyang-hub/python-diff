import os,sys
#项目添加到环境变量
sys.path.append(os.path.dirname(os.getcwd()))
# ==============查找不同文件，返回绝对路径=====================
import hashlib,threading,time
from conf import conf
# import conf.conf
# #求文件md5值函数
class file_md5(object):
    def __init__(self,file,status):
        self.file=file
        self.status=status
        self.path_list=[]
        self.svn_md5={}
        self.host_md5={}

    #求md5值
    def GetFileMd5(self,filename):
        if not os.path.isfile(filename):
            return
        myhash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    #获取到文件的绝对路径
    def GetPath(self):
        if os.path.isfile(self.file):
            self.path_list.append(self.file)
        else:
            for i in os.walk(self.file):
                try:
                    for f in i[2]:
                        if f.endswith(".java"):
                            continue
                        if f.endswith(".class"):
                            continue
                        j=(i[0]+"\\"+f)
                        self.path_list.append(j)
                except IndexError as Ie:
                    continue
                finally:
                    # print(self.path_list)
                    pass

    #获取到文件名和md5结果
    def result(self):

        if self.status == 1:

            for path in self.path_list:

                md5num=self.GetFileMd5(path)
                #print("文件：",path,"|=======|","md5:",md5num)
                self.svn_md5[path]=md5num

            return self.svn_md5
        else:

            for path in self.path_list:
                md5num = self.GetFileMd5(path)
                #print("文件：", path, "|=======|", "md5:", md5num)
                self.host_md5[path] = md5num

            return self.host_md5




#============================#对比文件内容，生成html结果文件
import sys,difflib,threading,os

class diff_file():

    def GetLines(self,file_name):
        return open(file_name).readlines()

    def diffile(self,file1,file2,html_file):

        txt_line1 = self.GetLines(file1)

        txt_line2 = self.GetLines(file2)

        d = difflib.HtmlDiff()

        html_file=conf.html_file+html_file+".html"
        conf.logger.info(html_file)
        print(html_file)
        fid = open(html_file,'wb')
        text=d.make_file(txt_line1,txt_line2,fromdesc="==SVN==",todesc="==PRD==")
        text=text.encode("utf-8")
        fid.write(text)
        print("OK")
        fid.close()
    def start(self,dict_list):
        thread_list=[]
        for i in dict_list:
            #dict_list=[[],[],[]]
            t=threading.Thread(target=self.diffile,args=(i[0],i[1],os.path.basename(i[0])))
            t.start()
            thread_list.append(t)
        for j in thread_list:
            j.join()


# if __name__=="__main__":
#     list=[["D:\\SVN文件\\code\\bpd\\mbs-code\\uat\\dev-mbs-20170415.iml","D:\\SVN文件\\code\\bpd\\mbs-code\\uat\\dev-mbs-201704151.iml"],]
#     d=diff_file()
#     d.start(list)

#============================================循环

def xunhuan(s1, s2):
    #print("===========xunhuan")
    conf.logger.info("===========xunhuan")
    print("===========xunhuan")
    k_list1=[]
    k_list2=[]
    for k1, v1 in s1.items():
        for k2, v2 in s2.items():
            if os.path.basename(k1) == os.path.basename(k2) and v1 == v2:
                # print("k1===",k1,"K2===",k2)
                # print("v1===",v1,"v2===",v2)
                k_list1.append(k1)
                k_list2.append(k2)
    return k_list1,k_list2

#===========================主方法
def start():
    start_time = time.time()
    d = diff_file()
    svn_file = conf.svn_file
    host_file =conf.host_file
    #print("===========获取svn文件，根目录：", svn_file)
    conf.logger.info("===========获取svn文件，根目录：%s"%(svn_file))
    print("===========获取svn文件，根目录：%s"%(svn_file))
    f1 = file_md5(svn_file, 1)
    f1.GetPath()
    s1 = f1.result()
    #print("===========获取svn文件，根目录：%s"%(host_file))
    conf.logger.info("===========获取prd文件，根目录：%s" % (host_file))
    print("===========获取prd文件，根目录：%s" % (host_file))
    f2 = file_md5(host_file, 2)
    f2.GetPath()
    s2 = f2.result()
    conf.logger.info("===========去除一致文件")
    print("===========去除一致文件")
    k_list1, k_list2 = xunhuan(s1, s2)
    conf.logger.info("svn文件数:%s,与prd相同文件数:%s，prd文件数:%s,与svn相同文件数：%s (第2个和第4个数应该相等)"%(len(s1), len(k_list1), len(s2), len(k_list2)))
    print("svn文件数:%s,与prd相同文件数:%s，prd文件数:%s,与svn相同文件数：%s (第2个和第4个数应该相等)"%(len(s1), len(k_list1), len(s2), len(k_list2)))
    for i in k_list1:
        del s1[i]
    # print("s1======",len(s1))
    for i in k_list2:
        del s2[i]
    # print("s2======", len(s2))
    # ========================================
    if len(s1) == 0 and len(s2) == 0:
        conf.logger.info("===========文件完全一致")
        print("===========文件完全一致")

    else:
        thread_list = []
        same_list1 = []
        same_list2 = []
        conf.logger.info("===========比对文件内容")
        print("===========比对文件内容")
        for k1, v1 in s1.items():
            for k2, v2 in s2.items():
                if os.path.basename(k1) == os.path.basename(k2):
                    t = threading.Thread(target=d.diffile, args=(k1, k2, os.path.basename(k1)))
                    t.start()
                    thread_list.append(t)
                    same_list1.append(k1)
                    same_list2.append(k2)
        for t in thread_list:
            t.join()

        conf.logger.info("===========文件名不同，内容也不同的文件，手动查看")
        print("===========文件名不同，内容也不同的文件，手动查看")
        for i in same_list1:
            del s1[i]
        for i in same_list2:
            del s2[i]
        if len(s1) == 0 and len(s2) > 0:
            conf.logger.info("===========host_file多出文件\n：%s"%(s2.keys()))
            print("===========host_file多出文件\n：%s"%(s2.keys()))
        elif len(s2) == 0 and len(s1) > 0:
            conf.logger.info("===========svn_file多出文件\n%s"%(s1.keys()))
            print("===========svn_file多出文件\n%s"%(s1.keys()))
        else:
            conf.logger.info("===========svn_file多出文件：\n%s\n===========host_file多出文件\n%s"%(s1.keys(),s2.keys()))
            print("===========svn_file多出文件：\n%s\n===========host_file多出文件\n%s"%(s1.keys(),s2.keys()))


    conf.logger.info("use_time:%s"%(time.time() - start_time))
    print("use_time:%s"%(time.time() - start_time))
if __name__=="__main__":
    # d=diff_file()
    # d.diffile("C:\\Users\\bai\Documents\\Tencent Files\\782940374\\FileRecv\\app.txt","C:\\Users\\bai\Documents\\Tencent Files\\782940374\\FileRecv\\b.txt","a")
    start()