from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器：只展示当前用户分类"""

    # SimpleListFilter提供的两个属性：title用于展示标题，parameter_name用于配置url参数
    title = '分类过滤器'
    parameter_name = 'owner_category'

    # SimpleListFilter提供的两个方法：lookups和queryset
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# 伪需求：在分类页面直接编辑文章（用于演示如何实现在同一页面编辑关联数据）
class PostInline(admin.TabularInline):  # 也可以继承StackedInline得到不同的样式
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # list_display设置页面展示哪些字段
    list_display = ('name', 'post_count', 'status', 'is_nav', 'created_time')
    # fields设置可编辑字段
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    inlines = [PostInline, ]


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    # 设置哪些字段作为链接
    list_display_links = []
    # 页面过滤器(自定义版)
    list_filter = [CategoryOwnerFilter]
    # 搜索字段
    search_fields = ['title', 'category__name']
    # 动作相关配置是否展示在顶部和底部
    actions_on_top = True
    actions_on_bottom = True

    # 保存、编辑等按钮是否在顶部展示
    save_on_top = True

    # 编辑页不展示owner字段，通过request.user自动获取
    exclude = ('owner',)

    # # 编辑页字段配置（有顺序）
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # 编辑页字段配置（有顺序、有布局）
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    # 自定义字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # # 自定义静态资源引入
    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css",),
    #     }
    #     js = ("https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.js",)
