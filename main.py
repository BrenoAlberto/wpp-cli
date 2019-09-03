import re
import colorama
from pyfiglet import figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt, style_from_dict)
from MessageSender import MessageSender

colorama.init(autoreset=True)

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#00ff00 bold',
    Token.Instruction: '#00ff00',
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

class NumbersValidator(Validator):
    num_pattern = r".*[0-9].*"

    def validate(self, numbers):
        if len(numbers.text):
            if re.match(self.num_pattern, numbers.text):
                return True
            else:
                raise ValidationError(message="Please provide the numbers", cursor_position=len(numbers.text))
        else:
            raise ValidationError(message="You can't leave this blank", cursor_position=len(numbers.text))


def listNumbers(numbers: str):
    return list(map(int, re.split(r'\s?[, ]\s?', numbers)))

def askMessageInformation():
    questions = [
        {
            'type': 'confirm',
            'name': 'save_session',
            'message': "Save browser session so you just scan the qrcode once"
        },
        {
            'type': 'input',
            'name': 'message',
            'message': 'Message to send'
        },
        {
            'type': 'input',
            'name': 'numbers',
            'message': 'Send to which numbers',
            'validate': NumbersValidator,
            'filter': lambda numbers: listNumbers(numbers)
        },
        {
            'type': 'confirm',
            'name': 'send_image',
            'default': False,
            'message': 'Send image too'
        },
        {
            'type': 'confirm',
            'name': 'send_image_before_msg',
            'message': 'Send image before message',
            'when': lambda answers: answers.get('send_image', True)
        },
        {
            'type': 'input',
            'name': 'image_path',
            'message': 'What is the image path',
            'when': lambda answers: answers.get('send_image', True)
        }
    ]
    answers = prompt(questions, style=style)
    return answers

def log(string, color, font="slant", figlet=False):
    if not figlet:
        print(f'{color}{string}')
    else:
        print(f'{color}{figlet_format(string, font=font)}')

def main():
    log("WhatsApp CLI", color=colorama.Fore.GREEN, figlet=True)
    log("Welcome to WPP CLI", colorama.Fore.GREEN)

    messages_info = askMessageInformation()
    log("Sending messages", colorama.Fore.GREEN)

    msg_sender = MessageSender(messages_info['save_session'])

    messages_info.pop('save_session')

    messages_info.pop('send_image')

    msg_sender.send_msgs(**messages_info)

if __name__ == '__main__':
    main()