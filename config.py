DEBUG = True


SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='fmmqsb100', server='127.0.0.1:3306', database='boxticket_test')
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='admin', password='fmmqsb100', server='testdb.cdbj30m3omel.us-east-2.rds.amazonaws.com:3306', database='boxticket')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SENT_EMAIL_USER = 'f.m.q1993@gmail.com'
SENT_EMAIL_PASSWORD = 'fmmqsb100'

ADMINSUPERKEY = "fd35b2fc13a0ad16ce5bd61e329a8e6ad43fd24552326559b6f0fb45"