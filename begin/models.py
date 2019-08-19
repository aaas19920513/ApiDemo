from django.db import models


class Category(models.Model):
    """
    多级分类
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    label = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", blank=True, null=True, help_text="类别描述")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="children")

    class Meta:
        verbose_name = "接口分类树"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label


class Project(models.Model):

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='project', null=False,
                                 verbose_name="项目类目",  default=1)
    name = models.CharField(max_length=128, blank=False, unique=True, verbose_name='项目名称')
    developer = models.CharField(max_length=256, verbose_name='开发人员')
    tester = models.CharField(max_length=256, verbose_name='测试人员')
    description = models.CharField(max_length=256, verbose_name='项目介绍')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "项目信息表"
        verbose_name_plural = verbose_name
        # db_table = "Project"

    def __str__(self):
        return self.name


class API(models.Model):
    """
    API信息表
    """

    class Meta:
        verbose_name = "接口表"
        verbose_name_plural = verbose_name
        ordering = ['id']
        # db_table = "API"
    category = models.ForeignKey(to=Category, blank=False, on_delete=models.CASCADE, related_name='api', null=False,
                                 verbose_name="Api类目")
    name = models.CharField("接口名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=200)
    method = models.CharField("请求方式", null=False, max_length=10)
    headers = models.TextField('请求头', null=False)
    protocol = models.CharField('请求协议', null=False, max_length=10, default='http')
        # bodyRemark = models.CharField('请求体注释', max_length=255)
        # headersRemark = models.CharField('请求头注释', max_length=255)
    response = models.TextField('接口返回')
    # test = models.ForeignKey(to=Category, blank=True, on_delete=models.CASCADE, related_name='children', null=False,
    #                          verbose_name='需与category一致', default=category)

    def __str__(self):
        return self.name


class Case(models.Model):

    run_flag = (
        (0, "不运行"),
        (1, "运行"),
    )

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='case', null=False,
                                 verbose_name="case类目",)
    project = models.ManyToManyField(to=Project, null=True, blank=True)
    api = models.ForeignKey(to=API, on_delete=models.CASCADE, related_name='case', null=False, verbose_name='Api')
    name = models.CharField(max_length=128, blank=False, verbose_name='用例名称')
    create_user = models.CharField(max_length=32, verbose_name='创建人',)
    update_user = models.CharField(max_length=32,  verbose_name='修改人', )
    runFlag = models.IntegerField(choices=run_flag, verbose_name='是否运行')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    class Meta:
        verbose_name = "用例信息表"
        verbose_name_plural = verbose_name
        # db_table = "Case"

    def __str__(self):
        return self.name


class Step(models.Model):

    method_choice = (
        (0, "POST"),
        (1, "DELETE"),
        (2, "GET"),
        (3, 'PATCH'),
        (4, "PUT"),
        (5, 'HEAD'),
        (6, 'OPTIONS'),
    )
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE, related_name='step')
    api = models.ForeignKey(to=API, on_delete=models.CASCADE, related_name='step')
    name = models.CharField(max_length=128, blank=False, verbose_name='步骤名称')
    url = models.CharField(max_length=256, blank=False, verbose_name='请求url')
    method = models.CharField(max_length=20, blank=False, null=False)
    body = models.TextField(blank=False, verbose_name='请求参数')
    bodyType = models.CharField('主体类型', null=False, max_length=10)
    headers = models.TextField('请求头', null=False)
    sequence = models.IntegerField(blank=False, verbose_name='步骤顺序')
    # step_info = models.TextField(verbose_name='配置信息')
    variables = models.TextField(verbose_name='变量', blank=True)
    extract = models.TextField(verbose_name='提取变量表达式', blank=True)
    validate = models.TextField(verbose_name='断言', blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    times = models.IntegerField('循环次数', default=1)

    class Meta:
        verbose_name = "步骤表"
        verbose_name_plural = verbose_name
        # db_table = "Step"
        ordering = ['sequence']

    def __str__(self):
        return self.name


class Config(models.Model):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息表"
        verbose_name_plural = verbose_name
        # db_table = "Config"

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='config')

    def __str__(self):
        return self.name


class Variables(models.Model):

    key = models.CharField(null=False, max_length=100, unique=True)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='variables')

    class Meta:
        verbose_name = "全局变量表"
        verbose_name_plural = verbose_name
        # db_table = "Variables"

    def __str__(self):
        return self.key


from mptt.models import MPTTModel


class Classify(MPTTModel):
    name = models.CharField('名称', max_length=50, unique=True)
    parent = models.ForeignKey('self', verbose_name='父类目', null=True, blank=True, related_name='children',
                               on_delete=models.CASCADE)

    class Meta:
        db_table = 'classify'
        verbose_name = verbose_name_plural = '接口分类'

    def __str__(self):
        return self.name

#
# class Report(models.Model):

