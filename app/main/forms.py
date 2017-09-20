# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from flask_pagedown.fields import PageDownField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email, Regexp
from ..models import User, Role


class NameForm(FlaskForm):
    name = StringField('姓名', validators=[Required('输入不可为空')])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators = [Length(0, 64, '请输入0-64位')])
    location = StringField('地址', validators = [Length(0, 64, '请输入0-64位')])
    about_me = TextAreaField('备注')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators = [Required('输入不可为空'), Length(1, 64, '请输入1-64位'),
                        Email('请输入正确邮箱地址')])
    username = StringField('用户名', validators = [
                           Required('输入不可为空'), Length(1, 64, '请输入1-64位'),
                           Regexp(u'^[0-9a-zA-Z\u4e00-\u9fa5]{2,16}$', 0, 
                           '请输入2-10位的字母、数字、汉字或三者的组合')])
    confirmed = BooleanField('确证')
    role = SelectField('角色', coerce = int)
    name = StringField('真实姓名', validators = [Length(0, 64, '请输入0-64位')])
    location = StringField('地址', validators = [Length(0, 64, '请输入0-64位')])
    about_me = TextAreaField('备注')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email = field.data).first():
            raise ValidationError('邮件已被他人注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已被他人使用')


class PostForm(FlaskForm):
    body = PageDownField('畅所欲言', validators = [Required('输入不可为空')])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('', validators = [Required('输入不可为空')])
    submit = SubmitField('提交')
