from webdriver.page_interaction import *
from create_bot_and_conn import db, bot, SERVER_LINK, LOGIN, PASSWORD, PROJECT, SERVER, HARD_SECURITY_MODE, RUN_LIMIT_BOT, RUN_LIMIT_SCHEDULER, COUNT_CHECK_PAGE_LOAD, MAX_TIME_CHECK_PAGE_LOAD
from aiogram.types import InputFile
import os

from translate import _

import asyncio

from log.create_loggers import webdriver_logger

sem_bot = asyncio.Semaphore(RUN_LIMIT_BOT)
sem_scheduler = asyncio.Semaphore(RUN_LIMIT_SCHEDULER)


DOC_PAGE_COMPLITE_JS = '''
                    if (typeof mstrApp !== 'undefined') {
                        mstrApp.isWaiting()
                    }
                    else {
                        true
                    }
                    '''

REP_PAGE_COMPLITE_JS = '''
                    if (typeof (document.readyState) !== 'undefined' && document.readyState == 'complete') {
                        false 
                    }
                    else {
                        true
                    }
                    '''

async def _sem_create_page(user_id, options=dict(), new_browser = None):


    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    path = options.get('path', f'{SERVER_LINK}/MicroStrategy/servlet/mstrWeb') # https://dashboard-temp/MicroStrategy/servlet/mstrWeb
    docID = options.get('docID', 'C4DB9BA7BF457B5B6D345090FF2BA99F')
    docType = options.get('docType', 'document')
    server = options.get('Server', SERVER)
    project = options.get('Project', PROJECT)
    login = options.get('login', LOGIN)
    password = options.get('password', PASSWORD)
    headless = options.get('headless', True)

    evt_temp = '2048001' if docType == 'document' else (
                '4001' if docType == 'report' else (
                '3140' if docType == 'dossier' else 'error'))
    evt = options.get('evt', evt_temp)
    

    
    path += '?evt=' + evt + '&src=mstrWeb.' + evt
    path += '&' + ('document' if docType == 'dossier' else docType) + 'ID=' + docID + '&currentViewMedia=1&visMode=0&'
    path += 'Server=' + server + '&'
    path += 'Project=' + project + '&Port=0&share=1&'
    path += 'uid=' + login + '&' + 'pwd=' + password
    path += '&hiddensections=path,dockTop,dockLeft,footer'

    if not new_browser:
        page = await create_browser(user_id, headless = headless)
    else: 
        page = new_browser
    

    await page.goto(path, {'timeout': timeout_long})
    ############################ press 'continue'
    # await page.waitForSelector('#\\33 054', {'timeout': timeout_long,'visible': True})
    # await page.click('#\\33 054')
    ############################
    if (docType == 'document'): 
        await page.waitForSelector('#pageLoadingWaitBox', {'timeout': timeout_long})  # ждем ухода самой загрузки документа и появления загрузки данных борда
    try:
        i = 0
        j = 0
        while i < COUNT_CHECK_PAGE_LOAD:
            page_loading_flag = await page.evaluate(DOC_PAGE_COMPLITE_JS if docType == 'document' else REP_PAGE_COMPLITE_JS)
            if not page_loading_flag:
                i += 1
            else:
                i = 0
            await page.waitFor(1000)
            j += 1
            if j > MAX_TIME_CHECK_PAGE_LOAD:
                raise errors.TimeoutError(j)
    except Exception as e:
        webdriver_logger.exception(f'\tuser_ID:{user_id}')
    
async def create_page(user_id, options=dict(), new_browser = None): 
    """Create new browser.

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``timeout_long`` (int): Maximum navigation time in milliseconds
    * ``timeout_short`` (int): Maximum download time in milliseconds
    * ``path`` (str): path to the MstrWeb
    * ``docID`` (str): id of the opening document
    * ``docType`` (str): type of the document
    * ``server`` (str): Mstr server name
    * ``project`` (str): Mstr project name
    * ``login`` (str): Mstr login
    * ``password`` (str): Mstr password
    * ``evt`` (str): Mstr event (use default to document, report, dossier)

    await create_page(aio.types.User.get_current().id, {'docID': 'EA706ACB43C4530927380DB3B07E0889'})
    """ 
    async with sem_bot:
        #print('start create')
        await _sem_create_page(user_id, options, new_browser)


async def _sem_send_filter_screen(user_id, options=dict(), new_browser = None, is_ctlkey = True, is_scheduler = False):
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    if not (await is_session_alive(user_id,  new_browser)):
        if not new_browser:
            await close_browser(user_id)
        else: 
            page.browser.close()
        raise TimeoutError('Session is dead')


    timeout_long = options.get('timeout_long', 60000)
    timeout_short = options.get('timeout_short', 3000)
    docType = options.get('docType', 'document')
    screen_name = options.get('path_screenshot', f'{user_id}.png')

    security_sel = 'S_security'
    security_val = options.get('security', [])

    filters_sel = options.get('filters', {})

    if (not (security_val or filters_sel)) or docType == 'report':
        await page.screenshot({'path': screen_name})
        if is_scheduler:
            await bot.send_document(chat_id=user_id, document=InputFile(screen_name), caption=_(user_id)('your_scheduler'))
            # await bot.send_message(user_id, _(user_id)('your_scheduler'))
        else:
            await bot.send_document(chat_id=user_id, document=InputFile(screen_name))
        os.remove(screen_name)
        return

    a, b = await get_selectors(user_id, new_browser=page)
    all_selectors = {**a, **b}

    try:
        if security_val:
            ctlkey = (all_selectors)[security_sel]
            tmp = await get_values(user_id, ctlkey, new_browser=page)
            security_ctl_val=[]
            for i in security_val:
                security_ctl_val.append(tmp[i])
            await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(security_ctl_val)}, new_browser=page)
    except Exception as e:
        webdriver_logger.warning(f'\tuser_ID:{user_id}', exc_info = True)
        if HARD_SECURITY_MODE:
            raise e

    try:
        if filters_sel: 
            if is_ctlkey:    
                for i in filters_sel.keys():
                    await request_set_selector(user_id, {'ctlKey': i, 'elemList': list_to_str(filters_sel[i])}, new_browser=page)
            else:
                for i in filters_sel.keys():
                    ctlkey = (all_selectors)[i]
                    tmp = await get_values(user_id, ctlkey, new_browser=page)
                    ctl_val=[]
                    for j in filters_sel[i]:
                        ctl_val.append(tmp[j])
                    await request_set_selector(user_id, {'ctlKey': f'{ctlkey}', 'elemList': list_to_str(ctl_val)}, new_browser=page)
    except:
        webdriver_logger.warning(f'\tuser_ID:{user_id}', exc_info = True)


    await apply_selectors(user_id, new_browser=page)

    if (docType == 'document'): 
        await page.waitForSelector('#pageLoadingWaitBox', {'timeout': timeout_long})  # ждем ухода самой загрузки документа и появления загрузки данных борда
    try:
        i = 0
        j = 0
        while i < COUNT_CHECK_PAGE_LOAD:
            page_loading_flag = await page.evaluate(DOC_PAGE_COMPLITE_JS if docType == 'document' else REP_PAGE_COMPLITE_JS)
            if not page_loading_flag:
                i += 1
            else:
                i = 0
            await page.waitFor(1000)
            j += 1
            if j > MAX_TIME_CHECK_PAGE_LOAD:
                raise errors.TimeoutError(j)

        await page.screenshot({'path': screen_name})
        if is_scheduler:
            await bot.send_document(chat_id=user_id, document=InputFile(screen_name), caption=_(user_id)('your_scheduler'))
            # await bot.send_message(user_id, _(user_id)('your_scheduler'))
        else:
            await bot.send_document(chat_id=user_id, document=InputFile(screen_name))
        os.remove(screen_name)
        return 
    except Exception as e:
        webdriver_logger.exception(f'\tuser_ID:{user_id}')
    return 


async def send_filter_screen(user_id, options=dict(), new_browser = None, is_ctlkey = True, is_scheduler = False):  
    """Send screenshot of the document with filters

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``timeout_long`` (int): Maximum navigation time in milliseconds
    * ``timeout_short`` (int): Maximum download time in milliseconds
    * ``path_screenshot`` (str): path to save screenshot
    * ``security`` (list): values to apply of security selector 
    * ``filters`` (dict): dict of ``selector``(str): ``values id``(list) to apply  
    * ``docType`` (str): type of the document

    await send_filter_screen(aio.types.User.get_current().id)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png','filters': {'Актер':['PENELOPE','BOB'], 'Год':['2006']}}, is_ctlkey=False)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB'], 'Год':['2006']}}, is_ctlkey=False)
    await send_filter_screen(aio.types.User.get_current().id, {'path_screenshot':f'{aio.types.User.get_current().id}_sec_withsec_withfiltr.png','filters': {'IGK719A420311EA16852B700080EF55FCB9':['h4;264614C648E9C743C4283B8137C8D9BA','h5;264614C648E9C743C4283B8137C8D9BA'], 'IGK719A442911EA16852B700080EF55FCB9':['h2006;F65860F746DE5329EC4065B6F888ED7D']}})
    """ 
    async with sem_bot:
        #print('start send')
        await _sem_send_filter_screen(user_id, options, new_browser = new_browser, is_ctlkey = is_ctlkey, is_scheduler = is_scheduler)