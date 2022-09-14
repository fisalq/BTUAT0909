class LoginResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.Token = ""
        self.RoleId = 0
        self.ErrorCode = 0
        self.Email = ""

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'Token': self.Token,
            'RoleId': self.RoleId,
            'ErrorCode': self.ErrorCode,
            'Email': self.Email
        }

class SendEmailForForgetPasswordResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.Token = ""
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'Token': self.Token,
            'ErrorCode': self.ErrorCode
        }

class VerifyForgetPasswordResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsVerified = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsVerified': self.IsVerified,
            'ErrorCode': self.ErrorCode
        }

class ChangeForgetPasswordResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.PasswordChanged = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'PasswordChanged': self.PasswordChanged,
            'ErrorCode': self.ErrorCode
        }

class GetCountriesResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.CountriesList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'CountriesList': self.CountriesList,
            'ErrorCode': self.ErrorCode
        }

class GetRegionsResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.RegionsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'RegionsList': self.RegionsList,
            'ErrorCode': self.ErrorCode
        }

class GetCitiesResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.CitiesList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'CitiesList': self.CitiesList,
            'ErrorCode': self.ErrorCode
        }

class SendEmailForRegistrResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.Token = ""
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'Token': self.Token,
            'ErrorCode': self.ErrorCode
        }

class ReSendEmailForRegistrResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'ErrorCode': self.ErrorCode
        }

class VerifyRegistrResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsVerified = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsVerified': self.IsVerified,
            'ErrorCode': self.ErrorCode
        }

class RegistrNewUserResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsUserRegistred = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsUserRegistred': self.IsUserRegistred,
            'ErrorCode': self.ErrorCode
        }

class ChangePersonalInfoResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsInfoChanged = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsInfoChanged': self.IsInfoChanged,
            'ErrorCode': self.ErrorCode
        }

class CreateNewEventResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsEventCreated = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsEventCreated': self.IsEventCreated,
            'ErrorCode': self.ErrorCode
        }

class GetCategoriesForMainResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.CategoriesList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'CategoriesList': self.CategoriesList,
            'ErrorCode': self.ErrorCode
        }

class GetEventsByCategoryForMainResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.EventsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'EventsList': self.EventsList,
            'ErrorCode': self.ErrorCode
        }

class GetEventDetailsResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.EventDetails = {}
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'EventDetails': self.EventDetails,
            'ErrorCode': self.ErrorCode
        }

class GetMoreLikeThisEventsForEventsResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.EventsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'EventsList': self.EventsList,
            'ErrorCode': self.ErrorCode
        }

class GetPlacesAroundYouResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.CitiesList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'CitiesList': self.CitiesList,
            'ErrorCode': self.ErrorCode
        }

class GetSlidersForMainResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.SlidersList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'SlidersList': self.SlidersList,
            'ErrorCode': self.ErrorCode
        }

class GetMenuResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.MenuList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'MenuList': self.MenuList,
            'ErrorCode': self.ErrorCode
        }

class GetTicketsForEventResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.TicketsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'TicketsList': self.TicketsList,
            'ErrorCode': self.ErrorCode
        }

class GetUpcomingAndPastEventsForUserResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.UpcomingEventsList = []
        self.PastEventsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'UpcomingEventsList': self.UpcomingEventsList,
            'PastEventsList': self.PastEventsList,
            'ErrorCode': self.ErrorCode
        }

class GetFilteredEventsWithPaginationResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.EventsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'EventsList': self.EventsList,
            'ErrorCode': self.ErrorCode
        }

class GetGuestUserProfileInfosResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.GuestProfile = {}
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'GuestProfile': self.GuestProfile,
            'ErrorCode': self.ErrorCode
        }

class LogoutResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.IsLogout = False
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'IsLogout': self.IsLogout,
            'ErrorCode': self.ErrorCode
        }

class StartBookTicketResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.UserTicketList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'UserTicketList': self.UserTicketList,
            'ErrorCode': self.ErrorCode
        }

class FinshBookTicketResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.QRsList = []
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'QRsList': self.QRsList,
            'ErrorCode': self.ErrorCode
        }

class GetUserProfileInfosResponse():
    def __init__(self):
        self.MethodStatus = False
        self.ErrorMessage = ""
        self.EndErrorMessge = ""
        self.UserProfile = {}
        self.ErrorCode = 0

    def Format(self):
        return {
            'MethodStatus': self.MethodStatus,
            'ErrorMessage': self.ErrorMessage,
            'EndErrorMessge': self.EndErrorMessge,
            'UserProfile': self.UserProfile,
            'ErrorCode': self.ErrorCode
        }