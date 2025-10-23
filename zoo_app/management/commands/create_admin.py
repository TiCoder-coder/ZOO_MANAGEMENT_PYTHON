#------------------------------------------------------------- HAM DUNG DE TAO RA TAI KHOAN ADMIN (QUAN LI) ----------------------------------------------------------------------------------------------------

from django.core.management.base import BaseCommand                                             # Khai bao lop co so de goi lenh quan li -- su dung handle(). stdput()
from django.contrib.auth.hashers import make_password
from zoo_app.models.managersModel import ManagerModel
from zoo_app.services.managersService import _apply_peper, ManagerService
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent                                 # Khai bao duong dan chinh cua thu muc
load_dotenv(os.path.join(BASE_DIR, ".env"))                                                     # Tao duong dan day du den thu muc .env

class Command(BaseCommand):

    # Ham dung de tao ra admin tu userName, password
    def handle(self, *args, **options):
        username = os.getenv("USER_NAME_ADMIN")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL", "admin@zoo.com")

        # Kiem tra co dung username va password khong --- Neu khong dung -> False
        if not username or not password:
            self.stdout.write(self.style.ERROR("LACK USER_NAME_ADMIN OR ADMIN_PASSWORD IN .env"))
            return

        # Kiem tra password co manh khong
        if not ManagerService.check_password_strength(password):
            self.stdout.write(self.style.ERROR("Error, weak password (len >6, has lower/upper/digit/special)"))
            return

        # Kiem tra co userName nao trung ten khong --- Neu co -> False
        if ManagerModel.objects.filter(userName=username).exists():
            self.stdout.write(self.style.WARNING(f"Admin '{username}' was existed"))
            return

        # Neu dung thong tin thi hash password truoc khi tao
        hashed_password = make_password(_apply_peper(password))

        ManagerModel.objects.create(
            userName=username,
            password=hashed_password,
            email=email,
            name="Administrator",
            role="manager",  # Match enum value
            is_active=True,
            failed_attempts=0,
            lock_until=None
        )
        self.stdout.write(self.style.SUCCESS(f"Admin '{username}' create successfully!"))