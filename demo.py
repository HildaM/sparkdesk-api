from sparkdesk_api.core import SparkAPI
from sparkdesk_web import web
from sparkdesk_web.core import SparkWeb

sparkAPI = SparkAPI(
    app_id="",
    api_key="",
    api_secret="",
)



sparkWeb = SparkWeb(
    cookie="",
    fd="",
    GtToken=""
)


def get_resp_by_api():
    question = input("User: ")
    print("\nAI: ", sparkAPI.chat(question))


def api_chatting():
    history = []
    print("Enter exit or stop to end the converation.\n")
    while True:
        query = input("User: ")
        if query == "exit" or query == "stop":
            break
        for response1, history1 in sparkAPI.chat_stream(query, history):
            print("\rAI: ", response1, end="")
        print("")


def web_chatting():
    sparkWeb.chat_stream()


if __name__ == '__main__':
    # Use SparkDesk API
    # get_resp_by_api()

    # terminal chatting
    # api_chatting()
    # ----------------------------

    # Use SparkDesk Web
    sparkWeb.chat_stream()