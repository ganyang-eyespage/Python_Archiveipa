import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 项目根目录
project_path = '/Users/yanggan/Desktop/jucai-ios-app'
# 编译成功后.app所在目录  其中'/Users/yanggan/Desktop/jucai-ios-app'为项目路径
app_path = '%s/build/Build/Products/Release-iphoneos/JuCaiShengHuo.app' % (project_path)
# 指定项目下编译目录
build_path = 'build'
# 打包后ipa存储目录
targerIPA_parth = '/Users/yanggan/Desktop'

# 项目名称
project_name = 'JuCaiShengHuo'

# ipafilename
ipa_filename = 'JuCaiShengHuo.ipa'

# firm的api token  需要自己申请账号，申请地址->  http://fir.im/apps
fir_api_token = '4a0d2512c33d0a10ca0e59dbd04b45b0'

# 需要自己配置邮件端口号，服务器和对方邮箱地址
#from_addr = "邮件地址"
#password = "邮件密码"
#smtp_server = "smtp.服务器"
#to_addr = "对方邮件地址"


# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd %s;xcodebuild clean' % project_path) # clean 项目
    os.system('cd %s;mkdir build' % project_path)

def build_project():
    print('build release start')
    os.system ('xcodebuild -list')
    os.system ('cd %s;xcodebuild -workspace %s.xcworkspace  -scheme %s -configuration release -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit' % (project_path,project_name,project_name,build_path))
# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在桌面
def build_ipa():
    global ipa_filename
#    ipa_filename = time.strftime('xx_%Y-%m-%d-%H-%M-%S.ipa',time.localtime(time.time()))
    os.system ('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s'%(app_path,targerIPA_parth,ipa_filename))
#上传
def upload_fir():
    if os.path.exists('%s/%s' % (targerIPA_parth,ipa_filename)):
        print('watting...')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system('fir p %s/%s -T %s' % (targerIPA_parth,ipa_filename,fir_api_token))
    else:
        print('没有找到ipa文件')

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发邮件
def send_mail():
    msg = MIMEText('xx iOS测试项目已经打包完毕，请前往 http://fir.im/xxxxx 下载测试！', 'plain', 'utf-8')
    msg['From'] = _format_addr('自动打包系统 <%s>' % from_addr)
    msg['To'] = _format_addr('xx测试人员 <%s>' % to_addr)
    msg['Subject'] = Header('xx iOS客户端打包程序', 'utf-8').encode()

#    pop = poplib.POP3("pop3.mxhichina.com")
#    pop.set_debuglevel(1)            #会打印出debug信息
#    pop.user(from_addr)
#    pop.pass_(password)

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def main():
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()
    # 上传fir
    # upload_fir()
    # 发邮件
#    send_mail() #暂时不用，需要配置企业邮箱的端口号和服务器

# 执行
main()
