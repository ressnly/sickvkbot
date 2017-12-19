import bot

if __name__ == '__main__':
    # functions for login
    def auth_login():
        login = input("Login: ")
        password = input("Password: ")
        return login, password

    def auth_handler():
        key = input("Enter authentication code: ")
        remember_device = True
        return key, remember_device

    # bot loop
    vk_bot = bot.Bot()
    vk_bot.login(auth_login, auth_handler)
    vk_bot.start()
    print("For stop bot just input everything")
    while True:
        if input() is not None:
            vk_bot.close_thread()
            break

