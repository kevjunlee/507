import random

def question():
    question_asked = input("What is your question: ")
    print(question_asked)
    check_question(question_asked)


answers = ['It is certain.', 'It is decidedly so.', 'Without a doubt', 'Yes - definitely.', 'You may rely on it', 'As i see it, yes.', 'Most likely', 'Outlookgood.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Dont count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']

random.choice(answers)

def check_question(question):
    if question.endswith('?'):
        print(random.choice(answers))
    else:
        while True:
            new_input = input("I am sorry, I can only answer questions. What is your question? ")
            if new_input.endswith('?'):
                print(random.choice(answers))
                break
            elif new_input == "quit":
                break



question()
