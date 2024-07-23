import random
import re
from playwright.sync_api import sync_playwright
from xitroo import Xitroo
from multiprocessing import Pool
import time
from raducord import BannerUtils
from colorama import Fore, Style

gray = Fore.LIGHTBLACK_EX
orange = Fore.LIGHTYELLOW_EX
lightblue = Fore.LIGHTBLUE_EX

class log:
    @staticmethod
    def log(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]{Style.RESET_ALL}"
        print(log.center(msg))
        
    @staticmethod
    def ilog(type, color, message):
        msg = f"{gray} [ {color}{type}{gray} ] [ {color}{message}{gray} ]"
        inputmsg = input(log.center(msg) + " ")
        return inputmsg
    
    @staticmethod
    def input(message):
        return log.ilog('i', lightblue, message)

    @staticmethod
    def success(message):
        log.log('+', Fore.GREEN, message)
        
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
    def working(message):
        log.log('-', orange, message)

    @staticmethod
    def center(text, width=80):
        return text.center(width)

def center(text):
    return BannerUtils.center_text(text)

def getMail(username):
    return f"{username}@xitroo.com"

def getUser():
    names = [
        'Brave', 'Clever', 'Witty', 'Loyal', 'Kind', 'Happy', 'Bold', 'Creative',
        'Friendly', 'Gentle', 'Jolly', 'Lively', 'Quick', 'Quiet', 'Silly', 'Smart',
        'Strong', 'Thoughtful', 'Vibrant', 'Wise', 'Zany', 'Adventurous', 'Ambitious',
        'Artistic', 'Calm', 'Charming', 'Cheerful', 'Confident', 'Courageous', 
        'Determined', 'Diligent', 'Dynamic', 'Energetic', 'Enthusiastic', 'Exciting', 
        'Fearless', 'Generous', 'Gracious', 'Humble', 'Imaginative', 'Inquisitive', 
        'Inspiring', 'Intelligent', 'Joyful', 'Keen', 'Passionate', 'Patient', 
        'Perceptive', 'Persistent', 'Playful', 'Polite', 'Resourceful', 'Sincere', 
        'Spontaneous', 'Supportive', 'Talented', 'Unique', 'Vigorous', 'Warm', 
        'Witty'
    ]
    
    u1 = random.choice(names)
    u2 = random.randint(0, 9999)
    u3 = random.choice(names) + u1
    username = f"{u3}_{u2:04d}"
    
    return username

def verify(email):
    while True:
        try:
            xitroo = Xitroo(email)
            mail = xitroo.getLatestMail()
            content = mail.getBodyText()
            url_pattern = re.compile(r'https?://[^\s/$.?#].[^\s]*')
            urls = url_pattern.findall(content)
            if urls:
                log.info(f"Verified --> {email}")
                return urls[0]
        except Exception as e:
            log.working(rf"Waiting For Verify link --> {email}")

def run(playwright):
    while True:
        try:
            browser = playwright.chromium.launch(headless=True, channel="chrome")
            context = browser.new_context()
            p = context.new_page()
            
            p.goto("https://chat.reka.ai/auth/login")
            p.click("div#__next a.chakra-button.css-1ylyzfc")
            
            username = getUser()
            email = getMail(username)
            password = "JustANugget11!"
            
            log.success(rf"Generated --> {email}")
            p.fill("input#email", email)
            p.fill("input#password", password)
            p.click('div.cc199ae96 > button[type="submit"]')

            verification_url = verify(email)
            if verification_url:
                p.goto(verification_url)
                p.click("div#__next div.chakra-stack.css-4z9kv2 > a")
                p.click('span.chakra-checkbox__control.css-t1ovm1')
                p.click('button[type="submit"]')
                
            with open("./output/reka.txt", 'a') as a:
                a.write(f"{email}:{password}\n")
        except Exception as e:
            log.fail(rf"Error Generating --> {email}")
        finally:
            browser.close()

def worker():
    with sync_playwright() as playwright:
        run(playwright)

def generator():
    threads = int(log.input("Threads --> "))

    with Pool(threads) as pool:
        while True:
            results = [pool.apply_async(worker) for _ in range(threads)]
            for result in results:
                result.wait()