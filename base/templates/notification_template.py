class NotificationTemplate:
    class UserCreated:
        """ Send notification to admin that the new account has been created"""
        def TITLE(name):  
            return f"Tài khoản {name} mới vưa được tạo"
        
        BODY = "Tài khoản mới được tạo"
        
        
    class UserCreateDayOffYear:
        """ Send notification to hrm that the user has been created day off year"""
        def TITLE(name):  
            return f"Nhân viên {name} gửi đơn báo nghỉ phép"
        
        BODY = "Nhân viên gửi đơn báo nghỉ phép"
    
    
    class HrmApprovedDayOffYear:
        """ Send notification to user that the hrm has been approved day off year"""
        TITLE = "Công ty đã chấp nhận đơn báo nghỉ phép của bạn"
        BODY = "Công ty đã chấp nhận đơn báo nghỉ phép của bạn"


    class HrmRefusedDayOffYear:
        """ Send notification to user that the hrm has been refused day off year"""
        TITLE = "Công ty đã từ chối đơn báo nghỉ phép của bạn"
        BODY = "Công ty đã từ chối đơn báo nghỉ phép của bạn"
    
    class HrmSendSalaryToAllUser:
        """ Send salary notification to all user but admin """
        def TITLE(month, year):  
            return f"Công ty đã gửi phiếu báo lương tháng {month} năm {year}"
        BODY = "Công ty đã gửi phiếu báolương đến nhân viên"

    
    class ProfileDelete:
        """ Send notification to admin that the new account has been delete"""
        def TITLE(name):  
            return f"Nhân viên {name} đã bị xoá"
        
        def BODY(email):
            return f"{email} - Vui lòng khoá tài khoản này hoặc xoá tài khoản"
    
