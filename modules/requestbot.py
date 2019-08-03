"""

"""
import requests
from modules.config import Config
import modules.generateaccountinformation as acc
from modules.getIdentity import getRandomIdentity
import json
import re
from modules.storeusername import store


#custom class for creating accounts
class CreateAccount:
    def __init__(self, email, username, password, name, numberofaccounts, use_custom_proxy, use_local_ip_address, proxy):
        self.sockets = []
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.numberofaccounts = numberofaccounts
        self.use_custom_proxy = use_custom_proxy
        self.use_local_ip_address = use_local_ip_address
        self.url = "https://www.instagram.com/accounts/web_create_ajax/"
        self.referer_url = "https://www.instagram.com/"
        self.proxy = proxy
        # self.headers = {
        #     'accept': "*/*",
        #     'accept-encoding': "gzip, deflate, br",
        #     'accept-language': "en-US,en;q=0.8",
        #     'content-length': "241",
        #     'content-type': 'application/x-www-form-urlencoded',
        #     'origin': "https://www.instagram.com",
        #     'referer': "https://www.instagram.com/",
        #     'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        #     'x-csrftoken': "95RtiLDyX9J6AcVz9jtUIySbwf75WhvG",
        #     'x-instagram-ajax': "c7e210fa2eb7",
        #     'x-requested-with': "XMLHttpRequest",
        #     'Cache-Control': "no-cache",
        # }
        self.__collectcrsf()
        self.__collect_sockets()

    # A function to fetch custom proxies
    def __collect_sockets(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for socket_str in revised_list:
            self.sockets.append(socket_str[:-5].replace("</td>", ":"))

    def __collectcrsf(self):
         r = requests.get('https://instagram.com/accounts/emailsignup/')
         print(r)

    # Account creation function
    def createaccount(self):
        # Account creation payload
        payload = {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'first_name': self.name,
           'seamless_login_enabled' : '1',
            'tos_version' : 'row',
            'opt_into_one_tap' : 'false'
        }

        """
            Check if to use local ip address to create account, then create account based on the amount set in the config.py
        """
        if self.use_custom_proxy is True:
            session = requests.Session()
            if (self.proxy is not None):
                try:
                    session_start = session.get(self.url, proxies={'http' : self.proxy, 'https' : self.proxy});
                    session.headers.update({'referer' : self.referer_url,'x-csrftoken' : session_start.cookies['csrftoken']})

                    create_request = session.post(self.url, data=payload, allow_redirects=True)
                    session.headers.update({'x-csrftoken' : session_start.cookies['csrftoken']})
                    response_text = create_request.text
                    response = json.loads(create_request.text)
                    print(response)
                except Exception as e:
                    print(e)
                    print("---Request Bot --- An error occured while creating account with local ip address")
            else:
                    raise Exception('---Request Bot --- Proxy must to added to proxies.txt list')

def runBot():
    for i in range(Config['amount_of_account']):

        if(Config['use_custom_proxy'] == True):
             with open(Config['proxy_file_path'], 'r') as file:
                content = file.read().splitlines()
                for proxy in content:
                    account_info = {}
                    identity, gender, birthday = getRandomIdentity(country=Config["country"])
                    account_info["name"] = identity
                    account_info["username"] = acc.username(account_info["name"])
                    account_info["password"] = acc.generatePassword()
                    account_info["email"] = acc.genEmail(account_info["username"])
                    account_info["gender"] = gender
                    account_info["birthday"] = birthday
                    print(account_info)
                    account = CreateAccount(
                        account_info['email'],
                        account_info['username'],
                        account_info['password'],
                        account_info['name'],
                        Config['amount_of_account'],
                        Config['use_custom_proxy'],
                        Config['use_local_ip_address'], proxy=proxy)
                    print(proxy)
                    account.createaccount()
        else :
            account_info = {}
            identity, gender, birthday = getRandomIdentity(country=Config["country"])
            account_info["name"] = identity
            account_info["username"] = acc.username(account_info["name"])
            account_info["password"] = acc.generatePassword()
            account_info["email"] = acc.genEmail(account_info["username"])
            account_info["gender"] = gender
            account_info["birthday"] = birthday
            print(account_info)
            account = CreateAccount(
                account_info['email'],
                account_info['username'],
                account_info['password'],
                account_info['name'],
                Config['amount_of_account'],
                Config['use_custom_proxy'],
                Config['use_local_ip_address'])
            account.createaccount()