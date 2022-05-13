from django.db import ProgrammingError


class AppConstants:

    VALID_FILE_EXTENSION = [
        # VIDEO
        '.mp4',
        '.avi',
        '.flv',
        '.mov',
        '.mpeg',
        '.3gp',
        '.wmv',
        # IMAGE
        '.jpeg',
        '.jpg',
        '.png',
    ]

    LANGUAGE = ['en']

    class Timezone:
        DEFAULT = 'UTC'

    class Expiration:
        FORGOT_PASSWORD_EXPIRED_IN_DAYS = 48  # 2 days

    class Role:
        # If update -> check Choices class below
        ADMIN = 1
        USER = 2

    class Upload:
        MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
        FILE_TYPES = ['.png', '.jpg', '.jpeg', '.xlsx']
        FILE_OPTIONS = {
            'document': 'documents',
            'video': 'videos',
            'image': 'images',
        }

    class ImageSize:
        MINI = ((50, 50), ('mini', 0))
        LOGO = ((200, 200), ('logo', 1))
        THUMBNAIL = ((300,), ('thumbnail', 2))
        MEDIUM = ((600,), ('medium', 3))
        LARGE = ((1024,), ('large', 4))

    class Weekday:
        # If update -> check Mapping class below
        SORTED_MAP = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }

        # Abbreviation
        ABBREVIATION = {
            'Monday': 'mon',
            'Tuesday': 'tue',
            'Wednesday': 'wed',
            'Thursday': 'thu',
            'Friday': 'fri',
            'Saturday': 'sat',
            'Sunday': 'sun'
        }

        CODE_TO_TITLE = [0, "Monday", "Tuesday", "Wednesday",
                         "Thursday", "Friday", "Saturday", "Sunday"]


class ConstantBase:
    def __get_list_attr_value__(self):
        members = [getattr(self, attr)
                   for attr in dir(self) if not attr.startswith("__")]
        return members


class AppChoices:
    ROLES_FOR_REGISTER = [
        (AppConstants.Role.ADMIN, 'Admin'),
        (AppConstants.Role.USER, 'User')
    ]

    ROLES_FOR_ADMIN_MANAGER_USER = [
        (AppConstants.Role.ADMIN, 'Admin'),
        (AppConstants.Role.USER, 'User')
    ]


class ViewConstants:
    class Action:
        LIST = 'List'
        CREATE = 'Create'
        UPDATE = 'Update'
        RETRIEVE = 'Retrieve'
        DELETE = 'Delete'


class ExceptionConstants:
    CAN_NOT_GET_SERIALIZER_CLASS = 'CannotGetSerializerClass'


class Permissions:

    STAFF_PERMISSION = {
        "Dashboard": (
            ('dashboard', 'Dashboard'),
        ),
        "Admin Staff": (
            ('admin_staff', 'Admin Staff'),
        ),
        "Role": (
            ('role', 'Role'),
        ),
        "User": (
            ('user', 'User'),
        ),
        "Video": (
            ('video', 'Video'),
        ),
        "Banner": (
            ('banner', 'Banner'),
        ),
        "Prize": (
            ('prize', 'Prize'),
        ),
        "Winner": (
            ('winner', 'Winner'),
        ),
        "Transaction": (
            ('transaction', 'Transaction'),
        ),
    }


class ResponseMessage:
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class UserStatus:

    ACTIVE = "Active"
    BLOCKED = "Blocked"


class ProjectStatus:
    PENDING_PROJECT = 1
    RUNNING_PROJECT = 2
    FINISH_PROJECT = 3


class NotificationType:
    """Type notification"""
    NEW_USER = 1
    BLOCK_USER = 2
    UNBLOCK_USER = 3
    USER_CREATED_DAY_OF_YEAR = 4
    HRM_APPROVED_DAY_OF_YEAR = 5
    HRM_SEND_SALARY_TO_ALL_USER = 6
    HRM_SEND_STAFF_DELETED = 7
    HRM_REFUSED_DAY_OF_YEAR = 8


class NotificationMetadata:
    default_data = dict(
        business_id=None
    )


class AddressType:
    """Type Address"""
    PLACE_OF_BIRTH_ADDRESS = "place_of_birth_address"
    DOMICILE = "domicile"
    TEMPORARY_RESIDENCE_ADDRESS = "temporary_residence_address"
    PERMANENT_ADDRESS = "permanent_address"
    HEAD_OFFICE_ADDRESS = "head_office_address"
    WORKING_OFFICE_ADDRESS = "working_office_address"
    CUSTOMER_ADDRESS = "customer_address"


class GenderStatus:
    """Gender"""
    MALE = "male",
    FEMALE = "female"
    UNKNOWN = "unknown"


class MaritalStatus:
    """Marital"""
    GOT_MARRIED = "got_married",
    SINGLE = "single"


class CodeConstants:

    class StaffRandomConstant:
        MIN = 100000
        MAX = 999999


class SkillTypes:
    """SkillTypes"""
    PROGRAMMING = "Lập trình",
    OFFICE = "Văn phòng"
    DESIGN = "Thiết kế"


class RelationshipType:
    """RelationshipType"""
    FATHER = "Ba",
    MOTHER = "Mẹ"
    HUSBAND = "Chồng"
    WIFE = "Vợ"


class SalaryContant:
    """Salary"""
    STANDARD_TIME = 160
    ALLOWANCE = 0.105
    M5 = 5000000
    M10 = 10000000
    M18 = 18000000
    M32 = 32000000
    M52 = 52000000
    M80 = 80000000
    M0_M5 = 0.05
    UP_M5_M10 = 0.10
    UP_M10_M18 = 0.15
    UP_M18_M32 = 0.20
    UP_M32_M52 = 0.25
    UP_M52_M80 = 0.30
    UP_M80 = 0.35
    BASIC_COEFFICIENT = 1.2


class TypeTimeKeeping:
    ADMININISTRATION = 1
    OVERTIME = 1.5
    DAY_OFF = 2.0
    HOLIDAY_VACATION = 3.0


class Data:
    address = [
        {
            "address": "",
            "city": "",
            "province": "",
            "district": "",
            "commune": "",
            "country": "",
            "postcode": "",
            "lat": 0,
            "lng": 0,
            "type": "place_of_birth_address"
        },
        {
            "address": "",
            "city": "",
            "province": "",
            "district": "",
            "commune": "",
            "country": "",
            "postcode": "",
            "lat": 0,
            "lng": 0,
            "type": "permanent_address"
        },
        {
            "address": "",
            "city": "",
            "province": "",
            "district": "",
            "commune": "",
            "country": "",
            "postcode": "",
            "lat": 0,
            "lng": 0,
            "type": "temporary_residence_address"
        }]
