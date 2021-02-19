# -*- coding:utf-8 -*-
from datetime import datetime
#from flask_sqlalchemy import SQLAlchemy
#from APPs import create_app
from app import db

class Stdlib(db.Model):
    __tablename__='stdlib'
    policy_id = db.Column(db.String(32),primary_key=True)
    policy_name = db.Column(db.String(200))
    demand_city = db.Column(db.String(5))
    online_city = db.Column(db.String(20))
    policy_type = db.Column(db.String(10))
    policy_attribute = db.Column(db.String(10))
    bear_type = db.Column(db.String(5),nullable=True)
    policy_QCI = db.Column(db.Integer,nullable=True)
    policy_ARP = db.Column(db.Integer,nullable=True)
    policy_speed = db.Column(db.String(300),nullable=True)
    policy_other = db.Column(db.String(300),nullable=True)
    time_online = db.Column(db.DateTime,nullable=True)
    time_offline = db.Column(db.DateTime,nullable=True)
    policy_status = db.Column(db.String(5))
    fact = db.Column(db.String(15))
    SMS_content = db.Column(db.String(500),nullable=True)
    priority_zx = db.Column(db.String(10),nullable=True)
    priority_hw = db.Column(db.String(10),nullable=True)
    priority_eri = db.Column(db.String(10),nullable=True)
    updatetime = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "policyid:{},policyname:{}".format(self.policy_id, self.policy_name)


class MSP(db.Model):
    __tablename__='mspolicy'
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    time=db.Column(db.String(10))
    pcrf=db.Column(db.String(20))
    fact=db.Column(db.String(5))
    policy_id=db.Column(db.String(32))
    policy_name=db.Column(db.String(20),nullable=True)

    def __repr__(self):
        return "time:{},pcrf:{},fact:{},policyid:{},policyname:{}".format(self.time,self.pcrf,self.fact,self.policy_id, self.policy_name)

class RBP(db.Model):
    __tablename__='rbpolicy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(10))
    pcrf = db.Column(db.String(20))
    fact = db.Column(db.String(5))
    policy_id = db.Column(db.String(50))
    policy_name = db.Column(db.String(50),nullable=True)

    def __repr__(self):
        return "time:{},pcrf:{},fact:{},policyid:{},policyname:{}".format(self.time,self.pcrf,self.fact,self.policy_id, self.policy_name)

class ERRP(db.Model):
    __tablename__='errpolicy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time=db.Column(db.String(10))
    pcrf=db.Column(db.String(20))
    fact=db.Column(db.String(5))
    policy_id=db.Column(db.String(32))
    role=db.Column(db.String(20))
    net_value=db.Column(db.String(500))
    stand_value=db.Column(db.String(500))

    def __repr__(self):
        return "time:{},pcrf:{},fact:{},policyid:{},role:{},net_value:{},stand_value:{}".format(self.time,self.pcrf,self.fact,self.policy_id, self.role,self.net_value,self.stand_value)

class MLE(db.Model):
    __tablename__='mlepolicy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(10))
    pcrf = db.Column(db.String(20))
    fact = db.Column(db.String(5))
    policy_id = db.Column(db.String(32))
    con_more = db.Column(db.String(500),nullable=True)
    con_less = db.Column(db.String(500),nullable=True)

    def __repr__(self):
        return "policyid:%s" % self.policy_id

class Stdlib_scriap(db.Model):
    __tablename__='stdlib_scriap'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    policy_id=db.Column(db.String(32))
    fact=db.Column(db.String(5))
    content=db.Column(db.String(10000))
    date=db.Column(db.DateTime, default = datetime.now())

    def __repr__(self):
        return  "policyid:%s" %self.policy_id
