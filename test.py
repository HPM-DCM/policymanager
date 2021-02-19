# -*- coding:utf-8 -*-
#from app import db
from APPs.models import MLE,MSP,ERRP
from sqlalchemy import func

# object=MSP.query.filter(MSP.time=='20201015').with_entities(MSP.pcrf,func.count(MSP.policy_id).label('count')).group_by(MSP.pcrf).all()
# print(object)
# for obj in object:
#     print(obj.count)