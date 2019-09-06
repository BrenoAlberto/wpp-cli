import re
from cli.utils import log, get_conf
from cli.MessageSender import MessageSender
from PyInquirer import (Token, ValidationError, Validator, prompt, style_from_dict)

# ADD ANTI-BAN MODE

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


def list_numbers(numbers: str):
    return list(map(int, re.split(r'\s?[, ]\s?', numbers)))


def ask_message_information():
    questions = [
        {
            'type': 'confirm',
            'name': 'save_session',
            'message': "Save browser session so you just scan the qrcode once",
            'when': lambda f: not bool(get_conf('saved_session'))
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
            'filter': lambda numbers: list_numbers(numbers)
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
            'name': 'img_path',
            'message': 'What is the image path',
            'when': lambda answers: answers.get('send_image', True)
        }
    ]
    answers = prompt(questions, style=style)
    return answers


def start_cli():
    log("WhatsApp CLI", figlet=True)
    log("Welcome to WPP CLI")

    try:
        messages_info = ask_message_information()
        messages_info.pop('send_image')

        log("Sending messages")

        if get_conf('saved_session'):
            messages_info['save_session'] = True

        msg_sender = MessageSender(messages_info['save_session'])
        messages_info.pop('save_session')

        msg_sender.send_msgs(**messages_info)
        msg_sender.exit_browser()
        log('Messages sended')
    except KeyboardInterrupt:
        if isinstance(msg_sender, MessageSender):
            msg_sender.exit_browser()
        log('Program closed from cli')
