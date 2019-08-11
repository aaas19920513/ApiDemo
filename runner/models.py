from django.db import models

# Create your models here.


class Project(models.Model):

    status_chioces = (
        (0, '开发中'),
        (1, '已完毕'),
    )
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='项目名称')
    developer = models.CharField(max_length=256, verbose_name='开发人员')
    tester = models.CharField(max_length=256, verbose_name='测试人员')
    status = models.IntegerField(choices=status_chioces, verbose_name='项目状态', default=0)
    description = models.CharField(max_length=256, verbose_name='项目描述')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "项目信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Module(models.Model):

    status_chioces = (
        (0, '开发中'),
        (1, '已完毕'),
    )
    project = models.ForeignKey(to=Project, related_name='module', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='模块名称')
    developer = models.CharField(max_length=256, verbose_name='开发人员')
    tester = models.CharField(max_length=256, verbose_name='测试人员')
    status = models.IntegerField(choices=status_chioces, verbose_name='模块状态', default=0)
    description = models.CharField(max_length=256, verbose_name='模块描述')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "模块信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Case(models.Model):

    module = models.ForeignKey(to=Module, on_delete=models.CASCADE, related_name='case')
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='用例名称')
    version = models.CharField(max_length=32, verbose_name='模块版本')
    description = models.CharField(max_length=256, verbose_name='用例描述')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "用例信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Api(models.Model):

    name = models.CharField(max_length=256, verbose_name='接口描述')
    endpoint = models.CharField(max_length=256, verbose_name='接口地址')
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE, related_name='api')

    class Meta:
        verbose_name = "接口信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CaseStep(models.Model):

    method_chioce = (
        (1, 'post'),
        (2, 'get'),
        (3, 'put'),
        (4, 'delete'),
    )
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE, related_name='step')
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='步骤名称')
    description = models.CharField(max_length=256, verbose_name='用例描述')
    url = models.CharField(max_length=256, blank=False, verbose_name='接口地址')
    method = models.IntegerField(choices=method_chioce, verbose_name='请求方式', default=1)
    header = models.CharField(max_length=256, verbose_name='请求头')
    data = models.CharField(max_length=256, verbose_name='请求数据')
    assert_response = models.CharField(max_length=256, verbose_name='期望')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "步骤表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Variables(models.Model):

    key = models.CharField(null=False, max_length=100, unique=True)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='variables')

    class Meta:
        verbose_name = "全局变量"
        verbose_name_plural = verbose_name
        db_table = "Variables"

    def __str__(self):
        return self.key


class Config(models.Model):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息"
        db_table = "Config"

    name = models.CharField("环境名称", null=False, max_length=100, unique=True)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='config')

    def __str__(self):
        return self.name


class DataBase(models.Model):

    db_type = (
        (1, "Sql Server"),
        (2, "MySQL"),
        (3, "Oracle"),
        (4, "Mongodb"),
        (5, "InfluxDB")
    )

    name = models.CharField("数据库名称", null=False, max_length=100)
    server = models.CharField("服务地址", null=False, max_length=100)
    account = models.CharField("登录名", max_length=50, null=False)
    password = models.CharField("登陆密码", max_length=50, null=False)
    type = models.IntegerField('数据库类型', default=2, choices=db_type)
    desc = models.CharField("描述", max_length=50, null=False)

    class Meta:
        verbose_name = "数据库信息"
        db_table = "DataBase"


class Debugtalk(models.Model):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动库"
        db_table = "Debugtalk"

    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)


