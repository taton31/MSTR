#!/usr/bin/env python
# coding: utf-8
import mstrio
from mstrio.connection import Connection
from mstrio.server import Cluster, ServerSettings
from mstrio.server import Environment, Project, compare_project_settings
'''from mstrio.users_and_groups.user_group import UserGroup, list_usergroups
from mstrio.users_and_groups.user import User, list_users
from mstrio.distribution_services import (ScheduleManager, EmailSubscription, SubscriptionManager,
                                          Content) '''

from mstrio.project_objects import list_dossiers 
import pandas as pd

# '0701C1BA3147300C064B8D9282147A15'
#mstr_tutorial_id = 'B7CA92F04B9FAE8D941C3E9B7E0CD754'
def connect(login = "mstr", password = "kcTCSvc5RGG7", url = "https://env-270933.customer.cloud.microstrategy.com/MicroStrategyLibrary/api/", project_name = 'MicroStrategy Tutorial'):
    conn_prod = Connection(url, login, password, login_mode=1, project_name = project_name)
    env_prod = Environment(connection=conn_prod)
    tutorial_prod = Project(conn_prod, name = project_name)
    return conn_prod


def search_rep(conn, name):
    return mstrio.project_objects.report.list_reports (name_begins = name, connection = conn)

