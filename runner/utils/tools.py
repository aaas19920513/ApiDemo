# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 21:32
# @Author  : tuihou
# @File    : tools.py

from runner import models


def get_counter(model, pk=None):
    """
    统计相关表长度
    """
    if pk:
        return model.objects.filter(project__id=pk).count()
    else:
        return model.objects.count()


def get_project_detail(pk):
    """
    项目详细统计信息
    """
    api_count = get_counter(models.Api, pk=pk)
    case_count = get_counter(models.Case, pk=pk)
    variables_count = get_counter(models.Variables, pk=pk)

    return {
        "api_count": api_count,
        "case_count": case_count,
        "variables_count": variables_count,
    }