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
    email = StringField('邮件', validators = [Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators = [Required(), Length(1, 64), 
                           Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0, 'Username must have only letters,' 
                           'numbers, dots or underscores')])
    password = PasswordField('密码', validators = [Required(), EqualTo('password2', 
                             message = 'password must match.')])
    password2 = PasswordField('确认密码', validators = [Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮件已被别人注册')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已被别人使用')
