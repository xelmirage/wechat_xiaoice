#!/usr/bin/env python
# coding: utf-8
#-*- coding: UTF-8 -*-
import os
from wxbot import *
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')
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
    valid_id_list=[]
    cfg_file='xiaoice.ini'
    processing=0

    def __init__(self):
        WXBot.__init__(self)
        self.robot_switch=False
        try:
            file=open(MyWXBot.cfg_file,'r')
            valid_string=file.readline()
            valid_string.encode('utf8')
            MyWXBot.valid_id_list=valid_string.split(',')
            for s in MyWXBot.valid_id_list:
                print s
        except:
            pass
        

    def show_list(self):
        valid_string = ''
        for s in self.valid_id_list:
            valid_string = valid_string + s + ' ,'
        valid_string = valid_string[0:-1]
        self.send_msg_by_uid(valid_string, u'filehelper')

    def wirte_ini(self):
        cfg_string=''
        for s in MyWXBot.valid_id_list:
            cfg_string=cfg_string+s+','
        cfg_string=cfg_string[0:-1]
        print 'about to write:',cfg_string
        file=open(MyWXBot.cfg_file,"w")
        file.write(cfg_string)
        file.close()

    def isUserInList(self,name):
        for s in MyWXBot.valid_id_list:
            try:
                idx=name.index(s)
                return True
            except:
                pass
        return False
    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if (msg['msg_type_id'] == 1):
            self.handle_command(msg)
        elif (msg['msg_type_id'] == 5):


            if msg['content']['type'] == 0 :


                self.send_msg_by_uid(msg['content']['data'], MyWXBot.lastid)
            elif msg['content']['type'] == 3\
            or msg['content']['type'] == 6:


                fn=get_msg_img(self,msg['msg_id'])
                send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), MyWXBot.lastid)
        elif (msg['msg_type_id'] == 4 ) :

            if MyWXBot.isUserInList(self,msg['user']['name']):
                if msg['content']['type'] == 0:


                #self.send_msg_by_uid(u'hi', msg['user']['id'])
                    self.send_msg_by_uid(msg['content']['data'], u'ms-xiaoice')
                    MyWXBot.lastid=msg['user']['id']
                elif msg['content']['type'] == 3\
                or msg['content']['type'] == 6:

                    fn=get_msg_img(self,msg['msg_id'])
                    send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), u'ms-xiaoice')

                    MyWXBot.lastid=msg['user']['id']





        elif (msg['msg_type_id'] == 3) :


            if MyWXBot.isUserInList(self, msg['user']['name']):

                if msg['content']['type'] == 0:
                    self.send_msg_by_uid(msg['content']['desc'], u'ms-xiaoice')
                    MyWXBot.lastid=msg['user']['id']
                elif msg['content']['type'] == 3\
                or msg['content']['type'] == 6:
                    fn=get_msg_img(self,msg['msg_id'])
                    send_img_msg_by_uid(self,os.path.join(self.temp_pwd,fn), u'ms-xiaoice')

                    MyWXBot.lastid=msg['user']['id']

    def handle_command(self, msg):
        msg_data = msg['content']['data']

        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开',u'end']
        start_cmd = [u'出来', u'启动', u'工作',u'begin']
        command_list=msg_data.split(' ')

        if command_list[0]=='add':
            if command_list[1]!='':
                try:
                    MyWXBot.valid_id_list.index(command_list[1])
                    print 'system:user already exists'
                except:

                    MyWXBot.valid_id_list.append(command_list[1])
                    self.wirte_ini()
                    print u'[add]', command_list[1]
                    self.show_list()

        elif command_list[0]=='del':
            if command_list[1] != '':
                try:
                    idx=MyWXBot.valid_id_list.index(command_list[1])
                    del (MyWXBot.valid_id_list[idx])
                    self.wirte_ini()
                    print u'[del]', command_list[1]
                    self.show_list()
                except:
                    print 'system:no such user'
        elif command_list[0] == 'list':
            self.show_list()
        else:
            if self.robot_switch:
                for i in stop_cmd:
                    if i == msg_data:
                        self.robot_switch = False
                        #self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])

                        # print u'[Robot]' + u'机器人已关闭！'
                        self.show_message('Robot', u'机器人已关闭！')
            else:
                for i in start_cmd:
                    if i == msg_data:
                        self.robot_switch = True
                        #self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])
                        #print u'[Robot]' + u'机器人已开启！'
                        self.show_message('Robot',u'机器人已开启！')

    def show_message(self,source,message):
        string = '['+source+'] '+message
        self.send_msg_by_uid(string, u'filehelper')
        print string
   
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
