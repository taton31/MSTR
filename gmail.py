import imaplib
import email
from email import policy
import datetime
from time import sleep
import dotenv, os
from log.create_loggers import gmail_logger
from database.user_database import DB, sqlite3


dotenv.load_dotenv('keys.env')

CHECK_TIMEOUT_SEC = 10
FROM_EMAIL  = os.environ.get('EMAIL')
FROM_PWD    = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


def read_email_from_gmail():
    db = DB('database/bot_database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
    mail.login(FROM_EMAIL, FROM_PWD)
    gmail_logger.info('Create connection with gmail')
    while True:
        try:
            gmail_logger.info('Start check gmail')
            
            mail.select('inbox')
            
            result, data = mail.search(None, 'UNSEEN')
        
            ids = data[0]
            id_list = ids.split()

            for id in id_list:
                result, data = mail.fetch(id, "(RFC822)")
                raw_email = data[0][1]
                raw_email_string = raw_email.decode()

                email_message = email.message_from_string(raw_email_string, policy=policy.default)
                message_from = email.utils.parseaddr(email_message['From'])

                if message_from[1] == 'DistributionServices@MicroStrategy.com':
                    title = email_message['Subject'].split(';')
                    trigger_name = title[0].strip()
                    date_time = datetime.datetime.strptime(';'.join(title[1:]), "%Y-%m-%d;%H.%M.%S")
                    all_triggers = db.get_triggers_by_name(trigger_name)
                    if all_triggers:
                        for row in all_triggers:
                            db.insert_date_trigger(row['ID'], date_time)

                    gmail_logger.info(f'Update trigger: {trigger_name}, {date_time}')
        except Exception as e:
            gmail_logger.exception(f'Error gmail with trigger:{trigger_name}')
        
        gmail_logger.info('Gmail has been verified')

        
        sleep(CHECK_TIMEOUT_SEC)
