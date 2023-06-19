import datetime
import json
from webdriver.screenshot import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from create_bot_and_conn import TRIGGER_CHECKER_TIMEOUT

from log.create_loggers import webdriver_logger

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///database/jobs.sqlite')
}

scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")
scheduler.start()


################################
# scheduler.remove_all_jobs()
################################


#######################################################################Примеры запусков
# scheduler.add_job(scheduler_dashboard,  "interval", seconds=1, replace_existing=True, args=[user_id, {'path_screenshot':f'{user_id}_sec_withsec_withfiltr1.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr1', name='sec_withsec_withfiltr1')
# scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=15, minute=44, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name=f'sec_withsec_withfiltr')

async def _sem_scheduler_dashboard(user_id: int, options=dict()):
    
    new_browser = await launch({'headless': True, 'ignoreHTTPSErrors': True, 'autoClose': False,
                                'defaultViewport': {'width': 1920, 'height': 1080}})
    page = (await new_browser.pages())[0]
    sched_options = options.copy()

    await create_page(user_id, options=sched_options, new_browser=page)

    filters_sel = options.get('filters', {})
    new_filters_sel = dict()
    a, b = await get_selectors(user_id, new_browser=page)
    all_selectors = {**a, **b}
    for i in filters_sel.keys():
        ctlkey = all_selectors[i]
        all_values = await get_values(user_id, ctlkey, new_browser=page)
        sel_values = []
        for j in filters_sel[i]:
            sel_values.append(all_values[j])
        new_filters_sel[ctlkey] = sel_values

    sched_options['filters'] = new_filters_sel
    sched_options['security'] = db.get_security(user_id)
    try:
        await send_filter_screen(user_id, options=sched_options, new_browser=page, is_scheduler = True)
    except KeyError as e:
        if e.args[0] == 'S_security':
            await bot.send_message(user_id, _(user_id)('security_key_error'))
            return
    except TimeoutError as e:
        if e.args[0] == 'Session is dead':
            await bot.send_message(user_id, _(user_id)('session_is_dead'))
            return
    except:
        webdriver_logger.exception(f'\tuser_ID:{user_id}')
    finally:
        await new_browser.close()


async def scheduler_dashboard(user_id: int, options=dict()):
    '''Create scheduler on dashboard
    
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
    * ``path_screenshot`` (str): path to save screenshot
    * ``security`` (list): values to apply of security selector 
    * ``filters`` (dict): dict of ``selector``(str): ``values name``(list) to apply  
    * ``docType`` (str): type of the document
    * ``language`` (str): language of bot

    Available options to scheduler.add_job:

    * ``func`` 
    * ``args`` (int): args for ``func``
    * ``hour`` (int)
    * ``minute`` (int)
    * ``day_of_week`` (str)
    * ``id`` (int): id of job
    * ``name`` (int): name of job
    * ``misfire_grace_time`` (int): seconds after the designated runtime that the job is still 
            allowed to be run (or ``None`` to allow the job to run no matter how late it is)
    * ``trigger`` (str): the alias name of the trigger (e.g. ``date``, ``interval`` or ``cron``), in which case
            any extra keyword arguments to this method are passed on to the trigger's constructor
    * ``replace_existing`` (bool): ``True`` to replace an existing job with the same ``id``
    
    scheduler.add_job(scheduler_dashboard, "cron", day_of_week='mon-sun', hour=17, minute=46, misfire_grace_time = None, replace_existing=True, args=[user_id, {'docID': '18C63CAE4B8268E07E3DAEA5E275BCC3', 'path_screenshot':f'{user_id}_sec_withsec_withfiltr.png', 'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'],'filters': {'Актер':['PENELOPE','BOB']}}],id=f'{user_id}_sec_withsec_withfiltr', name=f'sec_withsec_withfiltr')
    '''
    async with sem_scheduler:
        # print('start sched')
        await _sem_scheduler_dashboard(user_id, options)



async def _sem_trigger_scheduler():
    webdriver_logger.info('Checking trigger is started')
    all_triggers = db.get_all_triggers()
    for row in all_triggers:
        try:
            if not row['date_trigger']:
                continue
            if row['date_trigger'] > row['date_last_update']:
                options = {'docID': row['document_id'], 'path_screenshot': f"{row['ID']}_{row['document_id']}.png", 'filters': json.loads(row['document_filters'])}
                asyncio.get_event_loop().create_task(scheduler_dashboard(row['user_id'], options=options))
                db.insert_date_last_update(row['ID'], datetime.datetime.now())
        except:
            webdriver_logger.exception(f"Trigger_id:{row['ID']}")
    webdriver_logger.info('Checking trigger is complete')
    
scheduler.add_job(_sem_trigger_scheduler, "interval", minutes=TRIGGER_CHECKER_TIMEOUT, misfire_grace_time = None, replace_existing=True, id = f'trigger_scheduler')

def get_user_jobs(user_id: str) -> list:
    '''Get list of user's job
    
    Available options are:

    * ``user_id`` (int): userID from TG
    '''
    job_list = []
    for job in scheduler.get_jobs():
        if job.id.startswith(user_id):
            job_list.append(job)
    return job_list


def delete_job(job_id):
    scheduler.remove_job(job_id)


def get_jobs_name(jobs) -> list:
    '''Get list of jobs' name
    
    Available options are:

    * ``jobs`` (list): list of jobs
    '''
    job_name = []
    for job in jobs:
        job_name.append(job.name)
    return job_name
