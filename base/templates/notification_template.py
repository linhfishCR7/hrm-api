class NotificationTemplate:
    class UserCreated:
        """ Send notification to admin that the new account has been created"""
        def TITLE(name):  
            return f"New account {name} has been created"
        
        BODY = "New account has been created"
    
