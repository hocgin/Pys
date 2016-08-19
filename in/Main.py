# coding=utf-8
import smtplib
from hocg.py.utils import EmailUtil
# This is Demo

try:
    EmailUtil.send_email(to=["support@hocg.in"],
                               title="222",
                               text='<h5>hello world</h5><img src="cid:bz"/>',
                               file_paths=["/home/hocgin/Downloads/7_闭嘴.gif", "/home/hocgin/Downloads/7_闭嘴.gif"],
                               images_path={
                                   'bz': "http://7xs6lq.com1.z0.glb.clouddn.com/chat-1.png",
                                   'cc': "http://7xs6lq.com1.z0.glb.clouddn.com/Extr",
                                   'ee': "http://7xs6lq.com1.z0.glb.clouddn.com/Extr",
                                   'aa': "http://7xs6lq.com1.z0.glb.clouddn.com/Extr",
                                   'eee': "http://7xs6lq.com1.z0.glb.com/Extr"
                               },
                               sender="hocg.in官方邮件<support@hocg.in>")
except smtplib.SMTPException, e:
    print "Error: " + e.args[0].__str__()
    print "Message: " + e.args[1]
