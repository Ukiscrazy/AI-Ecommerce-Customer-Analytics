from ai.chatbot import client

try:
    models = client.models.list()
    print("API is working!")
    for model in models:
        print(model.name)
except Exception as e:
    print(e)