from datetime import datetime

class ForgetPasswordToken:
    def __init__(self):
        self.Token = ""
        self.CreatedDateTime = datetime.now()
        self.LatestDateTime = datetime.now()
        self.Email = ""
        self.ValidationCode = "0000"
        self.IsCodeValidate = False

    def Format(self):
        return {
            'Token': self.Token,
            'CreatedDateTime': self.CreatedDateTime,
            'LatestDateTime': self.LatestDateTime,
            'Email': self.Email,
            'ValidationCode': self.ValidationCode,
            'IsCodeValidate': self.IsCodeValidate
        }

    def CreateTokenStr(self):
        DateTimeYear = str(self.CreatedDateTime.year)

        DateTimeMonth = ''
        if int(self.CreatedDateTime.month) < 10:
            DateTimeMonth = '0' + str(self.CreatedDateTime.month)
        else:
            DateTimeMonth = str(self.CreatedDateTime.month)

        DateTimeDay = ''
        if int(self.CreatedDateTime.day) < 10:
            DateTimeDay = '0' + str(self.CreatedDateTime.day)
        else:
            DateTimeDay = str(self.CreatedDateTime.day)

        DateTimeHour = ''
        if int(self.CreatedDateTime.hour) < 10:
            DateTimeHour = '0' + str(self.CreatedDateTime.hour)
        else:
            DateTimeHour = str(self.CreatedDateTime.hour)

        DateTimeMinute = ''
        if int(self.CreatedDateTime.minute) < 10:
            DateTimeMinute = '0' + str(self.CreatedDateTime.minute)
        else:
            DateTimeMinute = str(self.CreatedDateTime.minute)

        DateTimeSecond = ''
        if int(self.CreatedDateTime.second) < 10:
            DateTimeSecond = '0' + str(self.CreatedDateTime.second)
        else:
            DateTimeSecond = str(self.CreatedDateTime.second)

        SplitedEmail = self.Email.split("@")
        EmailWantedPart = SplitedEmail[0]
        if len(EmailWantedPart) < 4:
            EmailWantedPart = EmailWantedPart + 'FFA'
        Part1 = EmailWantedPart[:2]
        Part2 = EmailWantedPart[2:4]
        Part3 = EmailWantedPart[-4:-2]
        Part4 = EmailWantedPart[-2:]


        return DateTimeSecond+Part1+DateTimeMinute+Part2+DateTimeHour+'FFA'+DateTimeDay+Part3+DateTimeMonth+Part4+DateTimeYear

class RegistrToken:
    def __init__(self):
        self.Token = ""
        self.CreatedDateTime = datetime.now()
        self.LatestDateTime = datetime.now()
        self.Email = ""
        self.ValidationCode = "0000"
        self.IsCodeValidate = False

    def Format(self):
        return {
            'Token': self.Token,
            'CreatedDateTime': self.CreatedDateTime,
            'LatestDateTime': self.LatestDateTime,
            'Email': self.Email,
            'ValidationCode': self.ValidationCode,
            'IsCodeValidate': self.IsCodeValidate
        }

    def CreateTokenStr(self):
        DateTimeYear = str(self.CreatedDateTime.year)

        DateTimeMonth = ''
        if int(self.CreatedDateTime.month) < 10:
            DateTimeMonth = '0' + str(self.CreatedDateTime.month)
        else:
            DateTimeMonth = str(self.CreatedDateTime.month)

        DateTimeDay = ''
        if int(self.CreatedDateTime.day) < 10:
            DateTimeDay = '0' + str(self.CreatedDateTime.day)
        else:
            DateTimeDay = str(self.CreatedDateTime.day)

        DateTimeHour = ''
        if int(self.CreatedDateTime.hour) < 10:
            DateTimeHour = '0' + str(self.CreatedDateTime.hour)
        else:
            DateTimeHour = str(self.CreatedDateTime.hour)

        DateTimeMinute = ''
        if int(self.CreatedDateTime.minute) < 10:
            DateTimeMinute = '0' + str(self.CreatedDateTime.minute)
        else:
            DateTimeMinute = str(self.CreatedDateTime.minute)

        DateTimeSecond = ''
        if int(self.CreatedDateTime.second) < 10:
            DateTimeSecond = '0' + str(self.CreatedDateTime.second)
        else:
            DateTimeSecond = str(self.CreatedDateTime.second)

        SplitedEmail = self.Email.split("@")
        EmailWantedPart = SplitedEmail[0]
        if len(EmailWantedPart) < 4:
            EmailWantedPart = EmailWantedPart + 'FFA'
        Part1 = EmailWantedPart[:2]
        Part2 = EmailWantedPart[2:4]
        Part3 = EmailWantedPart[-4:-2]
        Part4 = EmailWantedPart[-2:]

        return DateTimeSecond+Part1+DateTimeMinute+Part2+DateTimeHour+'FFA'+DateTimeDay+Part3+DateTimeMonth+Part4+DateTimeYear

class MainToken:
    def __init__(self):
        self.Token = ""
        self.CreatedDateTime = datetime.now()
        self.LatestDateTime = datetime.now()
        self.Email = ""
        self.Role = 0

    def Format(self):
        return {
            'Token': self.Token,
            'CreatedDateTime': self.CreatedDateTime,
            'LatestDateTime': self.LatestDateTime,
            'Email': self.Email,
            'Role': self.Role
        }

    def CreateTokenStr(self):
        DateTimeYear = str(self.CreatedDateTime.year)

        DateTimeMonth = ''
        if int(self.CreatedDateTime.month) < 10:
            DateTimeMonth = '0' + str(self.CreatedDateTime.month)
        else:
            DateTimeMonth = str(self.CreatedDateTime.month)

        DateTimeDay = ''
        if int(self.CreatedDateTime.day) < 10:
            DateTimeDay = '0' + str(self.CreatedDateTime.day)
        else:
            DateTimeDay = str(self.CreatedDateTime.day)

        DateTimeHour = ''
        if int(self.CreatedDateTime.hour) < 10:
            DateTimeHour = '0' + str(self.CreatedDateTime.hour)
        else:
            DateTimeHour = str(self.CreatedDateTime.hour)

        DateTimeMinute = ''
        if int(self.CreatedDateTime.minute) < 10:
            DateTimeMinute = '0' + str(self.CreatedDateTime.minute)
        else:
            DateTimeMinute = str(self.CreatedDateTime.minute)

        DateTimeSecond = ''
        if int(self.CreatedDateTime.second) < 10:
            DateTimeSecond = '0' + str(self.CreatedDateTime.second)
        else:
            DateTimeSecond = str(self.CreatedDateTime.second)

        SplitedEmail = self.Email.split("@")
        EmailWantedPart = SplitedEmail[0]
        if len(EmailWantedPart) < 4:
            EmailWantedPart = EmailWantedPart + 'FFA'
        Part1 = EmailWantedPart[:2]
        Part2 = EmailWantedPart[2:4]
        Part3 = EmailWantedPart[-4:-2]
        Part4 = EmailWantedPart[-2:]

        return DateTimeSecond+Part1+DateTimeMinute+Part2+DateTimeHour+'FFA'+DateTimeDay+Part3+DateTimeMonth+Part4+DateTimeYear