import vk_api
import time
import logger
import loggercontroller
from threading import Thread


class Bot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.active = False
        self.vk_session = None
        self.logger = logger.DataLogger("log")

    def close_thread(self):
        self.active = False

    def login(self, login_func, handler_func):
        # login_func need return: login(str), password(str)
        # handler_func need return: key(str), remember_device(bool)
        log, password = login_func()
        self.active = True
        self.vk_session = vk_api.VkApi(
            log, password,
            auth_handler=handler_func
        )
        try:
            self.vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            self.active = False
            return
        print("Login is successful")

    def _send_message(self, adds, msg):
        self.vk_session.method('messages.send', {'peer_id': adds, 'message': msg})
        try:
            self.logger.log_message(adds, msg, "SEND")
        except vk_api.Captcha as e:
            print(e.get_url())
            key = input("input captcha: ")
            e.try_again(key=key)

    def _log_message(self, adds, msg):
        print("from ", adds, "get: ", msg, " [", time.asctime(), "]")
        try:
            self.logger.log_message(adds, msg, "GET")
        except vk_api.Captcha as e:
            print(e.get_url())
            key = input("input captcha: ")
            e.try_again(key=key)

    def run(self):
        print("Start main loop")
        log_controller = loggercontroller.LogController(self.logger)
        log_controller.start()
        values = {'out': 0, 'count': 100, 'time_offset': 60}
        while self.active:
            response = self.vk_session.method('messages.get', values)
            if response['items']:
                values['last_message_id'] = response['items'][0]['id']
            for item in response['items']:
                chat_id = int(item['user_id'])
                if item.get('chat_id') is not None:
                    chat_id = int(item['chat_id']) + 2000000000
                last_message = item['body']
                last_message = last_message.rstrip()
                last_message = last_message.replace("natural", "roma pidor")
                last_message = last_message.replace("<", "-->")
                self._log_message(chat_id, last_message)
                if last_message[-1:] == "0" or last_message[-1:] == ")":
                    if last_message[-1:] == ')':
                        last_message += "0"
                    else:
                        last_message += ")"
                    self._send_message(chat_id, last_message+")")
                if last_message[-1:] == ".":
                    self._send_message(chat_id, "C:")
            time.sleep(5)
        log_controller.close_thread()
        print("Thread is closed")