import jwt
from datetime import datetime, timezone, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework.exceptions import ValidationError, PermissionDenied
from decouple import config
from zoo_app.repositories.managerRepository import ManagerRepository
from bson import ObjectId
from zoo_app.middleware.auth import require_manager, require_manager_or_admin

# Dinh nghia mot ham dung de convert cac object -> str
def convert_objectid(obj):
    # Neu la list: duyet qua cac phan tu torng list va chuyen doi object -> str
    if isinstance(obj, list):
        return [convert_objectid(o) for o in obj]
    
    # Neu la dict: duyet qua cac phan tu va xu li cho tung key, value
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                new_obj[k] = str(v)
            else:
                new_obj[k] = convert_objectid(v)
        return new_obj
    return obj


# SECURITY CONFIG
MAX_FAILED_ATTEMPTS = int(config("MAX_FAILED_ATTEMPS", default=5))
PASSWORD_PEPPER = config("PASSWORD_PEPPER", default=None)
RESET_TOKEN_SALT = config("RESET_TOKEN_SALT", default="reset_secret")
RESET_TOKEN_EXPIRY_SECONDS = int(config("RESET_TOKEN_EXPIRY_SECONDS", default=3600))
signer = TimestampSigner(config("SECRET_KEY"))

def _apply_pepper(raw_password: str) -> str:
    return raw_password + PASSWORD_PEPPER if PASSWORD_PEPPER else raw_password


# --------------------------------------------- CLASS KHONG TRUC TIEP TUONG TAC VOI DATABASE MA SE THONG QUA REPOSITORY DE TUONG TAC ----------------------------------------------------------------------- 
# ------------------------------------------------------------------VA PHAN QUYEN SU DUNG CHO STAFF HAY MANAGER VA ADMIN------------------------------------------------------------------------------------    

class ManagerService:

    # DINH NGHIA MOT HAM DUNG DE KIEM TRA XEM PASSWORD TAO RA CO MANH KHONG---------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check_password_strength(password: str) -> bool:
        if len(password) <= 6:
            return False
        has_lower = any(c.islower() for c in password)                                       # Phai co ki tu thuong
        has_upper = any(c.isupper() for c in password)                                       # Phai co ki tu in hoa
        has_digit = any(c.isdigit() for c in password)                                       # Phai co so
        has_special = any(c in "!@#$%^&*()-_+=" for c in password)                           # Phai co ki tu dac biet
        return has_lower and has_upper and has_digit and has_special


    # DINH NGHI MOT HAM DUNG DE KIEM TRA SO LAN DANG NHAP THAT BAI --- NEU LON HON SO LAN CHO PHEP THI ---> KHOA TAI KHOAN TRONG 1 KHOANG THOI GIAN --------------------------------------------------------
    @staticmethod
    def _increase_failed_attempt(manager):
        
        # Sau moi lan loi thi cong them 1
        failed = manager.get("failed_attempts", 0) + 1
        
        # Chua lock neu chua vuot qua so lan quy dinh
        lock_until = None
        
        # Lock
        if failed >= MAX_FAILED_ATTEMPTS:
            lock_until = datetime.now(timezone.utc) + timedelta(minutes=5)                  # Thoi gian locj la thoi gian hien tai + 5 phut
        
        # Cap nhap xupng database manager bi loi bao nhieu lan va lock den khi nao
        ManagerRepository.update_by_id(manager["_id"], {
            "failed_attempts": failed,
            "lock_until": lock_until
        })

    # MA HOA TOKEN TRUOC KHI DUA RA ---- TOKEN NAY SE DUOC NOI VOI MOT CHUOI KHAC --- NEU DE CHO NGUOI KHAC CO TOKEN THI CUNG KHONG THE TRUY CAP VI KHONG CO CHUOI SALT
    @staticmethod
    def generate_token(identifier: str) -> str:
        
        # Tim kiem thong tin manager
        manager = ManagerRepository.find_by_username_or_email(identifier)
        if not manager:
            raise ValidationError("Manager not found for token generation")
        
        # Neu tim thay manager thi se dua thong tin do vao token
        payload = f"manager:{manager['_id']}"
        signed = signer.sign(payload + "|" + RESET_TOKEN_SALT)
        return signed
    
    # HAM DUNG DE RESET PASSWORD KHI CAN--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def reset_password_with_token(token: str, new_password: str):
        
        # Giai ma token
        try:
            
            # Giai ma token va kiem tra xem token con han su dung hay khong
            signed_value = signer.unsign(token, max_age=RESET_TOKEN_EXPIRY_SECONDS)
        except (SignatureExpired, BadSignature):
            raise ValidationError("Token invalid or expired")

        # Tach paylooad va chuoi salt ra dung de kiem tra xem co dung thong tin khong
        payload, salt = signed_value.split("|", 1)
        
        # Neu khac chuoi salt da duoc dinh nghia trong .env thi bao loi
        if salt != RESET_TOKEN_SALT:
            raise ValidationError("Invalid token salt")

        # Kiem tra id nguoi dung
        manager_id = payload.split(":")[1]
        
        # Kiem tra xem id do co phai la cua manager hay khong
        manager = ManagerRepository.find_by_id(manager_id)
        if not manager:
            raise ValidationError("Manager not found")

        # Neu dung thi kiem tra xem mat khau muon dat lai co dung chuan hay khong
        if not ManagerService.check_password_strength(new_password):
            raise ValidationError("Weak new password")

        # Neu ok thi lay password moi dem di hash va cap nhap
        hashed_pw = make_password(_apply_pepper(new_password))
        ManagerRepository.update_by_id(manager_id, {
            "password": hashed_pw,
            "failed_attempts": 0,
            "lock_until": None,
            "updatedAt": datetime.now(timezone.utc)
        })
        return {"Reset": True}

    # CREATE MANAGER -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_manager(user, name, userName, password, email, role="staff"):
        require_manager_or_admin(user)

        if ManagerRepository.find_by_username(userName):
            raise ValidationError("Username already exists")
        if ManagerRepository.find_by_username_or_email(email):
            raise ValidationError("Email already exists")
        if not ManagerService.check_password_strength(password):
            raise ValidationError("Weak password")

        hashed_pw = make_password(_apply_pepper(password))
        normalized_role = str(role).capitalize() if role.lower() in ["manager", "staff", "admin"] else role

        data = {
            "name": name,
            "userName": userName,
            "password": hashed_pw,
            "email": email,
            "role": normalized_role,
            "is_active": True,
            "failed_attempts": 0,
            "lock_until": None,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        }
        ManagerRepository.insert_one(data)
        return {"Created": True}

    
    # REVIEW ALL MANAGER --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_all_managers(user):
        require_manager_or_admin(user)

        managers = ManagerRepository.find_all()
        for m in managers:
            m["_id"] = str(m["_id"])
            m.pop("password", None)
        return managers

    
    # REVIEW MANAGER BY ID ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def review_manager_by_id(user, idManager):
        require_manager_or_admin(user)

        manager = ManagerRepository.find_by_id(idManager)
        if not manager:
            raise ValidationError(f"No manager found with id: {idManager}")
        manager["_id"] = str(manager["_id"])
        manager.pop("password", None)
        return manager


    # UPDATE MANAGER ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def update_manager(user, idManager, validated_data):
        require_manager_or_admin(user)

        update_fields = {
            key: value for key, value in validated_data.items()
            if key in ["name", "email", "role", "is_active"]
        }
        update_fields["updatedAt"] = datetime.now(timezone.utc)
        result = ManagerRepository.update_by_id(idManager, update_fields)
        if result.matched_count == 0:
            raise ValidationError(f"No manager found with id: {idManager}")
        return {"Updated": True}


    # DELETE MANAGER -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def delete_manager(user, idManager):
        require_manager_or_admin(user)

        result = ManagerRepository.delete_by_id(idManager)
        if result.deleted_count == 0:
            raise ValidationError(f"No manager found with id: {idManager}")
        return {"Deleted": True}

    # AUTHENTICATE: DUNG DE KIEM TRA DANH NHAP ----------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def authenticate(userName: str, password: str):
        
        # Kiem tra manager co ton tai khong
        manager = ManagerRepository.find_by_username(userName)
        if not manager:
            raise ValidationError("Username does not exist")

        # Kiem tra tai khoan manager do co bi khoa tai khoan khong
        if manager.get("lock_until") and manager["lock_until"] > datetime.now(timezone.utc):
            raise PermissionDenied(f"Account locked until {manager['lock_until']}")

        
        # Kiem tra xem co dung password khong
        if not check_password(_apply_pepper(password), manager["password"]):        # Vi password da duoc hash nen phai ket hop voi _apply_peper moi kiem tra duoc
            ManagerService._increase_failed_attempt(manager)
            raise PermissionDenied("Invalid username or password")
        
        # Neu dang nhap thanh cong thi cap nhap lai cac thong tin
        ManagerRepository.update_by_id(manager["_id"], {
            "failed_attempts": 0,                                                   # Cap nhap lai so lan that bai la o
            "last_login": datetime.now(timezone.utc),                               # Cap nhap lai lan dang nhap cuoi cung
            "lock_until": None,                                                     # Cap nhap lai khong lock
            "updatedAt": datetime.now(timezone.utc)                                 # Cap nhap lai ngay update
        })

        # Chuyen doi id sang string va tra ve thong tin
        manager["_id"] = str(manager["_id"])
        
        manager.pop("password", None)                                               # Xoa di mat khau truoc khi in ra de bao mat
        return manager
