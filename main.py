from flask import Flask, request, redirect, url_for, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
from DB_models import *
from Ressponse_models import *
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Token import *
import hashlib
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
import os
import calendar
import pyqrcode
import png
from pyqrcode import QRCode

application.config.from_object('config')
db.init_app(application)
with application.app_context():
    db.create_all()
migrate = Migrate(application, db)
CORS(application)

ForgetPasswordsTokens = {}
RegistrTokens = {}
MainTokens = {}


@application.route('/')
@cross_origin()
def index():
    return 'Service is running'


@application.route('/Image/<string:DictName>/<string:FileName>/<string:FileType>', methods=['Get'])
@cross_origin()
def show_index(DictName, FileName, FileType):
    ApplicationPath = os.path.join(application.root_path, 'static')
    DictPath = os.path.join(ApplicationPath, DictName)
    FullFilePath = os.path.join(DictPath, FileName + '.' + FileType)
    print(FullFilePath)
    return render_template("ImageTemplate.html", temp_image=FullFilePath)


@application.route('/Login', methods=['POST'])
@cross_origin()
def Login():
    ReturnObj = LoginResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        TempPasswordObj = request.get_json()['Password']
        request.get_json()['Password'] = ''
        NewReqLog = Services_Log(Service_Name='Login', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=1, Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        request.get_json()['Password'] = TempPasswordObj
        EnteredEmail = request.get_json()['Email']
        EnteredPasswordBeforeHash = request.get_json()['Password']
        EnteredPassword = hashlib.sha224(EnteredPasswordBeforeHash.encode()).hexdigest()
        FoundUsers = User.query.filter_by(Email=EnteredEmail, Password=EnteredPassword).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('Email or password is incorrect')

        if FoundUsers[0].IsActive == True:
            ReturnObj.RoleId = FoundUsers[0].RoleId
        else:
            RaisedError = True
            ErrorCode = 2
            raise Exception('User is not active yet')
        TokenObj = MainToken()
        TokenObj.Email = EnteredEmail
        TokenStr = TokenObj.CreateTokenStr()
        TokenObj.Token = TokenStr
        TokenObj.Role = ReturnObj.RoleId
        MainTokens[TokenStr] = TokenObj
        ReturnObj.Token = TokenStr
        ReturnObj.MethodStatus = True
        ReturnObj.Email = EnteredEmail
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='Login', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='Login', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/SendEmailForForgetPassword', methods=['POST'])
@cross_origin()
def SendEmailForForgetPassword():
    ReturnObj = SendEmailForForgetPasswordResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='SendEmailForForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        EnteredEmail = request.get_json()['Email']
        FoundUsers = User.query.filter_by(Email=EnteredEmail).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('There is no account for this email')
        ValidationCode = random.randint(1000, 9999)
        TokenObj = ForgetPasswordToken()
        TokenObj.Email = EnteredEmail
        TokenStr = TokenObj.CreateTokenStr()
        TokenObj.Token = TokenStr
        TokenObj.ValidationCode = str(ValidationCode)
        ForgetPasswordsTokens[TokenStr] = TokenObj
        ReturnObj.Token = TokenStr
        fromaddr = application.config['SENT_EMAIL_USER']
        toaddr = EnteredEmail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Validation Code"
        body = "The ValidationCode is " + str(ValidationCode)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, application.config['SENT_EMAIL_PASSWORD'])
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='SendEmailForForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='SendEmailForForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/VerifyForgetPassword', methods=['POST'])
@cross_origin()
def VerifyForgetPassword():
    ReturnObj = VerifyForgetPasswordResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='VerifyForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        ValidationCode = request.get_json()['ValidationCode']
        Token = request.get_json()['Token']
        TokenObj = ForgetPasswordsTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.ValidationCode == ValidationCode:
            ForgetPasswordsTokens[Token].IsCodeValidate = True
            ReturnObj.IsVerified = True
        else:
            RaisedError = True
            ErrorCode = 2
            raise Exception('Validation Code is incorrect')
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='VerifyForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='VerifyForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/ChangeForgetPassword', methods=['POST'])
@cross_origin()
def ChangeForgetPassword():
    ReturnObj = ChangeForgetPasswordResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        TempPasswordObj = request.get_json()['Password']
        request.get_json()['Password'] = ''
        NewReqLog = Services_Log(Service_Name='ChangeForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        request.get_json()['Password'] = TempPasswordObj
        Email = request.get_json()['Email']
        PasswordBeforeHash = request.get_json()['Password']
        Password = hashlib.sha224(PasswordBeforeHash.encode()).hexdigest()
        Token = request.get_json()['Token']
        TokenObj = ForgetPasswordsTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        if TokenObj.IsCodeValidate == False:
            RaisedError = True
            ErrorCode = 3
            raise Exception('You are not Authorized')
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundUsers[0].Password = Password
        db.session.commit()
        ReturnObj.PasswordChanged = True
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='ChangeForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='ChangeForgetPassword', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetCountries', methods=['POST'])
@cross_origin()
def GetCountries():
    ReturnObj = GetCountriesResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetCountries', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalCountriesList = []
        FoundCountries = Countries.query.all()
        FoundCountriesCount = 0
        for CountryItem in FoundCountries:
            FinalCountriesList.append({"country_id": CountryItem.country_id, "country_name": CountryItem.country_name})
            FoundCountriesCount = FoundCountriesCount + 1
        if FoundCountriesCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.CountriesList = FinalCountriesList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetCountries', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetCountries', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetRegions', methods=['POST'])
@cross_origin()
def GetRegions():
    ReturnObj = GetRegionsResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetRegions', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalRegionsList = []
        CountryID = 0
        try:
            CountryID = request.get_json()['CountryID']
        except:
            CountryID = 0
        FoundRegions = []
        if CountryID == 0:
            FoundRegions = Regions.query.all()
        else:
            FoundRegions = Regions.query.filter_by(country_id=CountryID).all()
        FoundRegionsCount = 0
        for RegionItem in FoundRegions:
            FinalRegionsList.append({"region_id": RegionItem.region_id, "region_name": RegionItem.region_name,
                                     "country_id": RegionItem.country_id})
            FoundRegionsCount = FoundRegionsCount + 1
        if FoundRegionsCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.RegionsList = FinalRegionsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetRegions', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetRegions', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetCities', methods=['POST'])
@cross_origin()
def GetCities():
    ReturnObj = GetCitiesResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetCities', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalCitiesList = []
        RegionID = 0
        try:
            RegionID = request.get_json()['RegionID']
        except:
            RegionID = 0
        FoundCities = []
        if RegionID == 0:
            FoundCities = Cities.query.all()
        else:
            FoundCities = Cities.query.filter_by(region_id=RegionID).all()
        FoundCitiesCount = 0
        for CityItem in FoundCities:
            FinalCitiesList.append(
                {"city_id": CityItem.city_id, "city_name": CityItem.city_name, "country_id": CityItem.country_id,
                 "region_id": CityItem.region_id})
            FoundCitiesCount = FoundCitiesCount + 1
        if FoundCitiesCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.CitiesList = FinalCitiesList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetCities', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetCities', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/SendEmailForRegistr', methods=['POST'])
@cross_origin()
def SendEmailForRegistr():
    ReturnObj = SendEmailForRegistrResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='SendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        EnteredEmail = request.get_json()['Email']
        FoundUsers = User.query.filter_by(Email=EnteredEmail).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount != 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('There is account for this email')
        ValidationCode = random.randint(1000, 9999)
        TokenObj = RegistrToken()
        TokenObj.Email = EnteredEmail
        TokenStr = TokenObj.CreateTokenStr()
        TokenObj.Token = TokenStr
        TokenObj.ValidationCode = str(ValidationCode)
        RegistrTokens[TokenStr] = TokenObj
        ReturnObj.Token = TokenStr
        fromaddr = application.config['SENT_EMAIL_USER']
        toaddr = EnteredEmail
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Validation Code"
        body = "The ValidationCode is " + str(ValidationCode)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, application.config['SENT_EMAIL_PASSWORD'])
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='SendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='SendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/ReSendEmailForRegistr', methods=['POST'])
@cross_origin()
def ReSendEmailForRegistr():
    ReturnObj = ReSendEmailForRegistrResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='ReSendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Token = request.get_json()['Token']
        TokenObj = RegistrTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        ValidationCode = random.randint(1000, 9999)
        RegistrTokens[Token].ValidationCode = str(ValidationCode)
        Email = TokenObj.Email
        fromaddr = application.config['SENT_EMAIL_USER']
        toaddr = Email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Validation Code"
        body = "The ValidationCode is " + str(ValidationCode)
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, application.config['SENT_EMAIL_PASSWORD'])
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='ReSendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='ReSendEmailForRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/VerifyRegistr', methods=['POST'])
@cross_origin()
def VerifyRegistr():
    ReturnObj = VerifyRegistrResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='VerifyRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        ValidationCode = request.get_json()['ValidationCode']
        Token = request.get_json()['Token']
        TokenObj = RegistrTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.ValidationCode == ValidationCode:
            RegistrTokens[Token].IsCodeValidate = True
            ReturnObj.IsVerified = True
        else:
            RaisedError = True
            ErrorCode = 2
            raise Exception('Validation Code is incorrect')
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='VerifyRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='VerifyRegistr', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetForgetPasswordsTokens', methods=['POST'])
def GetForgetPasswordsTokens():
    ReturnObj = {}
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetForgetPasswordsTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        SuperKey = request.get_json()['SuperKey']
        SuperKeyAfterEnc = hashlib.sha224(SuperKey.encode()).hexdigest()
        if SuperKeyAfterEnc != application.config['ADMINSUPERKEY']:
            ReturnObj = {"error_message": "you are not authorized"}
        else:
            for key in ForgetPasswordsTokens:
                ReturnObj[key] = ForgetPasswordsTokens[key].Format()
    except Exception as ex:
        ReturnObj = {"error_message": ex.args[0]}
    try:
        NewResLog = Services_Log(Service_Name='GetForgetPasswordsTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetForgetPasswordsTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj)


@application.route('/GetRegistrTokens', methods=['POST'])
def GetRegistrTokens():
    ReturnObj = {}
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetRegistrTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        SuperKey = request.get_json()['SuperKey']
        SuperKeyAfterEnc = hashlib.sha224(SuperKey.encode()).hexdigest()
        if SuperKeyAfterEnc != application.config['ADMINSUPERKEY']:
            ReturnObj = {"error_message": "you are not authorized"}
        else:
            for key in RegistrTokens:
                ReturnObj[key] = RegistrTokens[key].Format()
    except Exception as ex:
        ReturnObj = {"error_message": ex.args[0]}
    try:
        NewResLog = Services_Log(Service_Name='GetRegistrTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetRegistrTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj)


@application.route('/GetMainTokens', methods=['POST'])
def GetMainTokens():
    ReturnObj = {}
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetMainTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        SuperKey = request.get_json()['SuperKey']
        SuperKeyAfterEnc = hashlib.sha224(SuperKey.encode()).hexdigest()
        if SuperKeyAfterEnc != application.config['ADMINSUPERKEY']:
            ReturnObj = {"error_message": "you are not authorized"}
        else:
            for key in MainTokens:
                ReturnObj[key] = MainTokens[key].Format()
    except Exception as ex:
        ReturnObj = {"error_message": ex.args[0]}
    try:
        NewResLog = Services_Log(Service_Name='GetMainTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetMainTokens', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj)


@application.route('/RegistrNewUser', methods=['POST'])
@cross_origin()
def RegistrNewUser():
    ReturnObj = RegistrNewUserResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        TempPasswordObj = request.get_json()['Password']
        request.get_json()['Password'] = ''
        NewReqLog = Services_Log(Service_Name='RegistrNewUser', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        request.get_json()['Password'] = TempPasswordObj
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = RegistrTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        if TokenObj.IsCodeValidate == False:
            RaisedError = True
            ErrorCode = 3
            raise Exception('You are not Authorized')
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount != 0:
            RaisedError = True
            ErrorCode = 4
            raise Exception('There is account for this email')
        PasswordBeforeHash = request.get_json()['Password']
        Password = hashlib.sha224(PasswordBeforeHash.encode()).hexdigest()
        CreatedBy = request.get_json()['CreatedBy']
        RoleId = request.get_json()['RoleId']
        CountryID = request.get_json()['CountryID']
        RegionID = request.get_json()['RegionID']
        CityID = request.get_json()['CityID']
        if RoleId != 4 and RoleId != 5:
            RaisedError = True
            ErrorCode = 5
            raise Exception('Something went wrong')
        CurrentDateTime = datetime.now()
        NewUser = User(Email=Email, Password=Password, IsActive=True, CreatedAt=CurrentDateTime,
                       EditedAt=CurrentDateTime, CreatedBy=CreatedBy, EditedBy=CreatedBy, RoleId=RoleId,
                       CountryID=CountryID, RegionID=RegionID, CityID=CityID)

        first_name = ''
        last_name = ''
        company_name = ''
        contact_no = ''
        cr_file = ''
        mobile = ''
        date_of_birth = ''
        FinalDOB = ''
        gender_id = ''

        if RoleId == 4:
            first_name = request.get_json()['first_name']
            last_name = request.get_json()['last_name']
            company_name = request.get_json()['company_name']
            contact_no = request.get_json()['contact_no']
            cr_file = request.get_json()['cr_file']

        if RoleId == 5:
            first_name = request.get_json()['first_name']
            last_name = request.get_json()['last_name']
            mobile = request.get_json()['mobile']
            date_of_birth = request.get_json()['date_of_birth']
            FinalDOB = datetime.strptime(date_of_birth, '%d/%m/%y %H:%M:%S')
            gender_id = request.get_json()['gender_id']

        db.session.add(NewUser)
        db.session.commit()
        TheNewUser = User.query.filter_by(Email=Email).first()
        if RoleId == 4:
            NewOrganizer = Event_Organizer(first_name=first_name, last_name=last_name, company_name=company_name,
                                           contact_no=contact_no, cr_file=cr_file, user_id=TheNewUser.UserId)
            db.session.add(NewOrganizer)
            db.session.commit()
        if RoleId == 5:
            NewGuest = Guest(first_name=first_name, last_name=last_name, email=Email, password=Password, mobile=mobile,
                             date_of_birth=FinalDOB, user_id=TheNewUser.UserId, gender_id=gender_id)
            db.session.add(NewGuest)
            db.session.commit()
        ReturnObj.IsUserRegistred = True
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='RegistrNewUser', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='RegistrNewUser', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/ChangePersonalInfo', methods=['POST'])
@cross_origin()
def ChangePersonalInfo():
    ReturnObj = ChangePersonalInfoResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        ThereIsPassword = False
        TempPasswordObj = ''
        try:
            TempPasswordObj = request.get_json()['Password']
            request.get_json()['Password'] = ''
            ThereIsPassword = True
        except:
            ThereIsPassword = False
        NewReqLog = Services_Log(Service_Name='ChangePersonalInfo', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        if ThereIsPassword == True:
            request.get_json()['Password'] = TempPasswordObj
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 3
            raise Exception('There is no account for this email')
        RoleId = request.get_json()['RoleId']
        if RoleId != 4 and RoleId != 5:
            RaisedError = True
            ErrorCode = 4
            raise Exception('Something went wrong')
        Password = 0
        first_name = 0
        last_name = 0
        mobile = 0
        contact_no = 0
        CountryID = 0
        RegionID = 0
        CityID = 0
        if RoleId == 4:
            UpdateUser = User.query.filter_by(Email=Email).first()
            UpdateEventOrganizer = Event_Organizer.query.filter_by(user_id=UpdateUser.UserId).first()
            try:
                PasswordBeforeHash = request.get_json()['Password']
                Password = hashlib.sha224(PasswordBeforeHash.encode()).hexdigest()
                UpdateUser.Password = Password
                db.session.commit()
            except:
                db.session.rollback()
                Password = 0
            try:
                first_name = request.get_json()['first_name']
                UpdateEventOrganizer.first_name = first_name
                db.session.commit()
            except:
                db.session.rollback()
                first_name = 0
            try:
                last_name = request.get_json()['last_name']
                UpdateEventOrganizer.last_name = last_name
                db.session.commit()
            except:
                db.session.rollback()
                last_name = 0
            try:
                contact_no = request.get_json()['contact_no']
                UpdateEventOrganizer.contact_no = contact_no
                db.session.commit()
            except:
                db.session.rollback()
                contact_no = 0
            try:
                CountryID = request.get_json()['CountryID']
                UpdateUser.CountryID = CountryID
                db.session.commit()
            except:
                db.session.rollback()
                CountryID = 0
            try:
                RegionID = request.get_json()['RegionID']
                UpdateUser.RegionID = RegionID
                db.session.commit()
            except:
                db.session.rollback()
                RegionID = 0
            try:
                CityID = request.get_json()['CityID']
                UpdateUser.CityID = CityID
                db.session.commit()
            except:
                db.session.rollback()
                CityID = 0
        if RoleId == 5:
            UpdateUser = User.query.filter_by(Email=Email).first()
            UpdateGuest = Guest.query.filter_by(user_id=UpdateUser.UserId).first()
            try:
                PasswordBeforeHash = request.get_json()['Password']
                Password = hashlib.sha224(PasswordBeforeHash.encode()).hexdigest()
                UpdateUser.Password = Password
                db.session.commit()
            except:
                db.session.rollback()
                Password = 0
            try:
                first_name = request.get_json()['first_name']
                UpdateGuest.first_name = first_name
                db.session.commit()
            except:
                db.session.rollback()
                first_name = 0
            try:
                last_name = request.get_json()['last_name']
                UpdateGuest.last_name = last_name
                db.session.commit()
            except:
                db.session.rollback()
                last_name = 0
            try:
                mobile = request.get_json()['mobile']
                UpdateGuest.mobile = mobile
                db.session.commit()
            except:
                db.session.rollback()
                mobile = 0
            try:
                CountryID = request.get_json()['CountryID']
                UpdateUser.CountryID = CountryID
                db.session.commit()
            except:
                db.session.rollback()
                CountryID = 0
            try:
                RegionID = request.get_json()['RegionID']
                UpdateUser.RegionID = RegionID
                db.session.commit()
            except:
                db.session.rollback()
                RegionID = 0
            try:
                CityID = request.get_json()['CityID']
                UpdateUser.CityID = CityID
                db.session.commit()
            except:
                db.session.rollback()
                CityID = 0
        ReturnObj.IsInfoChanged = True
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='ChangePersonalInfo', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='ChangePersonalInfo', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/CreateNewEvent', methods=['POST'])
@cross_origin()
def CreateNewEvent():
    ReturnObj = CreateNewEventResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='CreateNewEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        name = request.get_json()['name']
        num_of_tickets = request.get_json()['num_of_tickets']
        country_id = request.get_json()['country_id']
        region_id = request.get_json()['region_id']
        city_id = request.get_json()['city_id']
        TextLocation = request.get_json()['TextLocation']
        EventImage = request.get_json()['EventImage']
        Summary = request.get_json()['Summary']
        HaveMoreLikeThis = request.get_json()['HaveMoreLikeThis']

        location_lang = 0.0
        location_lat = 0.0
        location_url = ''

        try:
            location_lang = request.get_json()['location_lang']
        except:
            location_lang = 0.0

        try:
            location_lat = request.get_json()['location_lat']
        except:
            location_lat = 0.0

        try:
            location_url = request.get_json()['location_url']
        except:
            location_url = ''

        if location_url == '':
            if location_lang == 0.0 or location_lat == 0.0:
                RaisedError = True
                ErrorCode = 3
                raise Exception('one of the two location methods must be send')

        if TokenObj.Role != 1 and TokenObj.Email != 2:
            RaisedError = True
            ErrorCode = 4
            raise Exception('You are not Authorized to use this service')

        event_date = request.get_json()['event_date']
        event_days = request.get_json()['event_days']
        event_day_duration = request.get_json()['event_day_duration']
        event_total_duration = request.get_json()['event_total_duration']

        categoriesList = request.get_json()['categoriesList']

        TicketsList = request.get_json()['TicketsList']

        Event_Obj = Event(name=name, num_of_tickets=num_of_tickets, country_id=country_id, region_id=region_id,
                          city_id=city_id, location_lang=location_lang, location_lat=location_lat,
                          location_url=location_url, TextLocation=TextLocation, EventImage=EventImage, Summary=Summary,
                          HaveMoreLikeThis=HaveMoreLikeThis)
        db.session.add(Event_Obj)
        db.session.commit()

        Event_Days_Obj = Event_Days(event_date=event_date, event_days=event_days, event_id=Event_Obj.event_id,
                                    event_day_duration=event_day_duration,
                                    event_total_duration=event_total_duration)
        db.session.add(Event_Days_Obj)
        db.session.commit()

        for categoryItem in categoriesList:
            Event_Categories_Details_Obj = Event_Categories_Details(category_id=categoryItem,
                                                                    event_id=Event_Obj.event_id)
            db.session.add(Event_Categories_Details_Obj)
            db.session.commit()

        for TicketsItem in TicketsList:
            price = TicketsItem['price']
            ticket_type_id = TicketsItem['ticket_type_id']
            seats_total_number = TicketsItem['seats_total_number']
            special_note = TicketsItem['special_note']
            duration = TicketsItem['duration']
            isHaveSeats = TicketsItem['isHaveSeats']
            Tickets_Obj = Tickets(price=price, event_id=Event_Obj.event_id, ticket_type_id=ticket_type_id,
                                  seats_total_number=seats_total_number, special_note=special_note,
                                  duration=duration, isHaveSeats=isHaveSeats)
            db.session.add(Tickets_Obj)
            db.session.commit()
        ReturnObj.MethodStatus = True
        ReturnObj.IsEventCreated = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='CreateNewEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='CreateNewEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetCategoriesForMain', methods=['POST'])
@cross_origin()
def GetCategoriesForMain():
    ReturnObj = GetCategoriesForMainResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetCategoriesForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        EnteredRole = 0
        try:
            EnteredRole = request.get_json()['Role']
        except:
            EnteredRole = 0
        FinalCategoriesList = []
        FoundCategories = Event_SuperCategories.query.all()
        FoundCategoriesCount = 0
        FinalCategoriesList.append(
            {"category_id": 0, "category_name": "All", "category_image": None, "IsNearYou": False})
        if EnteredRole != 0:
            FinalCategoriesList.append(
                {"category_id": 0, "category_name": "Near You", "category_image": None, "IsNearYou": True})
        for CategoryItem in FoundCategories:
            FinalCategoriesList.append(
                {"category_id": CategoryItem.supercategory_id, "category_nameEn": CategoryItem.category_nameEn,"category_nameAr": CategoryItem.category_nameAr,
                 "category_image": CategoryItem.category_image, "IsNearYou": False})
            FoundCategoriesCount = FoundCategoriesCount + 1
        if FoundCategoriesCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.CategoriesList = FinalCategoriesList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetCategoriesForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetCategoriesForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetEventsByCategoryForMain', methods=['POST'])
@cross_origin()
def GetEventsByCategoryForMain():
    ReturnObj = GetEventsByCategoryForMainResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetEventsByCategoryForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalEventsList = []
        CategoryID = 0
        try:
            CategoryID = request.get_json()['CategoryID']
        except:
            CategoryID = 0
        IsNearYou = False
        try:
            IsNearYou = request.get_json()['IsNearYou']
        except:
            IsNearYou = False
        FoundEvents = []
        if IsNearYou == True:
            EnteredEmail = request.get_json()['Email']
            EnteredRole = request.get_json()['Role']
            FoundUsers = User.query.filter_by(Email=EnteredEmail, RoleId=EnteredRole).all()
            FoundEvents = db.session.query(Event, Event_Days).filter(Event.event_id == Event_Days.event_id,
                                                                     Event.city_id == FoundUsers[0].CityID).all()
        elif CategoryID == 0:
            FoundEvents = db.session.query(Event, Event_Days).filter(Event.event_id == Event_Days.event_id).all()
        else:
            # FoundEvents = db.session.query(Event,Event_Days,Event_Categories_Details).filter(Event.event_id == Event_Days.event_id and Event.event_id == Event_Categories_Details.event_id and Event_Categories_Details.category_id == CategoryID).order_by(desc(Event_Days.event_date)).limit(4).all()
            FoundEvents = db.session.query(Event, Event_Days, Event_Categories_Details).filter(
                Event.event_id == Event_Days.event_id, Event.event_id == Event_Categories_Details.event_id,
                Event_Categories_Details.supercategory_id == CategoryID).all()
        FoundEventsCount = 0
        FoundEventsModifyed = []
        for EventItem in FoundEvents:
            AudienceTypeList = AudienceType.query.filter_by(ID=EventItem.Event.AudienceTypeID).all()
            Event_TypeList = Event_Type.query.filter_by(ID=EventItem.Event.EventTypeID).all()
            FoundEventsModifyed.append({"event_id": EventItem.Event.event_id, "name": EventItem.Event.name,
                                        "event_date": datetime.strptime(EventItem.Event_Days.event_date, '%y-%m-%d'),
                                        "Location": EventItem.Event.TextLocation,
                                        "EventImage": EventItem.Event.EventImage,
                                        "AudienceTypeEN": AudienceTypeList[0].DescEn,
                                        "AudienceTypeAR": AudienceTypeList[0].DescAr,
                                        "EventTypeEN": Event_TypeList[0].DescEn,
                                        "EventTypeAR": Event_TypeList[0].DescAr
                                        })
            FoundEventsCount = FoundEventsCount + 1
        if FoundEventsCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        FoundEventsModifyed.sort(key=lambda x: x.get('event_date'), reverse=True)
        FinalListCounter = 0
        for FinalEventItem in FoundEventsModifyed:
            if FinalListCounter == 4:
                break
            FoundTickets = Tickets.query.filter_by(event_id=FinalEventItem.get('event_id')).all()
            FoundTickets.sort(key=lambda x: x.price)
            FinalEventsList.append({"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                                    "event_date": FinalEventItem.get('event_date'),
                                    "Location": FinalEventItem.get('Location'),
                                    "EventImage": FinalEventItem.get('EventImage'),
                                    "TicketPrice": FoundTickets[0].price,
                                    "AudienceTypeEN": FinalEventItem.get('AudienceTypeEN'),
                                    "AudienceTypeAR": FinalEventItem.get('AudienceTypeAR'),
                                    "EventTypeEN": FinalEventItem.get('EventTypeEN'),
                                    "EventTypeAR": FinalEventItem.get('EventTypeAR')})
            FinalListCounter = FinalListCounter + 1
        ReturnObj.EventsList = FinalEventsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetEventsByCategoryForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetEventsByCategoryForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetEventDetails', methods=['POST'])
@cross_origin()
def GetEventDetails():
    ReturnObj = GetEventDetailsResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetEventDetails', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        EventID = request.get_json()['EventID']
        FoundEventDetails = {}
        FoundEvents = Event.query.filter_by(event_id=EventID).all()
        FoundSubCategories = db.session.query(Event_Categories_Details, Event_SubCategories).filter(
            Event_Categories_Details.event_id == EventID,
            Event_Categories_Details.subcategory_id == Event_SubCategories.subcategory_id).all()
        FoundTickets = Tickets.query.filter_by(event_id=EventID).all()
        FoundFAQs = Event_FAQs.query.filter_by(EventId=EventID).all()
        FoundTermsAndConditions = Event_TermsAndConditions.query.filter_by(EventId=EventID).all()
        FoundEventsCount = 0
        FoundTicketsCount = 0
        for x in FoundEvents:
            FoundEventsCount = FoundEventsCount + 1
        if FoundEventsCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data found for this event')
        for y in FoundTickets:
            FoundTicketsCount = FoundTicketsCount + 1
        if FoundTicketsCount == 0:
            RaisedError = True
            ErrorCode = 2
            raise Exception('No Data found for this event')
        CategoriesList = []
        SubCategoriesList = []
        SuperCategoriesList = []
        TicketsList = []
        FAQsList = []
        TermsAndConditionsList = []
        for SubCategoryItem in FoundSubCategories:
            FoundCategory = Event_Categories.query.filter_by(category_id=SubCategoryItem.Event_Categories_Details.category_id).first()
            FoundSuperCategory = Event_SuperCategories.query.filter_by(supercategory_id=SubCategoryItem.Event_Categories_Details.supercategory_id).first()
            SubCategoriesList.append(
                {"ID": SubCategoryItem.Event_SubCategories.subcategory_id,
                 "NameEN": SubCategoryItem.Event_SubCategories.category_nameEn
                    , "NameAR": SubCategoryItem.Event_SubCategories.category_nameAr})
            CategoriesList.append(
                {"ID": FoundCategory.category_id,
                 "NameEN": FoundCategory.category_nameEn
                    , "NameAR": FoundCategory.category_nameAr})
            SuperCategoriesList.append(
                {"ID": FoundSuperCategory.supercategory_id, "NameEN": FoundSuperCategory.category_nameEn
                 ,"NameAR": FoundSuperCategory.category_nameAr})
        for TicketItem in FoundTickets:
            TicketsList.append({"price": TicketItem.price})
        for FAQItem in FoundFAQs:
            FAQsList.append({"Question": FAQItem.Question, "Answer": FAQItem.Answer})
        for TermsAndConditionsItem in FoundTermsAndConditions:
            TermsAndConditionsList.append(
                {"Header": TermsAndConditionsItem.Header, "Context": TermsAndConditionsItem.Context})
        AudienceTypeList =  AudienceType.query.filter_by(ID=FoundEvents[0].AudienceTypeID).all()
        Event_TypeList = Event_Type.query.filter_by(ID=FoundEvents[0].EventTypeID).all()
        FoundEventDetails = {"EventID": FoundEvents[0].event_id, "EventImage": FoundEvents[0].EventImage,
                             "EventName": FoundEvents[0].name,
                             "EventCategories": CategoriesList, "EventTickets": TicketsList,
                             "EventSubCategories": SubCategoriesList, "EventSuperCategories": SuperCategoriesList,
                             "EventLocation": FoundEvents[0].TextLocation,
                             "Summary": FoundEvents[0].Summary, "FAQs": FAQsList,
                             "TermsAndConditions": TermsAndConditionsList,"MinimumAge":FoundEvents[0].MinimumAge,
                             "AudienceTypeEN":AudienceTypeList[0].DescEn,"AudienceTypeAR":AudienceTypeList[0].DescAr,
                             "EventTypeEN":Event_TypeList[0].DescEn,"EventTypeAR":Event_TypeList[0].DescAr,
                             "MoreLikeThis": FoundEvents[0].HaveMoreLikeThis, "IsBook": True, "BookDescription": "Book"}
        ReturnObj.EventDetails = FoundEventDetails
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetEventDetails', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetEventDetails', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetMoreLikeThisEventsForEvents', methods=['POST'])
@cross_origin()
def GetMoreLikeThisEventsForEvents():
    ReturnObj = GetMoreLikeThisEventsForEventsResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetMoreLikeThisEventsForEvents', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        EventID = request.get_json()['EventID']
        FinalEventsList = []
        SendedEventCount = 0
        SendedEvent = Event.query.filter_by(event_id=EventID).all()
        for x in SendedEvent:
            SendedEventCount = SendedEventCount + 1
        if SendedEventCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data found for this event')
        FoundEvents = db.session.query(Event, Event_Days).filter(Event.event_id == Event_Days.event_id,
                                                                 Event.region_id == SendedEvent[0].region_id).all()

        FoundEventsCount = 0
        FoundEventsModifyed = []
        for EventItem in FoundEvents:
            FoundEventsModifyed.append({"event_id": EventItem.Event.event_id, "name": EventItem.Event.name,
                                        "event_date": datetime.strptime(EventItem.Event_Days.event_date, '%y-%m-%d'),
                                        "Location": EventItem.Event.TextLocation,
                                        "EventImage": EventItem.Event.EventImage})
            FoundEventsCount = FoundEventsCount + 1
        if FoundEventsCount == 0:
            RaisedError = True
            ErrorCode = 2
            raise Exception('No Data Found')
        FoundEventsModifyed.sort(key=lambda x: x.get('event_date'), reverse=True)
        FinalListCounter = 0
        for FinalEventItem in FoundEventsModifyed:
            if FinalListCounter == 4:
                break
            FoundTickets = Tickets.query.filter_by(event_id=FinalEventItem.get('event_id')).all()
            FoundTickets.sort(key=lambda x: x.price)
            FinalEventsList.append({"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                                    "event_date": FinalEventItem.get('event_date'),
                                    "Location": FinalEventItem.get('Location'),
                                    "EventImage": FinalEventItem.get('EventImage'),
                                    "TicketPrice": FoundTickets[0].price})
            FinalListCounter = FinalListCounter + 1
        ReturnObj.EventsList = FinalEventsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetMoreLikeThisEventsForEvents', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetMoreLikeThisEventsForEvents', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetPlacesAroundYou', methods=['POST'])
@cross_origin()
def GetPlacesAroundYou():
    ReturnObj = GetPlacesAroundYouResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetPlacesAroundYou', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalCitiesList = []
        RegionID = 0
        EnteredEmail = request.get_json()['Email']
        EnteredRole = request.get_json()['Role']
        FoundUsers = User.query.filter_by(Email=EnteredEmail, RoleId=EnteredRole).all()
        for UserItem in FoundUsers:
            RegionID = UserItem.RegionID
        FoundCities = []
        if RegionID == 0:
            FoundCities = Cities.query.all()
        else:
            FoundCities = Cities.query.filter_by(region_id=RegionID).all()
        FoundCitiesCount = 0
        for CityItem in FoundCities:
            FoundEvents = Event.query.filter_by(city_id=CityItem.city_id).all()
            FoundEventsCounter = 0
            for EventItem in FoundEvents:
                FoundEventsCounter = FoundEventsCounter + 1
            FinalCitiesList.append(
                {"city_id": CityItem.city_id, "city_name": CityItem.city_name, "country_id": CityItem.country_id,
                 "region_id": CityItem.region_id, "EventsNo": FoundEventsCounter})
            FoundCitiesCount = FoundCitiesCount + 1
        if FoundCitiesCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.CitiesList = FinalCitiesList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetPlacesAroundYou', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetPlacesAroundYou', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetSlidersForMain', methods=['POST'])
@cross_origin()
def GetSlidersForMain():
    ReturnObj = GetSlidersForMainResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetSlidersForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalSlidersList = []
        EnteredRole = request.get_json()['Role']
        FoundSlidersCount = 0
        FoundSliders = Slider.query.filter_by(IsActive=True, Role=EnteredRole).all()
        for SliderItem in FoundSliders:
            FinalSlidersList.append(
                {"ID": SliderItem.ID, "Description": SliderItem.Description, "Image": SliderItem.Image})
            FoundSlidersCount = FoundSlidersCount + 1
        if FoundSlidersCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.SlidersList = FinalSlidersList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetSlidersForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetSlidersForMain', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetMenu', methods=['POST'])
@cross_origin()
def GetMenu():
    ReturnObj = GetMenuResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetMenu', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalMenuList = []
        EnteredRole = request.get_json()['Role']
        FoundMenuiCount = 0
        FoundMenu = Menu.query.filter_by(IsActive=True, Role=EnteredRole).all()
        for MenuItem in FoundMenu:
            FinalMenuList.append({"ID": MenuItem.ID, "Description": MenuItem.Description})
            FoundMenuiCount = FoundMenuiCount + 1
        if FoundMenuiCount == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ReturnObj.MenuList = FinalMenuList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetMenu', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetMenu', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetTicketsForEvent', methods=['POST'])
@cross_origin()
def GetTicketsForEvent():
    ReturnObj = GetTicketsForEventResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetTicketsForEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalTicketsList = []
        EventID = request.get_json()['EventId']
        FoundTicketsCount = 0
        FoundTickets = db.session.query(Tickets, Ticket_type).filter(Tickets.event_id == EventID,
                                                                     Tickets.ticket_type_id == Ticket_type.id).all()
        FounEvents = Event_Days.query.filter_by(event_id=EventID).all()
        EventDateStr = ""
        EventDaysStr = ""
        for EventItem in FounEvents:
            EventDateStr = EventItem.event_date
            EventDaysStr = EventItem.event_days
            break
        if EventDateStr == "" or EventDaysStr == "":
            RaisedError = True
            ErrorCode = 1
            raise Exception('No Data Found')
        ListOfDaysWithDate = []
        EventDate = datetime.strptime(EventDateStr, '%y-%m-%d')
        EventDays = EventDaysStr.split(",")
        WeekCounter = 0
        while WeekCounter < 7:
            TempEventDate = EventDate + timedelta(days=WeekCounter)
            EventDateName = calendar.day_name[TempEventDate.weekday()]
            if EventDays.__contains__(EventDateName):
                ListOfDaysWithDate.append(EventDateName + " " + str(TempEventDate))
            WeekCounter = WeekCounter + 1
        for TicketItem in FoundTickets:
            TicketId = TicketItem.Tickets.id
            LimitedTime = datetime.now() - timedelta(minutes=30)
            FoundUsersTickets = Users_Tickets.query.filter_by(TicketId=TicketId).all()
            ExcludedSeatsNumber = 0
            for FoundUsersItem in FoundUsersTickets:
                if FoundUsersItem.IsActive == True or (
                        FoundUsersItem.IsActive == False and FoundUsersItem.CreatedAt >= LimitedTime):
                    ExcludedSeatsNumber = ExcludedSeatsNumber + 1
            SeatsAvalible = TicketItem.Tickets.seats_total_number - ExcludedSeatsNumber
            FinalTicketsList.append({"TicketID": TicketId, "TicketTypeID": TicketItem.Ticket_type.id,
                                     "TicketTypeDesc": TicketItem.Ticket_type.type
                                        , "Price": TicketItem.Tickets.price,
                                     "SpecialNote": TicketItem.Tickets.special_note
                                        , "SeatsAvalible": SeatsAvalible, "ListOfDaysWithDate": ListOfDaysWithDate})
            FoundTicketsCount = FoundTicketsCount + 1
        if FoundTicketsCount == 0:
            RaisedError = True
            ErrorCode = 2
            raise Exception('No Data Found')
        ReturnObj.TicketsList = FinalTicketsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetTicketsForEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetTicketsForEvent', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetUpcomingAndPastEventsForUser', methods=['POST'])
@cross_origin()
def GetUpcomingAndPastEventsForUser():
    ReturnObj = GetUpcomingAndPastEventsForUserResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetUpcomingAndPastEventsForUser', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 3
            raise Exception('There is no account for this email')
        FinalUpcomingEventsList = []
        FinalPastEventsList = []
        FoundEvents = db.session.query(Event, Event_Days, Users_Tickets).filter(Event.event_id == Event_Days.event_id,
                                                                                Event.event_id == Users_Tickets.EventId,
                                                                                Users_Tickets.UserId == FoundUsers[
                                                                                    0].UserId,
                                                                                Users_Tickets.IsActive == True).all()
        FoundEventsCount = 0
        FoundEventsModifyed = []
        for EventItem in FoundEvents:
            FoundUsersTickets = Tickets.query.filter_by(id=EventItem.Users_Tickets.TicketId).all()
            FoundEventsModifyed.append({"event_id": EventItem.Event.event_id, "name": EventItem.Event.name,
                                        "event_date": datetime.strptime(EventItem.Event_Days.event_date, '%y-%m-%d'),
                                        "Location": EventItem.Event.TextLocation,
                                        "EventImage": EventItem.Event.EventImage,
                                        "TicketPrice": FoundUsersTickets[0].price})
            FoundEventsCount = FoundEventsCount + 1
        if FoundEventsCount == 0:
            RaisedError = True
            ErrorCode = 4
            raise Exception('No Data Found')
        CurrentDate = datetime.now()
        for FinalEventItem in FoundEventsModifyed:
            if CurrentDate > FinalEventItem.get('event_date'):
                FinalPastEventsList.append(
                    {"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                     "event_date": FinalEventItem.get('event_date'), "Location": FinalEventItem.get('Location'),
                     "EventImage": FinalEventItem.get('EventImage'), "TicketPrice": FinalEventItem.get('TicketPrice')})
            else:
                FinalUpcomingEventsList.append(
                    {"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                     "event_date": FinalEventItem.get('event_date'), "Location": FinalEventItem.get('Location'),
                     "EventImage": FinalEventItem.get('EventImage'), "TicketPrice": FinalEventItem.get('TicketPrice')})
        ReturnObj.UpcomingEventsList = FinalUpcomingEventsList
        ReturnObj.PastEventsList = FinalPastEventsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetUpcomingAndPastEventsForUser', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetUpcomingAndPastEventsForUser', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetFilteredEventsWithPagination', methods=['POST'])
@cross_origin()
def GetFilteredEventsWithPagination():
    ReturnObj = GetFilteredEventsWithPaginationResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetFilteredEventsWithPagination', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        FinalEventsList = []
        CategoryID = 0
        try:
            CategoryID = request.get_json()['CategoryID']
        except:
            CategoryID = 0
        RegionID = 0
        try:
            RegionID = request.get_json()['RegionID']
        except:
            RegionID = 0
        PageNo = 0
        try:
            PageNo = request.get_json()['PageNo']
        except:
            PageNo = 0
        PageSize = 0
        try:
            PageSize = request.get_json()['PageSize']
        except:
            PageSize = 0
        FromDate = None
        try:
            FromDate = datetime.strptime(request.get_json()['FromDate'], '%y-%m-%d')
        except:
            FromDate = None
        ToDate = None
        try:
            ToDate = datetime.strptime(request.get_json()['ToDate'], '%y-%m-%d')
        except:
            ToDate = None
        if PageNo != 0 and PageSize == 0:
            RaisedError = True
            ErrorCode = 1
            raise Exception('Something went wrong')
        if PageNo == 0 and PageSize != 0:
            RaisedError = True
            ErrorCode = 2
            raise Exception('Something went wrong')
        if PageNo < 0:
            RaisedError = True
            ErrorCode = 3
            raise Exception('Something went wrong')
        if PageSize < 0:
            RaisedError = True
            ErrorCode = 4
            raise Exception('Something went wrong')
        FoundEvents = []
        if CategoryID == 0 and RegionID == 0:
            FoundEvents = db.session.query(Event, Event_Days).filter(Event.event_id == Event_Days.event_id).all()
        elif RegionID == 0:
            FoundEvents = db.session.query(Event, Event_Days, Event_Categories_Details).filter(
                Event.event_id == Event_Days.event_id, Event.event_id == Event_Categories_Details.event_id,
                Event_Categories_Details.supercategory_id == CategoryID).all()
        elif CategoryID == 0:
            FoundEvents = db.session.query(Event, Event_Days).filter(Event.event_id == Event_Days.event_id,
                                                                     Event.region_id == RegionID).all()
        else:
            FoundEvents = db.session.query(Event, Event_Days, Event_Categories_Details).filter(
                Event.event_id == Event_Days.event_id, Event.event_id == Event_Categories_Details.event_id,
                Event_Categories_Details.supercategory_id == CategoryID, Event.region_id == RegionID).all()
        FoundEventsCount = 0
        FoundEventsModifyed = []
        for EventItem in FoundEvents:
            EventDate = datetime.strptime(EventItem.Event_Days.event_date, '%y-%m-%d')
            ExcludidTimeItem = False
            if FromDate != None:
                if FromDate > EventDate:
                    ExcludidTimeItem = True
            if ToDate != None:
                if ToDate < EventDate:
                    ExcludidTimeItem = True
            if ExcludidTimeItem == False:
                FoundEventsModifyed.append(
                    {"event_id": EventItem.Event.event_id, "name": EventItem.Event.name, "event_date": EventDate,
                     "Location": EventItem.Event.TextLocation, "EventImage": EventItem.Event.EventImage})
                FoundEventsCount = FoundEventsCount + 1
        if FoundEventsCount == 0:
            RaisedError = True
            ErrorCode = 5
            raise Exception('No Data Found')
        FoundEventsModifyed.sort(key=lambda x: x.get('event_date'), reverse=True)
        FinalListCounter = 0
        PageLimit = (PageNo - 1) * PageSize
        PageCounter = 0
        for FinalEventItem in FoundEventsModifyed:
            if PageLimit == -1:
                FoundTickets = Tickets.query.filter_by(event_id=FinalEventItem.get('event_id')).all()
                FoundTickets.sort(key=lambda x: x.price)
                FinalEventsList.append({"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                                        "event_date": FinalEventItem.get('event_date'),
                                        "Location": FinalEventItem.get('Location'),
                                        "EventImage": FinalEventItem.get('EventImage'),
                                        "TicketPrice": FoundTickets[0].price})
            else:
                if PageCounter < PageLimit:
                    PageCounter = PageCounter + 1
                else:
                    if PageSize != 0 and FinalListCounter == PageSize:
                        break
                    FoundTickets = Tickets.query.filter_by(event_id=FinalEventItem.get('event_id')).all()
                    FoundTickets.sort(key=lambda x: x.price)
                    FinalEventsList.append(
                        {"event_id": FinalEventItem.get('event_id'), "name": FinalEventItem.get('name'),
                         "event_date": FinalEventItem.get('event_date'), "Location": FinalEventItem.get('Location'),
                         "EventImage": FinalEventItem.get('EventImage'), "TicketPrice": FoundTickets[0].price})
                    FinalListCounter = FinalListCounter + 1
        ReturnObj.EventsList = FinalEventsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetFilteredEventsWithPagination', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetFilteredEventsWithPagination', Email=EmailLog,
                                 CreatedAt=CurrentDateTime, Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/GetGuestUserProfileInfos', methods=['POST'])
@cross_origin()
def GetGuestUserProfileInfos():
    ReturnObj = GetGuestUserProfileInfosResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetGuestUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        if TokenObj.Role != 5:
            RaisedError = True
            ErrorCode = 3
            raise Exception('You are not Authorized')
        FoundUsers = db.session.query(User, Guest).filter(User.UserId == Guest.user_id, User.Email == Email).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 4
            raise Exception('There is no account for this email')
        GuestProfile = {"UserId": FoundUsers[0].User.UserId, "Email": FoundUsers[0].User.Email,
                        "CreatedAt": FoundUsers[0].User.CreatedAt, "FirstName": FoundUsers[0].Guest.first_name,
                        "LastName": FoundUsers[0].Guest.last_name, "Mobile": FoundUsers[0].Guest.mobile,
                        "DateOfBirth": FoundUsers[0].Guest.date_of_birth}
        ReturnObj.GuestProfile = GuestProfile
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetGuestUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetGuestUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())


@application.route('/Logout', methods=['POST'])
@cross_origin()
def Logout():
    ReturnObj = LogoutResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='Logout', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        MainTokens.pop(Token)
        ReturnObj.IsLogout = True
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='Logout', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='Logout', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())

@application.route('/GenrateQR', methods=['POST'])
@cross_origin()
def GenrateQR():
    ReturnObj = LogoutResponse()
    s = "http://127.0.0.1:5000/CheckQR/1"
    url = pyqrcode.create(s)
    #url.png('myqr.png', scale=6)
    encoded = url.png_as_base64_str(8)
    ReturnObj.EndErrorMessge = encoded
    return encoded

@application.route('/CheckQR/<int:UserTicketID>', methods=['GET'])
@cross_origin()
def CheckQR(UserTicketID):
    CheckResult = ""
    try:
        UserTickets = Users_Tickets.query.filter_by(ID=UserTicketID).first()
        if UserTickets.CheckedIn == True:
            CheckResult = "you already CheckedIn"
        else:
            UserTickets.CheckedIn = True
            UserTickets.CheckedInTime = datetime.now()
            db.session.commit()
            CheckResult = "CheckedIn succsefully"
    except:
        CheckResult = "something went wrong"
    return CheckResult

@application.route('/StartBookTicket', methods=['POST'])
@cross_origin()
def StartBookTicket():
    ReturnObj = StartBookTicketResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='StartBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        TicketsList = request.get_json()['TicketsList']
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundTickets = Tickets.query.filter_by(id=TicketsList[0]["TicketId"]).all()
        UserTicketList = []
        for TicketItem in TicketsList:
            QuantityCounter = 0
            while QuantityCounter < TicketItem["Quantity"]:
                QuantityCounter = QuantityCounter + 1
                NewUserTicket = Users_Tickets(UserId=FoundUsers[0].UserId, TicketId=TicketItem["TicketId"],
                                              TicketTypeId=TicketItem["TicketTypeId"],
                                              EventId=FoundTickets[0].event_id, SeatNum=None, CreatedAt=CurrentDateTime,
                                              IsActive=0,
                                              QR=None, CheckedIn=0, CheckedInTime=None)
                db.session.add(NewUserTicket)
                db.session.commit()
                UserTicketList.append(NewUserTicket.ID)

        ReturnObj.UserTicketList = UserTicketList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='StartBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='StartBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())

@application.route('/FinshBookTicket', methods=['POST'])
@cross_origin()
def FinshBookTicket():
    ReturnObj = FinshBookTicketResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='FinshBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        UserTicketList = request.get_json()['UserTicketList']
        QRsList = []
        for UserTicketItem in UserTicketList:
            UpdateUserTicket = Users_Tickets.query.filter_by(ID=UserTicketItem).first()
            TicketTypeItem = Ticket_type.query.filter_by(id=UpdateUserTicket.TicketTypeId).first()
            QR = pyqrcode.create("http://127.0.0.1:5000/CheckQR/" + str(UserTicketItem))
            QREncoded = QR.png_as_base64_str(8)
            try:
                UpdateUserTicket.IsActive = True
                UpdateUserTicket.QR = QREncoded
                db.session.commit()
                QRsList.append({"QR":QREncoded,"TicketType":TicketTypeItem.type})
            except:
                db.session.rollback()
        ReturnObj.QRsList = QRsList
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='FinshBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='FinshBookTicket', Email=EmailLog, CreatedAt=CurrentDateTime, Channel=ReqChannel,
                                 Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())

@application.route('/GetUserProfileInfos', methods=['POST'])
@cross_origin()
def GetUserProfileInfos():
    ReturnObj = GetUserProfileInfosResponse()
    RaisedError = False
    ErrorCode = 0
    EmailLog = ''
    CurrentDateTime = datetime.now()
    ReqChannel = 0
    try:
        try:
            EmailLog = request.get_json()['Email']
        except:
            EmailLog = ''
        try:
            ReqChannel = request.get_json()['Channel']
        except:
            ReqChannel = 0
        NewReqLog = Services_Log(Service_Name='GetUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=1,
                                 Json_Req=str(request.get_json()), Json_Res='')
        db.session.add(NewReqLog)
        db.session.commit()
        Email = request.get_json()['Email']
        Token = request.get_json()['Token']
        TokenObj = MainTokens.get(Token)
        if TokenObj == None:
            RaisedError = True
            ErrorCode = 1
            raise Exception('You are not Authorized')
        if TokenObj.Email != Email:
            RaisedError = True
            ErrorCode = 2
            raise Exception('You are not Authorized')
        FoundUsers = User.query.filter_by(Email=Email).all()
        FoundUsersCount = 0
        for item in FoundUsers:
            FoundUsersCount = FoundUsersCount + 1
        if FoundUsersCount == 0:
            RaisedError = True
            ErrorCode = 3
            raise Exception('There is no account for this email')
        RoleID = TokenObj.Role
        UserProfile = {}
        if RoleID == 5:
            FoundGuest = Guest.query.filter_by(user_id=FoundUsers[0].UserId).first()
            UserProfile = {"UserId": FoundUsers[0].UserId,"Email": FoundUsers[0].Email,"CreatedAt": FoundUsers[0].CreatedAt,
                           "FirstName": FoundGuest.first_name,"LastName": FoundGuest.last_name,"Mobile": FoundGuest.mobile,
                           "DateOfBirth": FoundGuest.date_of_birth, "RoleID":RoleID}
        if RoleID == 4:
            UserProfile = {}
        if RoleID == 3:
            UserProfile = {}
        if RoleID == 2:
            UserProfile = {}
        if RoleID == 1:
            FoundAdmin = Admin.query.filter_by(user_id=FoundUsers[0].UserId).first()
            UserProfile = {"UserId": FoundUsers[0].UserId,"Email": FoundUsers[0].Email,"CreatedAt": FoundUsers[0].CreatedAt,
                           "FirstName": FoundAdmin.first_name,"LastName": FoundAdmin.last_name, "RoleID":RoleID}

        ReturnObj.UserProfile = UserProfile
        ReturnObj.MethodStatus = True
    except Exception as ex:
        ReturnObj.MethodStatus = False
        ReturnObj.ErrorMessage = ex.args[0]
        ReturnObj.EndErrorMessge = 'Dear the service is not available'
        if RaisedError:
            ReturnObj.EndErrorMessge = ex.args[0]
    finally:
        ReturnObj.ErrorCode = ErrorCode
        db.session.close()
    try:
        NewResLog = Services_Log(Service_Name='GetUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res=str(ReturnObj.Format()))
        db.session.add(NewResLog)
        db.session.commit()
    except:
        NewResLog = Services_Log(Service_Name='GetUserProfileInfos', Email=EmailLog, CreatedAt=CurrentDateTime,
                                 Channel=ReqChannel, Log_Type=2,
                                 Json_Req='', Json_Res='')
        db.session.add(NewResLog)
        db.session.commit()
    return jsonify(ReturnObj.Format())

if __name__ == '__main__':
    application.run()
