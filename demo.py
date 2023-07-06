from sparkdesk_api.core import SparkAPI

APP_ID = ""
APISecret = ""
APIKey = ""

spark = SparkAPI(
    app_id=APP_ID,
    api_key=APIKey,
    api_secret=APISecret,
)


def get_resp_by_api():
    question = input("User: ")
    print("\nAI: ", spark.chat(question))


def chatting():
    history = []
    print("Enter exit or stop to end the converation.\n")
    while True:
        query = input("User: ")
        if query == "exit" or query == "stop":
            break
        for response1, history1 in spark.chat_stream(query, history):
            print("\rAI: ", response1, end="")
        print("")


if __name__ == '__main__':
    # Use SparkDesk API
    # get_resp_by_api()

    # terminal chatting
    chatting()