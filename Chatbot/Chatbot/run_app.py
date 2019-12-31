from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/restaurantnlu')
agent = Agent.load('models/dialogue', interpreter=nlu_interpreter)

print("Your bot is ready to talk! Type your messages here or send 'stop'")
while True:
    a = input()
    if a == 'stop':
        break
    responses = agent.handle_message(a)
    for response in responses:
        print(response["text"])