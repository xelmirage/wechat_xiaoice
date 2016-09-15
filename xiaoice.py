#!/usr/bin/env python
# coding: utf-8
__author__='xelmirage'
import os
from wxbot import *
def send_img_msg_by_uid(self, fpath, uid):
        mid = self.upload_media(fpath, is_img=True)
        if mid is None:
            return False
        url = self.base_uri + '/webwxsendmsgimg?fun=async&f=json'
        data = {
                'BaseRequest': self.base_request,
                'Msg': {
                    'Type': 3,
                    'MediaId': mid,
                    'FromUserName': self.my_account['UserName'],
                    'ToUserName': uid,
                    'LocalID': str(time.time() * 1e7),
                    'ClientMsgId': str(time.time() * 1e7), }, }
        if fpath[-4:] == '.gif':
            url = self.base_uri + '/webwxsendemoticon?fun=sys'
            data['Msg']['Type'] = 47
            data['Msg']['EmojiFlag'] = 2
        try:
            r = self.session.post(url, data=json.dumps(data))
            res = json.loads(r.text)
            if res['BaseResponse']['Ret'] == 0:
                return True
            else:
                return False
        except Exception,e:
            return False
def get_msg_img(self, msgid):
        """
        获取图片消息，下载图片到本地
        :param msgid: 消息id
        :return: 保存的本地图片文件路径
        """
        url = self.base_uri + '/webwxgetmsgimg?MsgID=%s&skey=%s' % (msgid, self.skey)
        r = self.session.get(url)
        data = r.content
        fn = 'img_' + msgid + '.jpg'
        with open(os.path.join(self.temp_pwd,fn), 'wb') as f:
            f.write(data)
        return fn
class MyWXBot(WXBot):
    lastid = ''
    valid_id_list=[u'ms-xiaoice',u'小冰']
    isValid=0
    processing=0
    def handle_msg_all(self, msg):
        if (msg['msg_type_id'] == 1):

            if msg['content']['data'] == '/begin':
                MyWXBot.isValid=1
                print "begin"
                print MyWXBot.valid_id_list,"\nisValid=",MyWXBot.isValid
            elif msg['content']['data'] == '/end':
                MyWXBot.isValid = 0
                print "end"

        if MyWXBot.isValid==1:
            
            
            if (msg['msg_type_id'] == 4 ) :

                if msg['content']['type'] == 0:


                #self.send_msg_by_uid(u'hi', msg['user']['id'])
                    self.send_msg_by_uid(msg['content']['data'], u'ms-xiaoice')
                    MyWXBot.lastid=msg['user']['id']
                elif msg['content']['type'] == 3\
                or msg['content']['type'] == 6:

                    fn=get_msg_img(self,msg['msg_id'])
                    send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), u'ms-xiaoice')

                    MyWXBot.lastid=msg['user']['id']


            elif (msg['msg_type_id'] == 5):
                if msg['content']['type'] == 0 :


                    self.send_msg_by_uid(msg['content']['data'], MyWXBot.lastid)
                elif msg['content']['type'] == 3\
                or msg['content']['type'] == 6:


                    fn=get_msg_img(self,msg['msg_id'])
                    send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), MyWXBot.lastid)


            elif (msg['msg_type_id'] == 3) :

                if msg['content']['type'] == 0:
                    self.send_msg_by_uid(msg['content']['desc'], u'ms-xiaoice')
                    MyWXBot.lastid=msg['user']['id']
                elif msg['content']['type'] == 3\
                or msg['content']['type'] == 6:
                    fn=get_msg_img(self,msg['msg_id'])
                    send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), u'ms-xiaoice')

                    MyWXBot.lastid=msg['user']['id']


                
   
'''     
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()
