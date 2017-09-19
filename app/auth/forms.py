# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('邮件', validators = [Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators = [Required()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮件', validators = [Required('输入不可为空'), Length(1, 64, '请输入1-64位'),
                        Email('请输入正确邮箱地址')])
    username = StringField('用户名', validators = [Required('输入不可为空'), Length(1, 64, '请输入1-64位'), 
                           Regexp(u'^[0-9a-zA-Z\u4e00-\u9fa5]{2,16}$', 0,  
                           '请输入2-10位的数字、字母、汉字或三者的组合')])
    password = PasswordField('密码', validators = [Required('输入不可为空'), EqualTo('password2', 
                             message = '两次输入的密码必须相同')])
    password2 = PasswordField('确认密码', validators = [Required('输入不可为空')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮件已被别人注册')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已被别人使用')
