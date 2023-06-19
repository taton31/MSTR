from pyppeteer import launch, errors
from pyppeteer.page import Page
from create_bot_and_conn import SERVER_LINK

_browsers_list = dict()


async def create_browser(user_id: int, headless = True) -> Page:
    _browsers_list[user_id] = await launch({'headless': headless, 'ignoreHTTPSErrors': True, 'autoClose':False, 'defaultViewport': {'width': 1920, 'height': 1080}})
    page = (await _browsers_list[user_id].pages())[0]
    return page 


async def close_browser(user_id: int):
    if user_id in _browsers_list:
        await _browsers_list[user_id].close()
        _browsers_list.pop(user_id, None)


async def get_browsers_page(user_id: int) -> Page:
    page = (await _browsers_list[user_id].pages())[0]
    return page



async def get_selectors(user_id, new_browser = None):
    """Get all dashboard's selector

    Available options are:

    * ``user_id`` (int): userID from TG
    """ 
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    select_multi = await page.evaluate('''
                                arr_1 = new Object();
                                Object.keys(mstrmojo.all).forEach(function(key) {

                                    try
                                    {
                                        if (mstrmojo.all[key].t == 111 && mstrmojo.all[key].multi){
                                            arr_1[mstrmojo.all[key].n] = mstrmojo.all[key].ckey;
                                        }
                                    }
                                    catch 
                                    {
                                        console.log('1')
                                    }
                                });
                                arr_1
                            ''')
    select_wo_multi = await page.evaluate('''
                                arr_2 = new Object();
                                Object.keys(mstrmojo.all).forEach(function(key) {

                                    try
                                    {
                                        if (mstrmojo.all[key].t == 111 && !mstrmojo.all[key].multi){
                                            arr_2[mstrmojo.all[key].n] = mstrmojo.all[key].ckey;
                                        }
                                    }
                                    catch 
                                    {
                                        console.log('1')
                                    }
                                });
                                arr_2
                            ''')
    return select_multi, select_wo_multi 


async def get_values(user_id, ckey, new_browser = None):
    """Get all values from dashboard's selector

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``ckey`` (str): selector's ctlkey
    """ 
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser
    """
    val = await page.evaluate(f'''
    bbb = new Object()
    z=mstrApp.docModel.getNodeDataByKey('{ckey}').data.elms
    for (i in z)
        {{
            bbb[z[i].n]=z[i].v
        }}
    bbb
    ''')
    """ 
    
    HTML = await page.evaluate('document.body.innerHTML')
    val = dict()
    HTML = HTML[HTML.find('\"k\":\"' + ckey + '\",\"wid\"'):]
    begin = HTML.find('\"elms\":[') + 9
    end = HTML[begin:].find(']') - 1
    values = HTML[begin:begin + end].split('},{')
    for i in values:
        tmp = i
        tmp = tmp[tmp.find('\"v\":\"') + 5:]
        value = tmp[:tmp.find('\"')]
        tmp = tmp[tmp.find('\"n\":\"') + 5:]
        name = tmp[:tmp.find('\"')]
        val[name] = value
    return val

    
async def request_set_selector(user_id, options=dict(), new_browser=None):
    """Send request to change selector's value

    Available options are:

    * ``user_id`` (int): userID from TG
    * ``url`` (str): url to taskProc
    * ``ctlKey`` (str): selector's ctlKey
    * ``elemList`` (str): list of values (concat throught \\u001e)
    """ 
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    url = options.get('url', f'{SERVER_LINK}/MicroStrategy/servlet/taskProc')  # url до taskproc (можно посмотреть через ф12 при прожатии селектора)
    ctlKey = options.get('ctlKey', 'W5121A375615A451CA272FD10697EA8EA')
    elemList = options.get('elemList', 'h29;77ECA0D9445F155A4B08DFAC49FC9624')

    taskid = options.get('taskid', 'mojoRWManipulation')
    rwb = await page.evaluate('mstrApp.docModel.bs')
    messageID = await page.evaluate('mstrApp.docModel.mid')
    mstr_now = await page.evaluate('mstrmojo.now()')
    servlet = await page.evaluate('mstrApp.servletState')
    keyContext = await page.evaluate(f'mstrApp.docModel.getNodeDataByKey("{ctlKey}").defn.ck')
    
    await page.evaluate(f'''
    url = \'{url}\'
    fetch(url, {{
    method: 'POST',
        headers: {{
        'Content-type': 'application/x-www-form-urlencoded',
        }},
    body:"taskId={taskid}&rwb={rwb}&messageID={messageID}&stateID=-1&params=%7B%22actions%22%3A%5B%7B%22act%22%3A%22setSelectorElements%22%2C%22keyContext%22%3A%22{keyContext}%22%2C%22ctlKey%22%3A%22{ctlKey}%22%2C%22elemList%22%3A%22{elemList}%22%2C%22isVisualization%22%3Afalse%2C%22include%22%3Atrue%2C%22tks%22%3A%22W12390BF5EDEF41D8A507193CEF784240%22%7D%5D%2C%22partialUpdate%22%3A%7B%22selectors%22%3A%5B%22W5121A375615A451CA272FD10697EA8EA%22%5D%7D%2C%22style%22%3A%7B%22params%22%3A%7B%22treesToRender%22%3A3%7D%2C%22name%22%3A%22RWDocumentMojoStyle%22%7D%7D&zoomFactor=1&styleName=RWDocumentMojoStyle&taskContentType=json&taskEnv=xhr&xts={mstr_now}&mstrWeb={servlet}"
    }})   
    ''')
    


async def apply_selectors(user_id, new_browser = None):
    """Apply selector changes 

    Available options are:

    * ``user_id`` (int): userID from TG
    """ 
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser

    await page.evaluate('mstrApp.docModel.controller.refresh()')

async def is_session_alive(user_id, new_browser = None):
    """Check session timeout

    Available options are:

    * ``user_id`` (int): userID from TG
    """ 
    if not new_browser:
        page = await get_browsers_page(user_id)
    else: 
        page = new_browser
    
    session_timeout = int(await page.evaluate('''
                try{
                    if (typeof (mstrApp) !== 'undefined') {
                            mstrApp.sessionManager.remainingTime
                        }
                        else {
                            -1
                        }
                    }
                catch {
                    -1
                }
                '''))

    return session_timeout > 30


def list_to_str(value: list) -> str:
    val = value.copy()
    str=val.pop()
    for i in val:
        str+='\\u001e'+i
    return str

"""
async def get_page_by_id(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            return i

async def close_page(user_id: int):
    for i in (await browser.pages()):
        if i.user_id == user_id:
            await i.close()
"""