# -*- coding:utf-8 -*-
from wtforms import StringField,SubmitField,DateTimeField,TextAreaField,SelectField,IntegerField,TextField,BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import Length,DataRequired,InputRequired
import datetime
from APPs.models import Stdlib,Stdlib_scriap
#登录
class User(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(message='请输入用户名')])
    password=StringField('密码',validators=[DataRequired(message='请输入密码')])
    login=SubmitField('login')

#策略分析查询
class Search_policyamount(FlaskForm):
    date=SelectField('日期',choices=[(0,'')],validators=[InputRequired()])
    fact = SelectField('厂家', choices=[(1,'爱立信'),(2,'华为'),(3,'中兴')],validators=[InputRequired()])
    pcrf = SelectField('PCRF',choices=[(0,'')],validators=[InputRequired()])
    search =SubmitField('搜索')


#策略标准库查询
class Search_stblib(FlaskForm):
    policy_id=SelectField('策略ID',validators=[InputRequired()])
    fact = SelectField('厂家',choices=[(1,'爱立信'),(2,'华为'),(3,'中兴')], validators=[InputRequired()])
    search = SubmitField('搜索')

#策略标准库查询
class Search_stblibscraip(FlaskForm):
    policy_id=SelectField('策略ID',validators=[InputRequired()])
    fact = SelectField('厂家',choices=[(1,'爱立信'),(2,'华为'),(3,'中兴')], validators=[InputRequired()])
    search = SubmitField('搜索')

#策略标准表新增策略
class Insert_stblib(FlaskForm):
    policy_id=StringField('策略ID',validators=[InputRequired(),Length(32)])
    policy_name=StringField('策略标识',validators=[InputRequired(),Length(max=30)])
    demand_city=BooleanField('需求地市',validators=[DataRequired()])
    online_city=BooleanField('上线地市',validators=[DataRequired()])
    policy_type=SelectField('策略类型',choices=[(0,''),(1,'差异化服务'),(2,'流量套餐'),(3,'能力开放'),(4,'其他'),(5,'通信保障')],validators=[DataRequired()])
    policy_attribute=SelectField('策略属性',choices=[(0,''),(1,'全局策略'),(2,'业务策略'),(3,'用户策略'),(4,'测试策略'),(5,'通信保障')],validators=[DataRequired()])
    bear_type=SelectField('承载类型',choices=[(0,''),(1,'专载'),(2,'默载')],validators=[DataRequired()])
    policy_QCI=StringField('QCI',default='',validators=[InputRequired()])
    policy_ARP=StringField('ARP',default='',validators=[InputRequired()])
    policy_speed=TextField('速率',default='',validators=[InputRequired()])
    policy_other=TextField('其他',default='',validators=[InputRequired()])
    time_online=DateTimeField('上线时间',default=datetime.datetime.now())
    time_offline=DateTimeField('下线时间',default=datetime.datetime.now()+datetime.timedelta(1))
    policy_statu=SelectField('策略状态',choices=[(0,''),(1,'已上线'),(2,'已下线')],validators=[DataRequired()])
    fact=BooleanField('厂家',validators=[DataRequired()])
    SMS_content=TextAreaField('短信口径',default='',validators=[InputRequired()])
    priority_zx=StringField('中兴优先级',validators=[InputRequired(),Length(max=5)])
    priority_hw = StringField('华为优先级',validators=[InputRequired(),Length(max=5)])
    priority_eri = StringField('爱立信优先级',validators=[InputRequired(),Length(max=5)])
    #user=StringField('用户',validators=[InputRequired()])
    updatetime=DateTimeField('修改时间',default=datetime.datetime.now())
    button_delete = SubmitField('新增')

#策略脚本表新增
class Insert_stbscriap(FlaskForm):
    policy_id = IntegerField('策略ID',validators=[InputRequired(),Length(32)])
    fact = StringField('厂家',validators=[InputRequired(),Length(3)])
    content=TextAreaField('脚本内容',validators=[InputRequired(),Length(1000000)])
    user=StringField('用户',validators=[InputRequired(),Length(min=5,max=10)])
    updatetime=DateTimeField('修改时间',default=datetime.datetime.now())
    button_detail=SubmitField('新增')