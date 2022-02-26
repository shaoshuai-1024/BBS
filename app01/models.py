from django.db import models

# Create your models here.
"""
先写普通字段
之后再写外键字段
"""
from django.contrib.auth.models import AbstractUser

# 用户表
class UserInfo(AbstractUser):
    phone = models.BigIntegerField(verbose_name='手机号',null=True,blank=True)
    """
    null=True   数据可该字段可以为空
    blank=True  admin后台管理该字段可以为空
    """
    # 头像
    avatar = models.FileField(upload_to='avatar/',default='avatar/default.png',verbose_name='用户头像')
    """
    给avatar字段传文件对象 该文件会自动储存到avatar文件下 然后avatar字段只保存在文件路径avatar/default.png
    """
    create_time = models.DateField(auto_now_add=True)
    """
    auto_now:每次修改数据的时候都会自动更新当前时间
    auto_now_add:只在创建数据的时候记录创建时间后续不会自动修改了
    """

    # 外键字段
    blog = models.OneToOneField(to='Blog',null=True)

    class Meta:
        verbose_name_plural = '用户表'  # 修改admin后台管理默认的表明

    def __str__(self):
        return self.username

# 博客站点表
class Blog(models.Model):
    site_name = models.CharField(verbose_name='站点名称',max_length=32)
    site_title = models.CharField(verbose_name='站点标题',max_length=32)
    # 给博客添加样式（简单模拟）
    site_theme = models.CharField(verbose_name='站点样式',max_length=64) # 存css/js的文件路径

    def __str__(self):
        return self.site_name

# 分类表
class Category(models.Model):
    name = models.CharField(verbose_name='文章分类',max_length=32)
    # 外键字段
    blog = models.ForeignKey(to='Blog',null=True)

    def __str__(self):
        return self.name

# 标签表
class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签',max_length=32)
    # 外键字段
    blog = models.ForeignKey(to='Blog',null=True)

    def __str__(self):
        return self.name

# 文章表
class Article(models.Model):
    title = models.CharField(verbose_name='文章标题',max_length=64)
    desc = models.CharField(verbose_name='文章简介',max_length=255)
    # 文章内容有很多 一般情况下都是使用TextField
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateField(auto_now_add=True)

    # 数据库字段设计优化
    up_num = models.BigIntegerField(verbose_name='点赞数',default=0)
    down_num = models.BigIntegerField(verbose_name='点踩数',default=0)
    comment_num = models.BigIntegerField(verbose_name='评论数',default=0)

    # 外键字段
    blog = models.ForeignKey(to='Blog',null=True)
    category = models.ForeignKey(to='Category',null=True)
    tags = models.ManyToManyField(to='Tag',
                                  through='Article2Tag',
                                  through_fields=('article','tag')
                                  )
    def __str__(self):
        return self.title

# 多对多第三方关系表
class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')

# 点赞点踩表
class UpAndDown(models.Model):
    is_up = models.BooleanField()  # 传布尔值 存0/1
    # 外键字段
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')

# 评论表
class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容',max_length=255)
    comment_time = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
    # 自关联
    parent = models.ForeignKey(to='self',null=True)  # 有些评论就是根评论
    # 外键字段
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')