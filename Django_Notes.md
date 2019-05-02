#### 使用Django ORM的步骤：
1. 手动创建数据库
2. settings.py中进行配置：
```
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'HOST': '127.0.0.1', #数据库地址
    'PORT': 3306, #端口
    'NAME': 'djangodatabase', #数据库名
    'USER': 'app', #用户
    'PASSWORD': '718618', #密码}}
```
3. 在项目的__init__.py中：
```
import pymysql
pymysql.install_as_MySQLdb()
```    
4. 在app的models.py中定义类
5. 执行：
```
python manage.py makemigrations
python manage.py migrate
```
6. 生成的表名规则为：app名_class名

#### ORM
- 链式调用的接口：
    - all
    - filter
    - exclude 相反逻辑的filter, 
    - reverse 将QuerySet结果倒序排列
    - distinct
- 不支持链式调用的接口(即返回值不是QuerySet)：
    - get `except MyModel.DoesNotExist: pass`
    - create
    - get_or_create
    - update
    - update_or_create
    - count 用于返回QuerySet中有多少条记录 
    - latest
    - earliest
    - first
    - last
    - *exists* 返回True或False，对于预期接下来会用到的数据，考虑使用len(queryset)的方式判断，可以减少一次查询请求。
    - bulk_create
    - *in_bulk*
    - delete
    - values
    - value_list
- 进阶接口(Django企业开发实战p104)：
    - defer
    - only
    - select_related
    - prefetch_related    
- 常用的字段查询：
    - contains 相似查询，icontains忽略大小写 `.filter(content__contains='keyword')`
    - exact 精确匹配，iexact忽略大小写 
    - in `.filter(id__in=[1,2,3])`
    - gt 大于
    - gte 大于等于
    - lt lte
    - startswith 已某个字符串开头 istartswith
    - endswith iendswith
    - range `.filter(created_time__range=('2019-01-01', '2019-01-31'))` 
- 进阶查询：
    - F 常用于执行数据库层面的计算，以避免出现竞争状态，如更新文章访问量：
    ```
    from django.db.models import F
    post = Post.objects.get(id=1)
    post.pv = F('pv') + 1
    post.save()
    ```    
    - Q 用于or、and查询：
    ```
    from django.db.models import Q
    Post.objects.filter(Q(id=1) | Q(id=2))
    Post.objects.filter(Q(id=1) & Q(id=2))
    ```
    - Count 聚合查询
    ```
    category = Category.objects.get(id=1)
    posts_count = category.post_set.count()
    ```
    VS
    ```
    from django.db.models import Count
    categories = Category.objects.annotate(posts_count=Count('post'))
    print(categories[0].posts_count)
    ```
    - Sum 合计
    ```
    from django.db.models import Sum
    Post.objects.aggregate(all_pv=Sum('pv'))
    ```
    - Avg Min Max
    - 使用原生sql查询 `.objects.raw('SELECT * FROM blog_post')`
    