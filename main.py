from flask import request,Flask
from  requests_html import HTMLSession

app = Flask(__name__,static_url_path='')
session = HTMLSession()
args = {"query":"","counter":1,"lang":"zh-CNS"}

@app.route('/cc/zoomapi', methods=['POST'])
def cc_zoom():
    args["query"] = request.get_json()["zoomapi"]
    return "ok"

@app.route('/cc/xunfei', methods=['POST'])
def cc_xunfei():
    data = request.get_json()
    args["counter"] = args["counter"] + 1
    url = "{}&seq={}&lang={}".format(args["query"],args["counter"],args["lang"])
    print(url)
    try:
        response = session.post(url = url, data=data["data"].encode(), headers={'Content-Type':'text/plain'})
        print(response.content)
    except Exception as err:
        print(err)
    return "ok"

if __name__ == '__main__':
    app.run()