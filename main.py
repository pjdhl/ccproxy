from flask import request, Flask
from requests_html import HTMLSession
from ots import OTSClient
from alimns.mnsQueue import MNSQueue

app = Flask(__name__, static_url_path='')
session = HTMLSession()
# args = {"query": "", "counter": 1, "lang": "zh-CNS"}
args = {"query": "", "counter": 1, "lang": "en-US"}
ots_client = OTSClient("ntrans.xfyun.cn")
mns_queue = MNSQueue()


@app.route('/cc/zoomapi', methods=['POST'])
def cc_zoom():
    params = request.get_json()
    args["query"] = params["zoomapi"]
    ots_client.APPID = params["ots_appid"]
    ots_client.APIKey = params["ots_appkey"]
    ots_client.Secret = params["ots_secret"]
    return "ok"


@app.route('/cc/xunfei', methods=['POST'])
def cc_xunfei():
    # data从消息服务mq中获取
    message = request.get_json()['data']
    mns_queue.send_message(message)
    data = mns_queue.recvdel_message()
    print(data)
    if len(data) > 3:
        ots_client.Text = data
        ret = ots_client.call_url()
        if ret and "data" in ret and "result" in ret["data"]:
            cc = ret["data"]["result"]["trans_result"]["dst"]
            args["counter"] = args["counter"] + 1
            url = "{}&seq={}&lang={}".format(args["query"], args["counter"], args["lang"])
            try:
                response = session.post(url=url, data=cc.encode(), headers={'Content-Type': 'text/plain'})
                print(response.content)
            except Exception as err:
                print(err)
    return "ok"


@app.route('/cc/mns/start', methods=['POST'])
def create_queue():
    mns_queue.create_queue()
    return "ok"


@app.route('/cc/mns/stop', methods=['POST'])
def remove_queue():
    mns_queue.delete_queue()
    return "ok"


if __name__ == '__main__':
    app.run()
