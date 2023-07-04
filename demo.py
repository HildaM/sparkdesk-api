from sparkdesk_api.core import SparkAPI


def get_resp_by_api():
    # Set your API Infomation here
    APP_ID = ""
    APISecret = ""
    APIKey = ""
    # ------------------------
    spark = SparkAPI(
        app_id=APP_ID,
        api_key=APIKey,
        api_secret=APISecret,
    )

    # continuously chatting
    history = []
    while True:
        question1 = input("Ask Question: ")
        if question1 == "exit" or question1 == "stop":
            break
        for resp, history in spark.chat_stream(question1, history):
            # End with a null character to achieve the effect of continuous output.
            print("\rAI: ", resp, end="")
            # print("\rHistory: ", history, end="")
        print("")


if __name__ == '__main__':
    # Use SparkDesk API
    get_resp_by_api()
