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
    
