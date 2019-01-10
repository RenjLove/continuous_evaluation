'''
Use a mongodb to persist the status of this framework.
'''
from db import MongoDB
import _config
import json

db = MongoDB(_config.db_name, host=_config.db_host, port=_config.db_port)


def add_evaluation_record(commitid, date, task, passed, infos, kpis, kpi_values, kpi_types,
                          kpi_objs, detail_infos):
    '''
    persist the evaluation infomation of a task to the database.

    commitid: str
    date: UNIX timestamp
    task: str
    passed: bool
    infos: list of string
    kpis: the kpis in a task, name -> kpivalues
    kpi_objs: objects of KPI.
    '''
    # delete old task record for this commit
    db.remove(_config.table_name, {
        'commitid': commitid,
        'type': 'kpi',
        'task': task,
    })

    # insert new record
    record = {
        'commitid': commitid,
        'date': date,
        'task': task,
        'type': 'kpi',
        'passed': passed,
        'infos': infos,
        'detail_infos': detail_infos,
        'kpis-keys': kpis,
        'kpis-values':
        json.dumps(list(value.tolist() for value in kpi_values)),
        'kpi-types': kpi_types,
        'kpi-activeds': [kpi.actived for kpi in kpi_objs],
        'kpi-unit-reprs': [kpi.unit_repr for kpi in kpi_objs],
        'kpi-descs': [kpi.desc for kpi in kpi_objs],
    }
    db.insert_one(_config.table_name, record)

