# -*- coding:utf-8 -*-
from flask import render_template,session,redirect,request,flash,url_for,send_from_directory
import matplotlib.pyplot as plt
import tablib
import os
#import functools
import uuid
from sqlalchemy import and_,func
from form import User,Search_policyamount,Search_stblib,Search_stblibscraip,Insert_stblib
from APPs.models import Stdlib,Stdlib_scriap,ERRP,MSP,RBP,MLE
from APPs import policy
from app import db
from settings import Config
from flask_paginate import Pagination,get_page_parameter

# Session = sessionmaker(bind=engine) #创建session
# session = Session()
# def is_login(func):
#     @functools.wraps(func)
#     def inner(*args,**kwargs):
#         user = session.get('username')
#         print(user)
#         if not user:
#             return render_template(url_for('policy.index'))
#         return  func(*args,**kwargs)
#     return  inner

#定义初始化数据库函数
@policy.route('/create_db/')
def create_db():
    db.create_all()

#顶固删除数据库函数
@policy.route('/drop_db/')
def drop_db():
    db.drop_all()
    return 'delete databases success'
#登录验证
@policy.route('/login/',methods=['GET','POST'])
def login():
    # get方式
    # username =request.args.get("username",None)
    # password =request.args.get("password",None)
    # post方式
    if request.method == 'POST':
        form=User()
        username=form.username.data
        password=form.password.data
        #username = request.form.get('username')
        #password = request.form.get('password')
        #print(username, password)
        if username == 'admin' and password == 'Gmcc!@':
            flash('Login Success',category='success')
            #session['user'] = username
            return redirect(url_for('policy.policy_amount_more'))
        else:
            flash('Login Fail,user or password not found', category='error')
            return render_template('login.html')
    else:
        return render_template('login.html')

#基础页
@policy.route('/hello/')
def hello():
    return render_template('index.html')

@policy.route('/')
def index():
    return render_template('login.html')

#------------------------策略分析----------------------
#策略缺少数
@policy.route('/policyamount_less/',methods=['GET','POST'])
##@is_login
def policy_amount_less():
    #返回下拉列表
    form = Search_policyamount()
    menu_time=MSP.query.with_entities(MSP.time).distinct().all()
    menu_pcrf=MSP.query.with_entities(MSP.pcrf).distinct().all()
    i=1
    for mtime in menu_time:
        form.date.choices += [(i,mtime)]
        i+=1
    s=1
    for mpcrf in menu_pcrf:
        form.pcrf.choices +=[(s,mpcrf)]
        s+=1
    #获取页数
    page=request.args.get(get_page_parameter(),type=int,default=1)
    if request.method == 'POST':
        if form.date.data == '':
            time =None
        else:
            time = form.date.data
        if form.fact.data == '':
            fact=None
        else:
            fact = form.fact.data
        if form.pcrf.data =='':
            fact ==None
        else:
            pcrf=form.pcrf.data
        #查询条件
        if (time is None) & (fact is None) & (pcrf is None):
            paginate =MSP.query.all()#无过滤
        if (time is None) & (not fact is None) & (pcrf is None):
            paginate =MSP.query.filter(MSP.fact==fact).paginate(page,Config.PER_PAGE,error_out=False)#过滤厂家
        if (time is None) & (fact is None) & (not pcrf is None):
            paginate = MSP.query.filter(MSP.pcrf==pcrf).paginate(page,Config.PER_PAGE,error_out=False)#过滤PCRF
        if (not time is None) & (fact is None) & (pcrf is None):
            paginate = MSP.query.filter(MSP.time==time).paginate(page,Config.PER_PAGE,error_out=False)#过滤日期

        if (not time is None) & (not fact is None) & (pcrf is None):
            paginate = MSP.query.filter(and_(MSP.time==time,MSP.fact==fact)).paginate(page,Config.PER_PAGE,error_out=False)#过滤日期和厂家
        if (not time is None) & (fact is None) & (not pcrf is None):
            paginate = MSP.query.filter(and_(MSP.time==time,MSP.pcrf==pcrf)).paginate(page,Config.PER_PAGE,error_out=False)#过滤日期和PCRF
        if (time is None) & (not fact is None) & (not pcrf is None):
            paginate = MSP.query.filter(and_(MSP.fact==fact,MSP.pcrf==pcrf)).paginate(page,Config.PER_PAGE,error_out=False)#过滤厂家和PCRF
        if (not time is None) & (not fact is None) & (not pcrf is None):
            paginate = MSP.query.filter(MSP.time==time,MSP.fact==fact,MSP.pcrf==pcrf).paginate(page,Config.PER_PAGE,error_out=False) # 过滤厂家和PCRF和日期
    else:
        paginate = MSP.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤

    object=paginate.items
    return  render_template('policy_amount_less.html',object=object,menu_time=menu_time,menu_pcrf=menu_pcrf,paginate=paginate)

@policy.route('/policyamount_more/',methods=['GET','POST'])
#策略冗余数
#@is_login
def policy_amount_more():
    form = Search_policyamount()
    menu_time=RBP.query.with_entities(RBP.time).distinct().all()
    menu_pcrf=RBP.query.with_entities(RBP.pcrf).distinct().all()
    i = 1
    for mpcrf in menu_pcrf:
        form.date.choices+=[(i,mpcrf[0])]
        i += 1
    s = 1
    for mtime in menu_time:
        form.date.choices += [(i,mtime[0])]
        s += 1
    page = request.args.get(get_page_parameter(), type=int, default=1)
    if request.method=='POST':
        if form.date.data == '':
            time =None
        else:
            time = form.date.data
        if form.fact.data == '':
            fact=None
        else:
            fact = form.fact.data
        if form.pcrf.data =='':
            fact ==None
        else:
            pcrf=form.pcrf.data
        #查询条件
        if (time is None) & (fact is None) & (pcrf is None):
            paginate = RBP.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤
        if (time is None) & (not fact is None) & (pcrf is None):
            paginate = RBP.query.filter(RBP.fact == fact).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家
        if (time is None) & (fact is None) & (not pcrf is None):
            paginate = RBP.query.filter(RBP.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤PCRF
        if (not time is None) & (fact is None) & (pcrf is None):
            paginate = RBP.query.filter(RBP.time == time).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期

        if (not time is None) & (not fact is None) & (pcrf is None):
            paginate = RBP.query.filter(and_(RBP.time == time, RBP.fact == fact)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和厂家
        if (not time is None) & (fact is None) & (not pcrf is None):
            paginate = RBP.query.filter(and_(RBP.time == time, RBP.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和PCRF
        if (time is None) & (not fact is None) & (not pcrf is None):
            paginate = RBP.query.filter(and_(RBP.fact == fact, RBP.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF
        if (not time is None) & (not fact is None) & (not pcrf is None):
            paginate = RBP.query.filter(RBP.time == time, RBP.fact == fact, RBP.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF和日期
    else:
        paginate = RBP.query.paginate(page,Config.PER_PAGE,error_out=False) # 无过滤
    object=paginate.items
    return render_template('policy_amount_more.html',object=object,menu_time=menu_time,menu_pcrf=menu_pcrf,paginate=paginate)


@policy.route('/policyreport_error/',methods=['GET','POST'])
#@is_login
def policy_report_error():
    form = Search_policyamount()
    menu_time=ERRP.query.with_entities(ERRP.time).distinct().all()
    menu_pcrf=ERRP.query.with_entities(ERRP.pcrf).distinct().all()
    i = 1
    for mtime in menu_time:
        form.date.choices += [(i, mtime[0])]
        i += 1
    s = 1
    for mpcrf in menu_pcrf:
        form.pcrf.choices += [(s, mpcrf[0])]
        s += 1
    page=request.args.get(get_page_parameter(),type=int,default=1)
    if request.method == 'POST':
        if form.date.data == '':
            time =None
        else:
            time = form.date.data
        if form.fact.data == '':
            fact=None
        else:
            fact = form.fact.data
        if form.pcrf.data =='':
            fact ==None
        else:
            pcrf=form.pcrf.data
        #查询条件
        if (time is None) & (fact is None) & (pcrf is None):
            paginate = ERRP.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤
        if (time is None) & (not fact is None) & (pcrf is None):
            paginate = ERRP.query.filter(ERRP.fact == fact).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家
        if (time is None) & (fact is None) & (not pcrf is None):
            paginate = ERRP.query.filter(ERRP.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤PCRF
        if (not time is None) & (fact is None) & (pcrf is None):
            paginate = ERRP.query.filter(ERRP.time == time).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期

        if (not time is None) & (not fact is None) & (pcrf is None):
            paginate = ERRP.query.filter(and_(ERRP.time == time, ERRP.fact == fact)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和厂家
        if (not time is None) & (fact is None) & (not pcrf is None):
            paginate = ERRP.query.filter(and_(ERRP.time == time, ERRP.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False) # 过滤日期和PCRF
        if (time is None) & (not fact is None) & (not pcrf is None):
            paginate = ERRP.query.filter(and_(ERRP.fact == fact, ERRP.pcrf == pcrf)).all()  # 过滤厂家和PCRF
        if (not time is None) & (not fact is None) & (not pcrf is None):
            paginate = ERRP.query.filter(ERRP.time == time, ERRP.fact == fact, ERRP.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF和日期
    else:
        paginate = ERRP.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤
    object=paginate.items
    return render_template('policy_report_error.html',object=object,menu_time=menu_time,menu_pcrf=menu_pcrf,paginate=paginate)

@policy.route('/policyreport_more/',methods=['GET','POST'])
#@is_login
def policy_report_more():
    form = Search_policyamount()
    menu_time=MLE.query.with_entities(MLE.time).distinct().all()
    menu_pcrf=MLE.query.with_entities(MLE.pcrf).distinct().all()
    i=1
    for mtime in menu_time:
        form.date.choices += [(i, mtime[0])]
        i += 1
    s = 1
    for mpcrf in menu_pcrf:
        form.pcrf.choices += [(s, mpcrf[0])]
        s += 1
    page=request.args.get(get_page_parameter(),type=int,default=1)
    if request.method == 'POST':
        if form.date.data == '':
            time =None
        else:
            time = form.date.data
        if form.fact.data == '':
            fact=None
        else:
            fact = form.fact.data
        if form.pcrf.data =='':
            fact ==None
        else:
            pcrf=form.pcrf.data
        page=request.args.get(get_page_parameter(),type=int,default=1)
        #查询条件
        if (time is None) & (fact is None) & (pcrf is None):
            paginate = MLE.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤
        if (time is None) & (not fact is None) & (pcrf is None):
            paginate = MLE.query.filter(MLE.fact == fact).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家
        if (time is None) & (fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(MLE.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤PCRF
        if (not time is None) & (fact is None) & (pcrf is None):
            paginate = MLE.query.filter(MLE.time == time).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期

        if (not time is None) & (not fact is None) & (pcrf is None):
            paginate = MLE.query.filter(and_(MLE.time == time, MLE.fact == fact)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和厂家
        if (not time is None) & (fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(and_(MLE.time == time, MLE.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和PCRF
        if (time is None) & (not fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(and_(MLE.fact == fact, MLE.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF
        if (not time is None) & (not fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(MLE.time == time, MLE.fact == fact, MLE.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF和日期
    else:
        paginate = MLE.query.filter(MLE.con_more.isnot(None)).paginate(page,Config.PER_PAGE,error_out=False) # 无过滤
    object=paginate.items
    return render_template('policy_report_more.html',object=object,menu_time=menu_time,menu_pcrf=menu_pcrf,paginate=paginate)


@policy.route('/policyreport_less/',methods=['GET','POST'])
#@is_login
def policy_report_less():
    form = Search_policyamount()
    menu_time = MLE.query.with_entities(MLE.time).distinct().all()
    menu_pcrf = MLE.query.with_entities(MLE.pcrf).distinct().all()
    i = 1
    for mtime in menu_time:
        form.date.choices += [(i, mtime[0])]
        i += 1
    s = 1
    for mpcrf in menu_pcrf:
        form.pcrf.choices += [(s, mpcrf[0])]
        s += 1
    page = request.args.get(get_page_parameter(), type=int, default=1)
    if request.method == 'POST':
        if form.date.data == '':
            time =None
        else:
            time = form.date.data
        if form.fact.data == '':
            fact=None
        else:
            fact = form.fact.data
        if form.pcrf.data =='':
            fact ==None
        else:
            pcrf=form.pcrf.data

        #查询条件
        if (time is None) & (fact is None) & (pcrf is None):
            paginate = MLE.query.paginate(page,Config.PER_PAGE,error_out=False)  # 无过滤
        if (time is None) & (not fact is None) & (pcrf is None):
            paginate = MLE.query.filter(MLE.fact == fact).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家
        if (time is None) & (fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(MLE.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤PCRF
        if (not time is None) & (fact is None) & (pcrf is None):
            paginate = MLE.query.filter(MLE.time == time).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期

        if (not time is None) & (not fact is None) & (pcrf is None):
            paginate = MLE.query.filter(and_(MLE.time == time, MLE.fact == fact)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和厂家
        if (not time is None) & (fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(and_(MLE.time == time, MLE.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤日期和PCRF
        if (time is None) & (not fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(and_(MLE.fact == fact, MLE.pcrf == pcrf)).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF
        if (not time is None) & (not fact is None) & (not pcrf is None):
            paginate = MLE.query.filter(MLE.time == time, MLE.fact == fact, MLE.pcrf == pcrf).paginate(page,Config.PER_PAGE,error_out=False)  # 过滤厂家和PCRF和日期
    else:
        paginate = MLE.query.filter(MLE.con_less.isnot(None)).paginate(page,Config.PER_PAGE,error_out=False) # 无过滤
    object=paginate.items
    return render_template('policy_report_less.html',object=object,menu_time=menu_time,menu_pcrf=menu_pcrf,paginate=paginate)

#---------------------标准库------------------------------
@policy.route('/policystdlib/',methods=['GET','POST'])#标准库
#@is_login
def policy_stdlib():
    page=request.args.get(get_page_parameter(),type=int,default=1)
    if request.method =='POST':
        form = Search_stblib()
        policyid = form.policy_id.data
        if form.validate_on_submit():
            if form.fact.data =='':
                fact = None
            else:
                fact=form.fact.data
        if (policyid is None) & (fact is None):
            paginate=Stdlib.query.paginate(page,Config.PER_PAGE,error_out=False)#无过滤
        if (not policyid is None) & (fact is None):
            paginate=Stdlib.query.filter(Stdlib.policy_id==policyid).paginate(page,Config.PER_PAGE,error_out=False)#过滤策略id
        if (policyid is None) & (not fact is None):
            paginate=Stdlib.query.filter(Stdlib.fact.like('%{}%'.format(fact))).paginate(page,Config.PER_PAGE,error_out=False)#过滤厂家
        if (not policyid is None) & (not fact is None):
            paginate=Stdlib.query.filter(Stdlib.policy_id==policyid).filter(Stdlib.fact.like('%{}%'.format(fact))).paginate(page,Config.PER_PAGE,error_out=False)#过滤策略id和厂家
    else:
        paginate = Stdlib.query.paginate(page,Config.PER_PAGE,error_out=False)# 无过滤
    object=paginate.items
    return render_template('policy_stdlib.html',object=object,paginate=paginate)

@policy.route('/policystdlib_script/',methods=['GET','POST'])#标准库脚本内容
#@is_login
def policy_stdlib_script():
    page=request.args.get(get_page_parameter(),type=int,default=1)
    if request.method =='POST':
        form = Search_stblibscraip()
        policyid = form.policy_id.data
        if form.validate_on_submit():
            fact = form.fact.data
        else:
            fact=None
        if (policyid is None) & (fact is None):
            paginate=Stdlib_scriap.query.paginate(page,Config.PER_PAGE,error_out=False)#无过滤
        if (not policyid is None) & (fact is None):
            paginate=Stdlib_scriap.query.filter(Stdlib_scriap.policy_id==policyid).paginate(page,Config.PER_PAGE,error_out=False)#过滤策略id
        if (policyid is None) & (not fact is None):
            paginate=Stdlib_scriap.query.filter(Stdlib_scriap.fact.like('%{}%'.format(fact))).paginate(page,Config.PER_PAGE,error_out=False).all()#过滤厂家
        if (not policyid is None) & (not fact is None):
            paginate=Stdlib_scriap.query.filter(Stdlib_scriap.policy_id==policyid).filter(Stdlib_scriap.fact.like('%{}%'.format(fact))).paginate(page,Config.PER_PAGE,error_out=False)#过滤策略id和厂家
    else:
        paginate = Stdlib.query.paginate(page,Config.PER_PAGE,error_out=False)# 无过滤
    object=paginate.items
    return render_template('policy_stdlib_script.html',object=object,paginate=paginate)

#----------------------------视图-----------------------------
@policy.route('/policyvisval_error/',methods=['GET','POST'])
#@is_login
def policy_visual_error():
    object_pcrf=[]
    object_count=[]
    menu_time=ERRP.query.with_entities(MSP.time).distinct().all()
    time=request.args.get('time')
    if time:
        object=ERRP.query.filter(ERRP.time==time).with_entities(ERRP.pcrf,func.count(ERRP.policy_id)).group_by(ERRP.pcrf).all()
    else:
        time = menu_time[-1][0]
        object=ERRP.query.filter(ERRP.time==str(time)).with_entities(ERRP.pcrf,func.count(ERRP.policy_id).label('count')).group_by(ERRP.pcrf).all()
    for obj in object:
        object_pcrf.append(obj.pcrf)
        object_count.append(obj.count)
    fig=plt.figure()
    plt.pie(object_count,labels=object_pcrf,autopct='%1.2f%')
    imgname=uuid.uuid4().hex+'.jpg'
    imgurl=os.path.join(Config.VISVAL_IMG,imgname)
    plt.title='%s 各PCRF分布' %time
    plt.savefig(imgurl)
    return render_template('policy_visual_error.html',menu_time=menu_time,imgurl=imgurl)

@policy.route('/policyvisval_more/',methods=['GET','POST'])
#@is_login
def policy_visual_more():
    return render_template('policy_visual_more.html')

@policy.route('/policyvisval_less/',methods=['GET','POST'])
#@is_login
def policy_visual_less():
    return render_template('policy_visual_less.html')


#新增策略列配置
@policy.route('/insert_stdlib/',methods=['GET','POST'])
def insert_stdlib():
    form = Insert_stblib()
    if (request.method =='POST') and (form.validate_on_submit() == True):
        policydata=Stdlib(policy_id=form.policy_id.data
                          ,policy_name=form.policy_name.data
                          ,online_city=form.online_city.data
                          ,demand_city=form.demand_city.data                                                       ,policy_attribute=form.policy_attribute
                          ,policy_type=form.policy_type
                          ,bear_type=form.bear_type.data
                          ,policy_QCI=form.policy_QCI
                          , policy_ARP=form.policy_ARP
                          ,policy_speed=form.policy_speed
                          ,policy_other=form.policy_other
                          ,fact=form.fact.data
                          ,policy_status=form.policy_statu
                          ,priority_eri=form.priority_eri
                          ,priority_zx=form.priority_zx
                          ,priority_hw=form.priority_hw
                          ,SMS_content=form.SMS_content)

        db.session.add(policydata)
        db.session.commit()
        return  redirect('policy_stdlib.html')
    else:
        return  render_template('insert_stdlib.html',demandcitys=Config.demandcitys,onlinecitys=Config.onlinecitys)

#策略列表详情
@policy.route('/details_stdlib/',methods=['GET','POST'])
def details_stdlib():
        return redirect('insert_stdlib.html')

#删除策略
@policy.route('/delete_stdlib/',methods=['GET'])
def delete_stdlib():
    delete_policy=request.args.get('policy_id',type=str)
    Stdlib.query.filter(Stdlib.policy_id == delete_policy).delete()
    db.session.commit()
    return render_template('policy_stdlib.html')

@policy.route('/delete_amount_less/',methods=['GET'])
def delete_amount_less():
    id = request.args.get('id', type=str)
    MSP.query.filter(MSP.id == id).delete()
    db.session.commit()
    return  render_template('policy_amount_less.html')

@policy.route('/delete_amount_more/',methods=['GET'])
def policy_amount_more2():
    id=request.args.get('id',type=str)
    RBP.query.filter(RBP.id==id).delete()
    db.session.commit()
    return  render_template('policy_amount_more.html')

@policy.route('/delete_report_less/',methods=['GET'])
def delete_report_less():
    id = request.args.get('id', type=str)
    MLE.query.filter(MLE.id == id).delete()
    db.session.commit()
    return  render_template('delete_report_less.html')

@policy.route('/delete_report_more/',methods=['GET'])
def delete_report_more():
    id = request.args.get('id', type=str)
    MLE.query.filter(MLE.id == id).delete()
    db.session.commit()
    return  render_template('delete_report_more.html')

@policy.route('/delete_report_error/',methods=['GET'])
def delete_report_error():
    id = request.args.get('id', type=str)
    ERRP.query.filter(ERRP.id == id).delete()
    db.session.commit()
    return  render_template('delete_report_error.html')
#改策略
@policy.route('/update_stdlib/',methods=['GET'])
def update_stdlib():
    db.session.excute();

    render_template('vpolicy_stdlib.html')

#新增策略脚本配置

#复选框值request.from.getlist("demandcity")
#下载
@policy.route('/export_/',methods=['GET','POST'])
def export():
    filename = uuid.uuid4().hex+'xlsx'
    object=Stdlib.query.all()
    list_obj=[]
    header=['policy_id','policy_name','demand_city','online_city','policy_type','policy_attribute','bear_type','policy_QCI','policy_ARP','policy_speed','policy_other','time_online','time_offline','policy_status','fact','SMS_content','priority_zx','priority_hw','priority_eri','updatetime']
    for obj in object:
        list_obj.append([obj.policy_id,obj.policy_name,obj.demand_city,obj.nline_city,obj.policy_type,obj.policy_attribute,obj.bear_type,obj.policy_QCI,obj.policy_ARP,obj.policy_speed,obj.policy_other,obj.time_online,obj.time_offline,obj.policy_status,obj.fact,obj.SMS_content,obj.priority_zx,obj.priority_hw,obj.priority_eri,obj.updatetime])
    datatab=tablib.Dataset(*list_obj,headers=header)
    f=open(filename,'wb')
    f.write(datatab.xlsx)
    f.close()
    return send_from_directory(Config.UPLOADFOLDER,filename=filename,as_attachment=True)


@policy.route('/export_sc/',methods=['',''])
def exprot_sc():
    filename=uuid.uuid4().hex+'xlsx'
    object=Stdlib_scriap.query.all()
    header=['policy_id','fact','content','date']
    list_data=[]
    for obj in object:
        list_data.append(obj.policy_id,obj.fact,obj.content,obj.date)
    data=tablib.Dataset(*list_data,headers=header)
    f=open(filename,'wb')
    f.write(data.xlsx)
    f.close()
    return send_from_directory(Config.UPLOADFOLDER,filename=filename,as_attachment=True)