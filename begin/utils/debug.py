# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 22:08
# @Author  : tuihou
# @File    : debug.py
from begin import models
from httprunner.api import HttpRunner


def debug_case(case, debugtalk=None, casename=None, config=None, save=True):
    """ debug case
        case :dict or list
    """
    if len(case) == 0:
        return 'Error, No case'

    if isinstance(case, dict):
        """
        httprunner scripts or case
        """
        case = [case]
    testset = parse_case(case, debugtalk=debugtalk, casename=casename, config=config)
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
    print(11111111111111111111111111)
    if len(cases) == 0 or not isinstance(cases, list):
        return 'Error, please input cases_list'
    cases_list = []
    print(11111111111111111111111111)
    for case in cases:
        testset = parse_case(case['teststeps'], case['name'], config, debugtalk)
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
    print(222222222222222222)
    print(testcases)
    runner = HttpRunner(**kwargs)
    runner.run(testcases)
    summary = runner.summary
    return summary


class Format2(object):
    """
    解析标准HttpRunner脚本 前端->后端
    """

    def __init__(self, request, level='test'):
        """
        body => {
                    header: header -> [{key:'', value:'', desc:''},],
                    request: request -> {
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
            self.name = request['name']
            self.__desc = {
                "header": request['header'].pop('desc'),
                "request": request['request']['form'].pop('desc'),
                "variables": request['variables'].pop('desc'),
            }

            if level is 'test':
                self.url = request['url']
                self.method = request['method']
                self.__times = request['times']
                self.__extract = request['extract']
                self.__validate = request['validate']
                # self.__desc['extract'] = request['extract']

            elif level is 'config':
                self.base_url = request['base_url']
                self.__parameters = request['parameters']
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
                    "method": self.method
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
        if self.__json:
            test["request"]["json"] = self.__json
        self.testcase = test


def build_case(body):
    teststeps = []
    for step in body:
        test = {
            "name": step['name'],
            "times": step['times'],
            "request": {
                "url": step['url'],
                "method": step['method']
            },
            # "desc": self.__desc
        }
        if step['extract']:
            test["extract"] = step['extract']
        if step['validate']:
            test['validate'] = step['validate']
        if step['json']:
            test["request"]["json"] = step['json']
        teststeps.append(test)
    return teststeps


def build_case_by_id(list_id):
    """

    :param list_id: [case_id_list]
    :return: case_list:[{'name':'casename',teststeps:[] },{}]
    """

    # def run_case(case, config = None):
    case_list = []
    for case_id in list_id:
        case_name = models.Case.objects.filter(pk=case_id).values("name")
        # questset转为dict
        case_name = [case_info for case_info in case_name if case_info is not None][0]
        case = case_name
        steps = models.Step.objects.filter(case_id=case_id).values("name", "extract", "variables", "validate", "api_id")
        teststeps = []
        for step in steps:
            api_id = step.pop("api_id")
            api_info = models.API.objects.filter(pk=api_id).values("name", "body", "method", "url")
            # questset转为dict
            api_info = [api_info for api_info in api_info if api_info is not None][0]
            api = { }
            api["url"] = api_info["url"]
            api["method"] = api_info["method"]
            api["body"] = api_info["body"]
            step["request"] = api
            teststeps.append(step)
        case["teststeps"] = teststeps
        case_list.append(case)
    return case_list


