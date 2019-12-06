
#svn文件位置注意双斜杠
svn_file="D:\\SVN文件\\code"
#prd文件位置
host_file="D:\\SVN文件\\code1"
#比对结果生成文件位置，是result文件位置的绝对路径
html_file="D:\\untitled\\Diff\\result\\"


import time
import logging

#生成的日志文件位置
LOG_FILENAME = 'D:\\untitled\\Diff\\log\\log.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
logger = logging.getLogger()
