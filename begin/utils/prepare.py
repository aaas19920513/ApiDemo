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
    # todo 重构
    """

    :param body:    [{
                       name:'',
                       method: '',
                       url:'',
                       times:'',
                       path_params:'',
                       query_params:'',
                       body:'',
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

        test = {
            "name": step['name'],
            "times": step['times'],
            "request": {
                "url": step['url'],
                "method": step['method'],
                # step['bodyType']: body_dict['body'],
                "headers": headers_dict['headers']
            },
            # "desc": self.__desc
        }

        if step['body']:
            for body in step['body']:
                # set body's  key & name
                # 解析body的value是否是faker的方法并执行
                step['body'][body['name']] = tools.is_faker_func(body['value'])
            test['request']['data'] = step['body']

        if step['query_params']:
            for dict_obj in step['body']:
                # set params's  key & name
                # 解析params的value是否是Faker类的方法并执行
                step['query_params'][dict_obj['name']] = tools.is_faker_func(dict_obj['value'])
            test['request']['params'] = step['query_params']

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
        else:
            step['variables'] = {}

        if step['path_params']:
            # 将含变量的url_path 替换
            path_params = step['path_params'][0]['name']
            step['variables']['url_path_variables'] = path_params
            start = step['url'].index('{')
            end = step['url'].index('}')
            step['url'] = step['url'].replace(step['url'][start:end+1], path_params)

        case_steps.append(test)

    case_obj = {
        'case_name': case_name,
        'case_steps': case_steps
    }
    return case_obj


def build_case_by_id(case_id):
    """

    :param case_id: id
    :return: case: {case_name:'',  case_steps:[]}
    """

    case_name_query = models.Case.objects.filter(pk=case_id).values('name')
    # case_name = serializers.serialize('json', models.Case.objects.filter(pk=case_id))
    if not case_name_query:
        return []
    # questset转为dict, 只能是单个对象
    # case_name = model_to_dict(case_name)['name']
    case_name = [case_name for case_name in case_name_query][0]
    steps_query = models.Step.objects.filter(case_id=case_id).values("name", "extract", "variables", "validate", "method",
                                    "body", "url", "headers", "sequence", "query_params", 'path_params', "times").order_by('sequence')
    steps = [steps for steps in steps_query]
    case = build_case(steps, case_name=case_name)

    return case


def parse_validate_from_database(step):
    l = []
    dict1 = {}
    for obj in step:
        actual = obj['actual']
        comparator = obj['comparator']
        try:
            if obj['type'] == 2:
                expect1 = int(obj['expect'])
            elif obj['type'] == 3:
                expect1 = float(obj['expect'])
            else:
                expect1 = obj['expect']
            dict1[comparator] = [actual, expect1]
        except ValueError:
            pass
        l.append(dict1)
    return l