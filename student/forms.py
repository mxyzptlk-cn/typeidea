#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author: Mxyzptlk
# Date: 2019-03-28

from django import forms
from .models import Student


# 使用forms.ModelForm可以复用Student在models.py中的定义，并对部分字段进行改进
class StudentForm(forms.ModelForm):
    # 这里会自动调用、进行校验
    def clean_qq(self):
        cleaned_data = self.cleaned_data['qq']
        if not cleaned_data.isdigit():
            raise forms.ValidationError('has to be numbers')
        return int(cleaned_data)

    class Meta:
        model = Student
        fields = (
            'name', 'sex', 'profession',
            'email', 'qq', 'phone'
        )
