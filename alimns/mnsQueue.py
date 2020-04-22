import sys
from alimns.common import MNSSampleCommon
from mns.account import Account
from mns.queue import *


class MNSQueue:
    def __init__(self):
        accid, acckey, endpoint, token = MNSSampleCommon.LoadConfig()

        # 初始化 my_account, my_queue
        my_account = Account(endpoint, accid, acckey, token)
        self.queue_name = sys.argv[1] if len(sys.argv) > 1 else "MySampleQueue"
        self.my_queue = my_account.get_queue(self.queue_name)
        base64 = False if len(sys.argv) > 2 and sys.argv[2].lower() == "false" else True
        self.my_queue.set_encoding(base64)

    def create_queue(self):
        queue_meta = QueueMeta()
        try:
            queue_url = self.my_queue.create(queue_meta)
            print("Create Queue Succeed! QueueName:%s\n" % self.queue_name)
        except MNSExceptionBase as e:
            if e.type == "QueueAlreadyExist":
                print("Queue already exist, please delete it before creating or use it directly.")
                sys.exit(0)
            print("Create Queue Fail! Exception:%s\n" % e)

    def delete_queue(self):
        try:
            self.my_queue.delete()
            print("Delete Queue Succeed! QueueName:%s\n" % self.queue_name)
        except MNSExceptionBase as e:
            print("Delete Queue Fail! Exception:%s\n" % e)

    def send_message(self, message):
        print(
            "%sSend Message To Queue%s\nQueueName:%s\n" % (10 * "=", 10 * "=", self.queue_name))
        try:
            msg = Message(message)
            re_msg = self.my_queue.send_message(msg)
            print("Send Message Succeed! MessageBody:%s MessageID:%s" % (message, re_msg.message_id))
        except MNSExceptionBase as e:
            if e.type == "QueueNotExist":
                print("Queue not exist, please create queue before send message.")
                sys.exit(0)
            print("Send Message Fail! Exception:%s\n" % e)

    def recvdel_message(self):
        wait_seconds = 10
        print("%sReceive And Delete Message From Queue%s\nQueueName:%s\nWaitSeconds:%s\n" % (
            10 * "=", 10 * "=", self.queue_name, wait_seconds))
        while True:
            # 读取消息
            try:
                recv_msg = self.my_queue.receive_message(wait_seconds)
                print("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (
                    recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id))
            except Exception as e:
                # except MNSServerException as e:
                if e.type == u"QueueNotExist":
                    print("Queue not exist, please create queue before receive message.")
                    sys.exit(0)
                elif e.type == u"MessageNotExist":
                    print("Queue is empty!")
                    sys.exit(0)
                print("Receive Message Fail! Exception:%s\n" % e)
                continue

            # 删除消息
            try:
                self.my_queue.delete_message(recv_msg.receipt_handle)
                print("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
                return str(recv_msg.message_body, encoding="utf-8")
            except Exception as e:
                print("Delete Message Fail! Exception:%s\n" % e)
