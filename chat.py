import random
import time
from playwright.sync_api import sync_playwright
from colorama import Fore, Style

gray = Fore.LIGHTBLACK_EX
orange = Fore.LIGHTYELLOW_EX
lightblue = Fore.LIGHTBLUE_EX

class log:
    @staticmethod
    def slog(type, color, message, time):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ] [ {Fore.CYAN}{time:.2f}s{gray} ]"
        print(log.center(msg))
        
    @staticmethod
    def ilog(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]"
        inputmsg = input(log.center(msg) + " ")
        return inputmsg

    @staticmethod
    def log(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]{Style.RESET_ALL}"
        print(log.center(msg))

    @staticmethod
    def success(message, time):
        log.slog('+', Fore.GREEN, message, time)

    @staticmethod
    def fail(message):
        log.log('X', Fore.RED, message)

    @staticmethod
    def warn(message):
        log.log('!', Fore.YELLOW, message)

    @staticmethod
    def info(message):
        log.log('i', lightblue, message)
        
    @staticmethod
    def input(message):
        return log.ilog('i', lightblue, message)

    @staticmethod
    def working(message):
        log.log('-', orange, message)

    @staticmethod
    def center(text):
        t_width = 80
        textlen = len(text)
        if textlen >= t_width:
            return text
        l_pad = (t_width - textlen) // 2
        return ' ' * l_pad + text

def process(img, q, to):
    retries = 3 

    for i in range(retries):
        try:
            with open("./data/reka.txt", 'r') as r:
                accs = r.readlines()

            info = random.choice(accs).strip().split(":")
            email = info[0]
            password = info[1]

            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True, channel="chrome")
                context = browser.new_context()
                p = context.new_page()

                p.goto("https://chat.reka.ai/auth/login")
                p.click("div#__next a.chakra-button.css-1pwke5d")

                p.fill("input#username", email)
                p.fill("input#password", password)
                p.click('div.cc199ae96 > button[type="submit"]')

                try:
                    p.wait_for_selector('span.chakra-checkbox__control.css-t1ovm1', timeout=3000)
                    p.click('span.chakra-checkbox__control.css-t1ovm1')
                    p.click('button[type="submit"]')
                except:
                    pass

                if img:
                    p.fill("div#__next textarea", str(img))
                    p.keyboard.press("Control+A")
                    p.keyboard.press("Control+C")
                    p.keyboard.press("Backspace")
                    p.keyboard.press("Control+V")
                    
                p.fill("div#__next textarea", q)
                p.keyboard.press('Enter')

                time.sleep(to)
        
                try:
                    answer = p.locator('div#message-list div.text-item_markdown__XA0ZK.css-fc23wu > p').text_content()
                except:
                    pass

                if answer is None:
                    log.warn("No response received, retrying...")
                    browser.close()
                    continue

                e = time.time()
                browser.close()

                return answer
        
        except Exception as e:
            log.fail(f"Error --> {str(e)}")
            time.sleep(2)
    return None

def chatter():
    st = time.time()
    
    img = log.input("Image Link [ leave blank for none ] --> ")
    q = log.input("Prompt --> ")
    to = int(log.input("Timeout [ how long to wait ] --> "))

    resp = process(img, q, to)
    et = time.time()
    log.success(f"Response --> {resp}", round(et-st, 2))
    with open("response.txt", 'w') as r:
        r.write(str(resp))