# -*- coding:utf-8 -*-
class Config:
    SECRET_KEY='policy ORM'
    DEBUG = False
    TESTING = False
    VISVAL_IMG='visval_img'


    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:123456@127.0.0.1:3306/policy?charset=utf8'

    demandcitys=('集团','省公司','广州','深圳','佛山','中山','清远','珠海','韶关','东莞','惠州','汕头','汕尾','揭阳','潮州','梅州','河源','湛江','江门','茂名','云浮','阳江','肇庆')

    onlinecitys=('全省','广州','深圳','佛山','中山','清远','珠海','韶关','东莞','惠州','汕头','汕尾','揭阳','潮州','梅州','河源','湛江','江门','茂名','云浮','阳江','肇庆')
    PER_PAGE=30