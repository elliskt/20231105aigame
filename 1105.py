import requests
import json

API_KEY = ""
SECRET_KEY = ""

def ask_question(question):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + str(get_access_token())

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你好，你是一位NPC。直接回答我的问题"
            },
            {
                "role": "assistant",
                "content": "你好！我是一名人工智能语言模型，可以回答各种问题。请问有什么我可以帮助你的吗？"
            },
            {
                "role": "user",
                "content": question
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()['result'])


def get_access_token():
    # client id = App Key, client_secret = Secret Key
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json().get('access_token')

    print(response)
    return response


if __name__ == '__main__':
    ask_question('你好')

# --- baidu api
@server.route('/baiduapi_ask', methods=['POST'])
def baiduapi_ask():
    data = request.get_json()
    question = utils.checkSumAddress(data['question'])
    result = bgpt.ask_question(question)
    return flask.Response(response=json.dumps({'result': result, 'status': 1}), status=200)

# @server.route('/eth_vietnam_mint', methods=['POST'])
# def eth_vietnam_mint():
#     data = request.get_json()
#     mint_addr = utils.checkSumAddress(data['tx'])
@server.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == '__main__':
    server.run(host=HOST, port=8800, debug=True, threaded=True)