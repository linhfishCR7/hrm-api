class NotificationTemplate:
    class UserCreated:
        """ Send notification to admin that the new account has been created"""
        def TITLE(name):  
            return f"New account {name} has been created"
        
        BODY = "New account has been created"
        
        
    class UserCreateDayOffYear:
        """ Send notification to hrm that the user has been created day off year"""
        def TITLE(name):  
            return f"The user {name} has been created day off year"
        
        BODY = "The user has been created day off year"
    
    
    class HrmApprovedDayOffYear:
        """ Send notification to user that the hrm has been approved day off year"""
        TITLE = "The hrm has been approved day off year"
        BODY = "The hrm has been approved day off year"

    
    class HrmSendSalaryToAllUser:
        """ Send salary notification to all user but admin """
        def TITLE(month, year):  
            return f"The Hrm has been sent salary {month} in {year}"
        BODY = "The Hrm has been sent salary to you"
    
