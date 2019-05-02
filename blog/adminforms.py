#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author: Mxyzptlk
# Date: 2019-04-04

from django import forms


# 自定义后台form展示，这里把desc摘要由单行显示改为多行显示（CharField → Textarea）
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)


