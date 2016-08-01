#encoding=utf-8
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path
import smtplib
import mailConfig

def sendMail(fileName):
    fromAddr = mailConfig.From
    toAddrs = mailConfig.To
    mail_subject = 'smtplib test'
    mail_content = 'smtplib test: hello, smtplib ! Can you see it ?'
    #file_name = mailConfig.file_name
    file_name = fileName

    #仅smtp服务器需要验证时
    server = smtplib.SMTP(mailConfig.smtp_server)
    server.login(mailConfig.username,mailConfig.password)

    #构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()

    #构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = email.MIMEText.MIMEText(mail_content)
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype,subtype = contype.split('/',1)

    #读入文件内容并格式化
    data = open(file_name,'rb')
    base_msg = email.MIMEBase.MIMEBase(maintype,subtype)
    base_msg.set_payload(data.read())
    data.close()
    email.Encoders.encode_base64(base_msg)

    #设置附件头
    basename = os.path.basename(file_name)
    base_msg.add_header('Content-Disposition','attachment',filename = basename)
    main_msg.attach(base_msg)

    # 设置根容器属性
    main_msg['From'] = fromAddr
    main_msg['To'] = toAddrs
    main_msg['Subject'] = mail_subject
    main_msg['Date'] = email.Utils.formatdate()

    # 得到格式化后的完整文本
    fullText = main_msg.as_string()

    #用smtp发送邮件
    try:
        server.sendmail(fromAddr, toAddrs, fullText)
    finally:
        server.quit()
