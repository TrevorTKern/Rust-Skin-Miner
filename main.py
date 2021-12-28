import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

def login(driver):
    #Logs in
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/header/img').click()
    time.sleep(random.randint(2,4))

    #user
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[2]/div/div[2]/div[2]/div/form[1]/input[4]').send_keys('')
    time.sleep(random.randint(2,4))

    #pass
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[2]/div/div[2]/div[2]/div/form[1]/input[5]').send_keys('')
    time.sleep(random.randint(2,4))

    #clicks login
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[2]/div/div[2]/div[2]/div/form[1]/div[4]/input').click()
    time.sleep(random.randint(2,4))

    #2fa box
    twoFA = input('Enter 2FA: ')
    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div/div/form/div[3]/div[1]/div/input').send_keys(twoFA)
    time.sleep(random.randint(2,4))

    #submit
    driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div/div/form/div[4]/div[1]/div[1]').click()
    time.sleep(random.randint(2,4)) 

def claim(driver):
    driver.get('https://www.rustysaloon.com/50x')
    time.sleep(random.randint(2,4))
    
    #faucet
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[1]/div[3]').click()
    time.sleep(random.randint(2,4))
    '''
    #Claim
    driver.find_element_by_xpath('/html/body/div[2]/div/div[6]/div[2]/section[1]/article/div/p').click()
    time.sleep(random.randint(2,4))
    '''
    #2Captcha
    r = requests.get('https://2captcha.com/in.php?key=5066d06537a13b3c1307a8445bf2856d&method=userrecaptcha&googlekey=6LefWTAaAAAAAIeeXuXO0VJ0RjioqSGXbNBvaJc_&pageurl=https://rustysaloon.com/50x')
    time.sleep(random.randint(15,20))
    temp = r.text.split('|')
    capchaID = temp[1]

    while 1:
        res = requests.get('https://2captcha.com/res.php?key=5066d06537a13b3c1307a8445bf2856d&action=get&id={0}'.format(capchaID))
        if res.text != 'CAPCHA_NOT_READY':
            break
        clear('Waiting on captcha')
        time.sleep(5)

    temp = res.text.split('|')
    token = temp[1]

    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{0}';".format(token))

    driver.execute_script('reCaptchaWidgetCallback0()')
    time.sleep(random.randint(2,4))

    if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText') == '0.00': 
        driver.refresh()
        claim(driver)

def bet(driver, bets):
    driver.get('https://www.rustysaloon.com/50x')
    time.sleep(random.randint(2,4))

    while 1:
        if 's' in driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/main/article/h1').get_attribute('innerText'):
            #Max
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/nav/section[1]/article/div[4]/p').click()
            time.sleep(random.randint(2,4))

            #50x
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/section[4]/header').click()
            time.sleep(random.randint(2,4))
            if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText') != '0.00':
                driver.refresh()
                bet(driver, bets)
                break
            bets += 1
            return bets

def betRemaining(driver, withdraws):
    driver.get('https://www.rustysaloon.com/50x')
    bet(driver, bets)
    if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText') != '0.00':
	    withdraw(driver, withdraws)

def withdraw(driver, withdraws):
    #Withdraw
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/a[1]').click()
    time.sleep(random.randint(2,4))

    #Descending
    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/div/div/p').click()
    time.sleep(random.randint(2,4))

    bal = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText')
    cost = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/article/div[1]/article/b[2]').get_attribute('innerText')
    if float(cost) > float(bal):
        betRemaining(driver)
        return

    remainder = 0
    i = 1
    while 1:
        bal = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText')
        cost = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/article/div[{0}]/article/b[2]'.format(i)).get_attribute('innerText')
        if float(cost) == float(bal):
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/article/div[{0}]/div'.format(i)).click()
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/nav/div[2]/b').click()
            withdraws[1] += float(cost)
            break
        elif float(cost) > float(bal):
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/article/div[{0}]/div'.format(i-1)).click()
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/nav/div[2]/b').click()
            remainder = 1
            withdraws[1] += float(driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/section/article/div[{0}]/article/b[2]'.format(i-1)).get_attribute('innerText'))
            break
        i += 1
    time.sleep(random.randint(2,4))

    #open trades
    driver.get('https://steamcommunity.com/id/obamanablesnowman/tradeoffers')
    time.sleep(random.randint(2,4))

    #opens offer
    onclick = driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[2]/div/div[2]/div[1]/div[2]/div[4]/div[1]').get_attribute('onclick')
    split = onclick.split('\'')
    offerID = split[1]
    driver.get('https://steamcommunity.com/tradeoffer/{0}/'.format(offerID))
    time.sleep(random.randint(2,4))

    #confirm content
    driver.execute_script('ToggleReady(true)')
    time.sleep(random.randint(2,4))

    #trade
    driver.execute_script('ConfirmTradeOffer()')
    time.sleep(random.randint(2,4))

    withdraws[0] += 1
    driver.get('https://rustysaloon.com')

    if remainder == 1:
        betRemaining(driver)
    return withdraws

def clear(x):
    print('\n' * 20)
    f = open('title.txt')
    lines = f.readlines()
    for line in lines:
        print(line, end='')
    print('\n' * 11)
    if x != '':
        print(x)

clear('Starting...')
display = Display(visible=0, size=(1920,1080))
display.start()

options = Options()
options.add_argument('--window-size=1920,1080')
options.add_argument('--start-maximized')
#options.add_argument('user-data-dir=./session')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_extension('./2captcha.crx')

driver = webdriver.Chrome(options = options)

driver.get('https://www.rustysaloon.com')
time.sleep(random.randint(2,4))

clear('Logging in')
login(driver)

bets = 0
withdraws = [0, 0]

while 1:
    clear('Claiming Faucet')
    claim(driver)
    '''
    #exits faucet
    driver.find_element_by_xpath('/html/body/div[2]/div/div[6]/div[2]/header/h1').click()
    time.sleep(random.randint(2,4))
    '''
    clear('All in Baby Fuck')
    bets = bet(driver, bets)
   
    clear('Bet placed waiting for roll')
    time.sleep(random.randint(26,34))

    #checks for win
    if driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/section[2]/div/b').get_attribute('innerText') != '0.00':
        clear('Withdrawing...')
        withdraws = withdraw(driver, withdraws)
    
    clear('')
    print('Bets Placed: {0} | Withdraws: {1} | Total Winnings: {2}'.format(bets, withdraws[0], withdraws[1]))


    time.sleep(869)
