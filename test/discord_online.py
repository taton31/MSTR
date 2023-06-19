
import asyncio
import sys
from turtle import delay
from pyppeteer import launch
import time
import telebot


token = '5098007657:AAEwiPhBn7k-CR8q4FtPSYPJFNwrUEyGDxk'
bot = telebot.TeleBot(token)
    
async def screenshot(options = dict()):

    
    path = 'https://discord.com/channels/@me'
    login = 'anton15456@yandex.ru'
    password = 'fynjy15456'
    login_wind = 'input[aria-label="Email or Phone Number"]'       #'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > div.marginBottom20-315RVT > div > div.inputWrapper-1YNMmM.inputWrapper-3ESIDR > input'
    password_wind = 'input[aria-label="Password"]'                                        #'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > div:nth-child(2) > div > input'
    OK_but= 'button[type="Submit"]'                                                     #'#app-mount > div.app-3xd6d0 > div > div > div > div > form > div > div > div.mainLoginContainer-wHmAjP > div.block-3uVSn4.marginTop20-2T8ZJx > button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F'
    ID_chat = '949580819293425714'
    message_wind_BI = 'div[aria-label="Написать Без имени"]'                            #'#app-mount > div.app-3xd6d0 > div > div.layers-OrUESM.layers-1YQhyW > div > div > div > div > div.chat-2ZfjoI > div.content-1jQy2l > main > form > div > div.scrollableContainer-15eg7h.webkit-QgSAqd > div > div.textArea-2CLwUE.textAreaSlate-9-y-k2.slateContainer-3x9zil'
    BI_but = 'a[href="/channels/@me/949580819293425714"]'
    IREK_but = 'a[href="/channels/@me/697741581196722206"]'
    message = 'hello world!' 
    user_login_tg = '1723464345'    
    print ('Start try')
    try:
        browser = await launch({'args': ['--lang=en_US'], 'headless': options.get('headless', False), 'ignoreHTTPSErrors': options.get('ignoreHTTPSErrors', True), 'defaultViewport': options.get('defaultViewport', {'width': 1920, 'height': 1080})})
        page = await browser.newPage()  
        await page.goto(path)
        await page.waitForSelector(password_wind)

        await page.type(password_wind, password, {delay: 20})
        await page.type(login_wind, login, {delay: 20})
        await page.waitFor(1000)
        await page.click(OK_but)
        await page.waitFor(3000)
        await page.waitForSelector(BI_but)
        await page.click(BI_but)
        await page.waitFor(3000)
        #await page.waitFor(300000)

        await page.waitForSelector(message_wind_BI)
        await page.click(message_wind_BI)
        print('Start loop')
        ############## send message
        while time.localtime().tm_hour > 9 and time.localtime().tm_hour < 19:   
            await page.click(IREK_but)
            await page.waitFor(3000)
            await page.click(BI_but)
            await page.waitFor(3000)
            await page.type(message_wind_BI, str(time.localtime().tm_hour) + ':' +str(time.localtime().tm_min), {delay: 20})
            await page.keyboard.press("Enter")
            print (str(time.localtime().tm_hour) + ':' +str(time.localtime().tm_min))
            await page.waitFor(300000)
            await page.mouse.move(10,10)
        bot.send_message(user_login_tg, 'END TIME discord ' + str(time.localtime().tm_hour) + ':'+str(time.localtime().tm_min))
    except Exception as E:
        print (E)
        bot.send_message(user_login_tg, 'ERROR discord ' + str(time.localtime().tm_hour) + ':'+str(time.localtime().tm_min))
        await page.screenshot({'path': 'screenshots/example.png'})
            
asyncio.get_event_loop().run_until_complete(screenshot())