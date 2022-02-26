from django import template
from app01 import models
from django.db.models import Count
from django.db.models.functions import TruncMonth

register = template.Library()


# 自定义inclusion_tag
@register.inclusion_tag('left_meau.html')
def left_menu(username):
    # 构造侧边栏需要的数据
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog

    # 1 查询当前用户所有的分类及分类下的文章数
    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')
    # print(category_list)  # <QuerySet [('shuai的分类一', 1, 1), ('shuai的分类二', 2, 2), ('shuai的分类三', 1, 3)]>

    # 2 查询当前用户所有的标签及标签下的文章数
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')
    # print(tag_list)  # <QuerySet [('shuai的标签一', 2, 1), ('shuai的标签二', 1, 2), ('shuai的标签三', 1, 3)]>

    # 3 按照年月统计所有的文章
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values_list('month', 'count_num')
    # print(data_list)
    return locals()