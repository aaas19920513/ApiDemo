# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 22:08
# @Author  : tuihou
# @File    : parse.py
from begin import models
from httprunner.api import HttpRunner


def debug_case(case_obj, debugtalk=None, config=None):
    """ debug case
        case :dict or list
    """
    print(case_obj)
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
            "name": teststeps[-1]["name"],
            "variables": []
        },
        "teststeps": teststeps,
    }

    if config:
        testset["config"] = config

    if casename:
        testset["config"]["name"] = casename

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


def debug_cases(cases, config=None,  debugtalk=None, project_mapping = None):
    """

    :param cases: [ {case_name:'',  case_steps:[]}, {}]
    :param config:
    :param debugtalk:
    :param project_mapping:
    :return:
    """
    if len(cases) == 0 or not isinstance(cases, list):
        return 'Error, please input cases_list'

    cases_list = []
    print(cases)
    print(type(cases))
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
    print(testcases)
    runner = HttpRunner(**kwargs)
    runner.run(testcases)
    summary = runner.summary
    return summary


class ParseStepFromClient(object):
    """
    解析标准HttpRunner脚本 前端->后端
    """

    def __init__(self, step, level='test'):
        """
        step => {
                    header: header -> [{key:'', value:'', desc:''},],
                    body: body -> {
                        form: formData - > [{key: '', value: '', type: 1, desc: ''},],
                        json: jsonData -> {},-
                        params: paramsData -> [{key: '', value: '', type: 1, desc: ''},]
                        files: files -> {"fields","binary"}
                    },
                    extract: extract -> [{key:'', value:'', desc:''}],
                    validate: validate -> [{expect: '', actual: '', comparator: 'equals', type: 1},],
                    variables: variables -> [{key: '', value: '', type: 1, desc: ''},],
                    hooks: hooks -> [{setup: '', teardown: ''},],
                    url: url -> string
                    method: method -> string
                    name: name -> string
                }
        """

        try:
            self.name = step.pop('name')
            self.__headers = step['headers'].pop('headers')
            self.__data = step['body'].pop('body')
            self.__dataType = step['bodyType']
            # self.__files = step['request']['files'].pop('files')

            # self.__setup_hooks = step['hooks'].pop('setup_hooks')
            # self.__teardown_hooks = step['hooks'].pop('teardown_hooks')
            # self.__desc = {
            #     "headers": step['headers'].pop('desc'),
            #     "step": step['body']['form'].pop('desc'),
            #     "variables": step['variables'].pop('desc'),
            #     "data": step['body']['form'].pop('desc'),
            #     'extract': step['extract'].pop('desc')
            # }

            if step['variables']['variables']:
                self.__variables = step['variables'].pop('variables')

            if step['extract']['extract']:
                self.__extract = step['extract']['extract']

            if step['validate']['validate']:
                self.__validate = step['validate']['validate']


            if level is 'test':
                self.url = step['url']
                self.method = step['method']
                self.__times = step['times']

            elif level is 'config':
                self.base_url = step['base_url']
                self.__parameters = step['parameters']
                # self.__desc["parameters"] = body['parameters']

            self.level = level
            self.testcase = None
        except KeyError:

            pass

    def parse(self):
        """
        返回标准化HttpRunner "desc" 字段运行需去除
        """

        if self.level is 'test':
            test = {
                "name": self.name,
                "times": self.__times,
                "request": {
                    "url": self.url,
                    "method": self.method,
                    self.__dataType: self.__data
                },
                # "desc": self.__desc
            }

            if self.__extract:
                test["extract"] = self.__extract
            if self.__validate:
                test['validate'] = self.__validate

        elif self.level is 'config':
            test = {
                "name": self.name,
                "request": {
                    "base_url": self.base_url,
                },
                # "desc": self.__desc
            }

            if self.__parameters:
                test['parameters'] = self.__parameters
        if self.__headers:
            test["request"]["headers"] = self.__headers
        if self.__variables:
            test["variables"] = self.__variables
        # if self.__setup_hooks:
        #     test['setup_hooks'] = self.__setup_hooks
        # if self.__teardown_hooks:
        #     test['teardown_hooks'] = self.__teardown_hooks
        self.testcase = test

