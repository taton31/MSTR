from mstrio.connection import Connection
from mstrio.project_objects import list_reports, list_documents
from mstrio.distribution_services import list_subscriptions
from mstrio.distribution_services.subscription.email_subscription import EmailSubscription

import mstrio.config as conf
conf.verbose = False

import dotenv

import os

from log.create_loggers import connection_logger

dotenv.load_dotenv('keys.env')

url = os.environ.get('SERVER_LINK') + '/MicroStrategyLibrary/api/'
mstr_username = os.environ.get('LOGIN')
mstr_password = os.environ.get('PASSWORD')
project_name = os.environ.get('PROJECT')


def get_connection():
    try:
        conn = Connection(base_url=url, username=mstr_username, password=mstr_password, login_mode=1, project_name=project_name)
        connection_logger.info(f'Create connection to MSTR: {url}')
        return conn
    except Exception as e:
        connection_logger.exception(f"Connection to MSTR {url} is failed ({project_name}, {mstr_username})")
        raise e


def get_list_subscription(connection, **filters):
    all_subs = list_subscriptions(connection=connection, project_name=project_name, **filters)
    return all_subs
        

def search_report(connection, report_name):
    reports = list_reports(connection, name_begins=report_name)
    return reports


def search_document(connection, doc_name):
    documents = list_documents(connection, doc_name)
    return documents

def get_document_name_by_id(connection, id):
    document = list_documents(connection, id=id)
    if not document:
        report = list_reports(connection, id=id)
        if not report:
            return "Not found"
        else: 
            return report[0].name
    else:
        return document[0].name


def search_report_by_id(connection, id):
    reports = list_reports(connection, id=id)
    return reports


def search_document_by_id(connection, id):
    documents = list_documents(connection, id=id)
    return documents


'''
def get_report(connection, report_id):
    my_report = Report(connection=connection, id=report_id, parallel=False)
    return my_report


def get_report_attributes(connection, report_id):
    report_attributes = Report(connection=connection, id=report_id, parallel=False).attributes
    return report_attributes


def get_report_metrics(connection, report_id):
    report_metrics = Report(connection=connection, id=report_id, parallel=False).metrics
    return report_metrics


def get_report_attr_elements(connection, report_id):
    attr_elements = Report(connection=connection, id=report_id, parallel=False).attr_elements
    return attr_elements'''
