#!/opt/ActivePython-2.7/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import ConfigParser
import os,sys,os.path
import time
import logging
import logging.handlers

###########usage#################
###C:\>python send_mail.py "99999" "RHEL57" "/tmp" "ITM" "/tmp文件系统满" "SIT_LZ_DSK_UsedPct" "SIT_KLZ_DISK" "2012-04-08"  "3" "网上银行"
###########usage#################

To = sys.argv.pop().split(";")

abspath = os.path.abspath(sys.argv[0])
dirname = os.path.dirname(abspath)
conffile = dirname + "/send_mail.conf"
logfile = dirname + "/send_mail.log"

######add logging ######
logger = logging.getLogger('send_mail')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(logfile, maxBytes = 2000000, backupCount = 5)
formatter = logging.Formatter(fmt = '%(asctime)s -- %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p' )
handler.setFormatter(formatter)
logger.addHandler(handler)


######add logging ######



cf = ConfigParser.ConfigParser()
cf.read(conffile)

column = cf.items("column")
op_c = cf.options("column")

Host = cf.get("mailconf", "SmtpHost")
Port = cf.get("mailconf", "SmtpPort")
From = User = cf.get("mailconf", "User")
Password = cf.get("mailconf", "Password")
Subject = cf.get("mailconf", "Subject").lower()

i = op_c.index(Subject)
Subject = unicode(sys.argv[i+1],"utf8")


ISOTIMEFORMAT='%Y-%m-%d %X'
if "LastOccurrence".lower() in op_c:
    i = op_c.index("LastOccurrence".lower())
    sys.argv[i+1] = time.strftime( ISOTIMEFORMAT,time.localtime(float(sys.argv[i+1])) )

    
head = ['\n\n', 'Tivoli监控系统收到告警，具体报警内容请参见以下:', '\n\n']
tail = ['\n\n', '此邮件由Tivoli监控系统自动发送,请勿回复', '\n\n']
body = list()
    
f1 = [ x[1] for x in column ]
f2 = sys.argv[1:]

body = [ x + ":" + "\t" + y for x, y in zip(f1, f2) ]
    
MailMsg = '\n'.join(head + body + tail)



#print(MailMsg)
#print(Host,Port,From,User,Password)



######################
def send_mail(To,Subject,MailMsg):
    #msg = MIMEText(content, 'plain', 'gbk')
    msg = MIMEText(MailMsg, 'plain', 'utf8')
    msg['From'] = From
    msg['To'] = ";".join(To)
    msg['Subject'] = Subject
    try:
        s = smtplib.SMTP()
        s.connect(Host, Port)
        #s.set_debuglevel(1)
        s.login(User, Password)
        s.sendmail(From, To, msg.as_string())
        s.close()
	    logger.info('starting send_mail scripte')
	    logger.info("From: %s\nTo: %s\nMsg: %s\n", From, To, MailMsg) 
	    logger.info("send mail successfully")
        #return True
    except Exception, e:
        print str(e)
	logger.info("send mail failed")
        #return False

if __name__ == '__main__':
    send_mail(To, Subject, MailMsg)

