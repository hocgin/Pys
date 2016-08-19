# coding=utf-8
import email
import os
import re
import smtplib
import urllib2
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailUtil(object):
    # @param to 接收邮箱地址, 支持数组
    # @param title 邮件标题
    # @param text 邮件内容(请使用HTML编码)
    # @param file_paths 多附件
    # @param images_path 使用（本地/网络）图片, 突破邮件服务商添加外链是无效的情况
    #         使用方式: {'imgKey': '/home/hocgin/Downloads/7_闭嘴.gif'}  HTML: <img src="cid:imgKey"
    #         *注: cid 最好不要使用中文
    # @param sender 发件人昵称
    # @param account 发件人账户
    # @param password 发件人密码
    # @param smtp_host SMTP地址
    # @param port SMTP端口
    @classmethod
    def send_email(cls, to, title,
                   text='', file_paths=None, images_path=None,
                   sender='', account='test@hocg.in', password='Test123456',
                   smtp_host='smtp.exmail.qq.com', port=25):
        if images_path is None:
            images_path = {}
        if file_paths is None:
            file_paths = []

        message = MIMEMultipart('related')
        if (file_paths.__len__() != 0):
            # 添加html文本
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)
            # 添加附件
            for file_path in file_paths:
                file_data = open(file_path, 'rb')
                # 构造MIMEBase对象做为文件附件内容并附加到根容器
                mime_file = email.MIMEBase.MIMEBase(maintype, subtype)
                mime_file.set_payload(file_data.read())
                file_data.close()
                email.Encoders.encode_base64(mime_file)
                os.path.basename(file_path)
                mime_file.add_header('Content-Disposition',
                                     'attachment', filename=os.path.split(file_data.name)[1])
                message.attach(mime_file)
            message['Date'] = email.Utils.formatdate()

        text_message = MIMEMultipart('alternative')
        message.attach(text_message)
        text_message.attach(MIMEText(text, 'html', _charset='utf-8'))
        # CID图片
        if (images_path.__len__() != 0):
            for image_key in images_path.keys():
                image_path = images_path[image_key]
                if re.match('^https?:\/\/(([a-zA-Z0-9_-])+(\.)?)*(:\d+)?(\/((\.)?(\?)?=?&?[a-zA-Z0-9_-](\?)?)*)*$',
                            image_path):  # 网络图片
                    try:
                        image_data = urllib2.urlopen(image_path)
                    except urllib2.HTTPError, e:
                        print '读取网络图片(' + image_path + ')发生错误(' + str(e.code) + '): ' + e.msg
                        continue
                else:  # 本地图片
                    image_data = open(image_path, 'rb')
                mime_image = MIMEImage(image_data.read())
                image_data.close()
                mime_image.add_header('Content-ID', '<' + image_key + '>')
                message.attach(mime_image)

        message['Subject'] = title
        message['From'] = sender.__len__() != 0 and sender or account
        message['To'] = ','.join(to)

        smtp = smtplib.SMTP(timeout=20)
        smtp.connect(smtp_host, port)
        smtp.login(account, password)
        smtp.sendmail(account, to, message.as_string())
        smtp.close()
