# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 22:08
# @Author  : tuihou
# @File    : parse.py
from begin import models
from httprunner.api import HttpRunner
from .tools import run_fast


def debug_case(case_obj, debugtalk=None, config=None):
    """ debug case
        case :dict or list
    """
    case = case_obj['case_steps']
    case_name = case_obj['case_name']

    if len(case) == 0:
        return 'Error, No case'

    if isinstance(case, dict):
        """
        httprunner scripts or case
        """
        case = [case]
    testset = parse_case(case, debugtalk=debugtalk, casename=case_name, config=config)

    if isinstance(testset, dict):
        """
        httprunner scripts or case
        """
        testset = [testset]

    testcase = {
        'testcases': testset
    }
    kwargs = {
        "failfast": False
    }
    runner = HttpRunner(**kwargs)
    runner.run(testcase)
    summary = runner.summary
    return summary


def parse_case(teststeps, casename=None, config=None, debugtalk=None):
    """get test case structure
        teststeps: list
        config: none or dict
        debugtalk: dict
    """
    # refs = {
    #     "env": {},
    #     "def-api": {},
    #     "def-testcase": {},
    #     "debugtalk": debugtalk
    # }
    testset = {
        "config": {
            "name": casename,
            "variables": []
        },
        "teststeps": teststeps,
    }

    if config:
        testset["config"] = config
        testset["config"]["name"] = casename

    # if casename:
    #     testset["config"]["name"] = casename

    global_variables = []
    # 1.如果传参config有变量，且数据库的变量不跟传过来的变量同名，则将这些数据库变量添加到全局变量,
    #   再将全局变量赋给testset['config']['variables']
    # 2.如果未传变量，则数据库的变量全部添加到全局变量，且将全局变量赋给testset['config']['variables']
    for variables in models.Variables.objects.all().values("key", "value"):
        if testset["config"].get("variables"):
            for content in testset["config"]["variables"]:
                if variables["key"] not in content.keys():
                    global_variables.append({variables["key"]: variables["value"]})
        else:
            global_variables.append({variables["key"]: variables["value"]})

    if not testset["config"].get("variables"):
        testset["config"]["variables"] = global_variables
    else:
        testset["config"]["variables"].extend(global_variables)
    # testcase = {
    #     "testcases": [testset]
    #
    # }
    return testset


# @run_fast
def debug_cases(cases, config=None,  debugtalk=None, project_mapping = None):

    """

    :param cases: [ {case_name:'',  case_steps:[]}, {}]
    :param config:
    :param debugtalk:
    :param project_mapping:
    :return:s
    """
    if len(cases) == 0 or not isinstance(cases, list):
        return "error! this case no steps"

    cases_list = []

    for case in cases:
        testset = parse_case(case['case_steps'], case['case_name'], config, debugtalk)
        cases_list.append(testset)

    testcases = {
        "project_mapping": {
            "PWD": "",
            "functions": {},
            "variables": {},
            "env": {}
        },
        'testcases': cases_list
    }
    kwargs = {
        "failfast": False
    }
    runner = HttpRunner(**kwargs)
    runner.run(testcases)
    summary = runner.summary
    return summary


def create_report_obj(data, suiteId=None):
    # TODO
    import json
    print(data)
    data = json.loads(json.dumps(data))
    if not suiteId:
        suiteId = models.TestSuite.objects.filter(id=suiteId)
    # report_info
    case_total = data['stat']['testcases']['total']
    success = data['stat']['testcases']['success']
    failures = data['stat']['testcases']['fail']
    start_time = data['time']['start_at']
    duration = data['time']['duration']
    platform = data['platform']['platform']

    report_info_obj = models.Report.objects.create(suite=suiteId, total=case_total, successes=success, failures=failures,
                                                   start=start_time, duration=duration, platform=platform)

    # case_info
    case_info = {}
    case_info['report'] = report_info_obj
    for detail in data['details']:

        stat = detail['stat']
        case_info['name'] = detail['name']['name']
        case_info['start_time'] = detail['time']['start_at']
        case_info['duration'] = detail['time']['duration']
        case_info['total'] = stat['total']
        case_info['successes'] = stat['successes']
        case_info['failures'] = stat['failures']
        case_info['errors'] = stat['errors']
        case_info['expectedFailures'] = stat['expectedFailures']
        case_info['unexpectedSuccesses'] = stat['unexpectedSuccesses']
        case_info['skipped'] = stat['skipped']
        if detail['success'] == True:
            case_info['result'] = 1
        else:
            case_info['result'] = 0
        case_info_obj = models.ReportCase.objects.create(**case_info)

        # step info
        records = detail['records']
        step_info = {}
        step_info_list = []
        for record in records:
            step_info['name'] = record['name']
            step_info['reportCase'] = case_info_obj
            step_info['duration'] = record['response_time']
            if record['status'] == 'success':
                # TODO
                step_info['result'] = 1
            else:
                step_info['result'] = 0
            step_info['content_size'] = record['meta_datas']['stat']['content_size']
            step_info['request'] = record['meta_datas']['data'][0]['request']
            step_info['response'] = record['meta_datas']['data'][0]['response']
            step_info['validate'] = record['meta_datas']['validators']
            step_info_list.append(step_info)
        models.ReportDetail.objects.bulk_create(step_info_list)