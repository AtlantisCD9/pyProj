#encoding=utf-8
import poplib
import email
import mailConfig

if __name__ == '__main__':
    M = poplib.POP3(mailConfig.pop_server)
    M.user(mailConfig.username)
    M.pass_(mailConfig.password)

    #打印有多少封信
    numMessages = len(M.list()[1])
    print 'num of messages', numMessages

    i = numMessages - 1
    #从最老的邮件开始遍历
#    for i in range(numMessages):
    m = M.retr(i+1)
    msg = email.message_from_string('\n'.join(m[1]))
    #allHeaders = email.Header.decode_header(msg)
    aimHeaderStrs = {'from':'', 'to':'', 'subject':''}
    for aimKey in aimHeaderStrs.keys():
        aimHeaderList = email.Header.decode_header(msg[aimKey])
        for tmpTuple in aimHeaderList:
            if tmpTuple[1] == None:
                aimHeaderStrs[aimKey] += tmpTuple[0]
            else:
                aimHeaderStrs[aimKey] += tmpTuple[0].decode(tmpTuple[1]) #转成unicode
            for aimKey in aimHeaderStrs.keys():
                print aimKey,':',aimHeaderStrs[aimKey].encode('utf-8') #转成utf-8显示

    for part in msg.walk(): #遍历所有payload
        contenttype = part.get_content_type()
        filename = part.get_filename()
        if filename: #and contenttype=='application/octet-stream':
            #保存附件
            data = part.get_payload(decode=True)
            file("./receivedFiles/mail%d.attach.%s" % (i+1,filename),'wb').write(data)
        elif contenttype == 'text/plain':
            #保存正文
            data = part.get_payload(decode=True)
            charset = part.get_content_charset('ios-8859-1')
            file('./receivedFiles/mail%d.txt' % (i+1), 'w').write(data.decode(charset).encode('utf-8'))
