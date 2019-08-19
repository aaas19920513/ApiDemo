# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 22:01
# @Author  : tuihou
# @File    : prepare.py
import json
from begin.utils import tools
from begin import models
from django.forms.models import model_to_dict
from django.core import serializers


def build_case(body, case_name):
    """

    :param body:    [{
                       name:'',
                       method: '',
                       url:'',
                       times:'',
                       bodytype:'',
                       headers:  {"headers":{"content-type":"application/json"},"desc":{"content-type":"test"}},
                       body: {"body":{"keyWord":"@name"},"desc":{"keyWord":"搜索歌手信息"}},
                       validate: {"validate":[{"equals":["status_code",200]}]},
                       extract:  {"extract":[{"status":"status_code"}],"desc":{"status":"响应状态码"}},
                       variables: {"variables":[{"name":"周杰伦"}],"desc":{"name":"歌手"}},
                  }]
    :return: test_case {
                        case_name:'',
                        case_steps:''
                    }
    """
    case_steps = []
    for step in body:
        body_dict = json.loads(step['body'])
        headers_dict = json.loads(step['headers'])

        # 解析body的value是否是faker的方法并执行
        for k, v in body_dict['body'].items():
            body_dict['body'][k] = tools.is_faker_func(v)
        test = {
            "name": step['name'],
            "times": step['times'],
            "request": {
                "url": step['url'],
                "method": step['method'],
                step['bodyType']: body_dict['body'],
                "headers": headers_dict['headers']
            },
            # "desc": self.__desc
        }
        if step['extract']:
            extract_dict = json.loads(step['extract'])
            test["extract"] = extract_dict['extract']

        if step['validate']:
            try:
                validate_dict = json.loads(step['validate'])
                test['validate'] = validate_dict['validate']
            except:
                # [{"expect": "122", "actual": "test", "comparator": "equals", "type": 3}]
                # [{"equals":["status_code",200]}]
                test['validate'] = parse_validate_from_database(json.loads(step['validate']))

        if step['variables']:
            variables_dict = json.loads(step['variables'])
            test['variables'] = variables_dict['variables']
        case_steps.append(test)

    case_obj = {
        'case_name': case_name,
        'case_steps': case_steps
    }
    return case_obj


def build_case_by_id(list_id):
    """

    :param list_id: [case_id_list]
    :return: case_list:  [ {case_name:'',  case_steps:[]}, {}]
    """

    cases_list = []
    for case_id in list_id:
        print('case_id:{}'.format(case_id))
        case_name = models.Case.objects.get(pk=case_id)
        if not case_name:
            return []
        # questset转为dict, 只能是单个对象
        case_name = model_to_dict(case_name)['name']
        # case_name = [case_info for case_info in case_name if case_info is not None][0]
        steps_query = models.Step.objects.filter(case_id=case_id).values("name", "extract", "variables", "validate", "method",
                                        "body", "url", "headers", "sequence", "bodyType", "times").order_by('sequence')
        if not steps_query:
            return []
        steps = [steps for steps in steps_query]
        case = build_case(steps, case_name=case_name)
        cases_list.append(case)
    return cases_list


def parse_validate_from_database(step):
    l = []
    dict1 = {}
    for obj in step:
        actual = obj['actual']
        comparator = obj['comparator']
        try:
            if obj['type'] == 1:
                expect1 = obj['expect']
            elif obj['type'] == 2:
                expect1 = int(obj['expect'])
            elif obj['type'] == 3:
                expect1 = float(obj['expect'])
            dict1[comparator] = [actual, expect1]
        except ValueError:
            pass
        l.append(dict1)
    return l