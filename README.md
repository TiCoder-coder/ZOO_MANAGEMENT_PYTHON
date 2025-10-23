## ZOO MANAGEMENT
https://www.google.com/url?sa=i&url=https%3A%2F%2Fduhocduytan.vn%2Ftu-van-du-hoc%2Fdu-hoc-my-nganh-sinh-hoc-va-quan-ly-vuon-thu-biology-and-management-of-zoo-animals-portland-community-collge.html&psig=AOvVaw1zqjt8dZ0_2mbtlJR7a_gq&ust=1761301039903000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCODG2eiLupADFQAAAAAdAAAAABAL

ZOO_MANAGEMENT – Hệ thống quản lý vườn thú thông minh được xây dựng bằng Python + Django, tích hợp MongoDB, chuẩn MVC + Repository Pattern, bảo mật bằng JWT, và tài liệu API trực quan qua Swagger.
Dự án cho phép quản lý toàn diện:

Động vật (loài, tuổi, sức khỏe, chuồng ở)
Chuồng trại (diện tích, khí hậu, sức chứa)
Thực phẩm & lịch cho ăn (loại, calo, định lượng, thời gian)
Người quản lý (phân quyền Admin/Staff, khóa tài khoản tự động khi đăng nhập sai nhiều lần)

- Tất cả được tách biệt rõ ràng theo tầng: Model → Repository → Service → View → Middleware
- Đảm bảo dễ bảo trì, mở rộng, test và bảo mật cao.
- API RESTful đầy đủ, có Swagger UI để test ngay trên trình duyệt.
- Hỗ trợ đăng nhập JWT, phân quyền theo role, tracking hoạt động, tự động khóa tài khoản.
---------------------------------------------------------------------------------------------------------------------------------------------------------
## 📂 Cấu trúc dự án
## <!-- 
    ├── 📁 API_TEST                                             # Dữ liệu mẫu (txt) để test API
    │   ├── 📄 animals.txt  
    │   ├── 📄 enclosures.txt
    │   ├── 📄 feedRecords.txt
    │   ├── 📄 foods.txt
    │   ├── 📄 login.txt
    │   └── 📄 managers.txt
    ├── 📁 ZOO_MANAGEMENT                                       # Django project config
    │   ├── 🐍 __init__.py
    │   ├── 🐍 asgi.py
    │   ├── 🐍 settings.py
    │   ├── 🐍 urls.py
    │   └── 🐍 wsgi.py
    ├── 📁 zoo_app                                              # Gender, HealthStatus, Climate, TypeFood, Role
    │   ├── 📁 enums
    │   │   ├── 🐍 __init__.py
    │   │   └── 🐍 enums.py
    │   ├── 📁 management                                       # create_admin command
    │   │   ├── 📁 commands
    │   │   │   ├── 🐍 __init__.py
    │   │   │   └── 🐍 create_admin.py
    │   │   └── 🐍 __init__.py
    │   ├── 📁 middleware                                       # JWT, Auth, Rate limiting
    │   │   ├── 🐍 __init__.py
    │   │   ├── 🐍 auth.py
    │   │   ├── 🐍 authentication.py
    │   │   └── 🐍 jwt_handler.py
    │   ├── 📁 migrations
    │   │   ├── 🐍 0001_initial.py
    │   │   └── 🐍 __init__.py
    │   ├── 📁 models                                           # Định nghĩa schema (MongoDB-compatible)
    │   │   ├── 🐍 __init__.py
    │   │   ├── 🐍 animalsModels.py
    │   │   ├── 🐍 enclosuresModel.py
    │   │   ├── 🐍 feedRecordsModel.py
    │   │   ├── 🐍 foodsModel.py
    │   │   └── 🐍 managersModel.py
    │   ├── 📁 repositories                                     # CRUD trực tiếp với DB
    │   │   ├── 🐍 __init__.py
    │   │   ├── 🐍 animalRepository.py
    │   │   ├── 🐍 enclosureRepository.py
    │   │   ├── 🐍 feedRecordRepository.py
    │   │   ├── 🐍 foodRepository.py
    │   │   └── 🐍 managerRepository.py
    │   ├── 📁 serializers                                      # Base, Create, Update serializers (kế thừa)
    │   │   ├── 📁 animalsSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   ├── 🐍 baseSerializerAnimal.py
    │   │   │   ├── 🐍 createAnimals.py
    │   │   │   └── 🐍 updateAnimals.py
    │   │   ├── 📁 enclosureSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   ├── 🐍 baseSerializerEnclosure.py
    │   │   │   ├── 🐍 createEnclosures.py
    │   │   │   └── 🐍 updateEnclosures.py
    │   │   ├── 📁 feedRecordsSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   ├── 🐍 baseSerializerFeedRecord.py
    │   │   │   ├── 🐍 createFeedRecords.py
    │   │   │   └── 🐍 updateFeedRecords.py
    │   │   ├── 📁 foodsSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   ├── 🐍 baseSerializerFoods.py
    │   │   │   ├── 🐍 createFoods.py
    │   │   │   └── 🐍 updateFoods.py
    │   │   ├── 📁 loginSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   └── 🐍 loginSerializer.py
    │   │   ├── 📁 managersSerializer
    │   │   │   ├── 🐍 __init__.py
    │   │   │   ├── 🐍 baseSerializerManagers.py
    │   │   │   ├── 🐍 createManagers.py
    │   │   │   └── 🐍 updateManagers.py
    │   │   └── 🐍 __init__.py
    │   ├── 📁 services                                          # Business logic + phân quyền
    │   │   ├── 🐍 __init__.py
    │   │   ├── 🐍 animalsService.py
    │   │   ├── 🐍 enclosuresService.py
    │   │   ├── 🐍 feedRecordsService.py
    │   │   ├── 🐍 foodsService.py
    │   │   └── 🐍 managersService.py
    │   ├── 📁 views                                            # API Views + Swagger annotations
    │   │   ├── 🐍 __init__.py
    │   │   ├── 🐍 animalsView.py
    │   │   ├── 🐍 authsView.py
    │   │   ├── 🐍 enclosuresView.py
    │   │   ├── 🐍 feedRecordsView.py
    │   │   ├── 🐍 foodsView.py
    │   │   └── 🐍 managersView.py
    │   ├── 🐍 __init__.py
    │   ├── 🐍 admin.py
    │   ├── 🐍 apps.py
    │   ├── 🐍 tests.py
    │   └── 🐍 urls.py                                          # API routers
    ├── ⚙️ .gitignore
    ├── 📝 README.md
    ├── 📄 db.sqlite3
    ├── 🐍 generateSecertKey.py
    └── 🐍 manage.py ## --> 

---------------------------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Tính năng
- Quản lý thông tin **động vật**: thêm, sửa, xóa, xem danh sách.
- Quản lý **chuồng nuôi** và **khả năng chứa** của từng chuồng.
- Quản lý **thức ăn** và **lịch sử cho ăn**.
- Quản lý **quản lý viên (manager)** với phân quyền và bảo mật.
- **Hệ thống đăng nhập an toàn** với JWT Token.
- **CRUD trực tiếp với MongoDB**.
- Tài liệu **Swagger API** để thử nghiệm dễ dàng.

---------------------------------------------------------------------------------------------------------------------------------------------------------

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.10.11
- **Framework:** Django 4.2
- **Cơ sở dữ liệu:** MongoDB 7.0
- **API Docs:** Swagger
- **Kiến trúc:** MVC (Model-View-Controller)

---------------------------------------------------------------------------------------------------------------------------------------------------------

## 🐾 Mô tả các Model

### 1️⃣ Animal
- `id`: Mã động vật (primary key)
- `name`: Tên động vật
- `age`: Tuổi
- `species`: Loài
- `gender`: Giới tính (enum)
- `weight`: Cân nặng
- `healthStatus`: Tình trạng sức khỏe (enum)
- `enclosureId`: Mã chuồng nuôi
- `createAt`: Thời gian tạo
- `updateAt`: Thời gian cập nhật

### 2️⃣ Enclosure
- `idEnclosure`: Mã chuồng
- `nameEnclosure`: Tên chuồng
- `areaSize`: Diện tích
- `climate`: Khí hậu (enum)
- `capacity`: Sức chứa tối đa

### 3️⃣ FeedRecord
- `idFeedRecord`: Mã bản ghi
- `animalIdFeedRecord`: ID động vật
- `foodId`: ID thức ăn
- `quantity`: Số lượng
- `feedAt`: Thời gian cho ăn

### 4️⃣ Food
- `idFood`: Mã thức ăn
- `nameFood`: Tên thức ăn
- `typeFood`: Loại thức ăn (enum)
- `caloriesPerUnit`: Calories trên đơn vị

### 5️⃣ Manager
- `id`: ID tự sinh
- `name`, `userName`, `password`, `email`
- `role`: Vai trò (enum)
- `is_active`: Trạng thái kích hoạt
- **Security & Tracking:**
  - `failed_attempts`: Số lần đăng nhập thất bại
  - `lock_until`: Thời gian khóa nếu đăng nhập sai nhiều lần
  - `last_login`: Lưu lần đăng nhập gần nhất
  - `createdAt`, `updatedAt`: Theo dõi thời gian tạo/cập nhật

---------------------------------------------------------------------------------------------------------------------------------------------------------

## ⚙️ Cơ chế hoạt động từng tầng

1. **Middleware**:  
   - Xử lý **authenticate**, kiểm tra JWT token, phân quyền truy cập.
   - Các hàm xác thực được gọi trước khi vào tầng Service.

2. **Models**:  
   - Định nghĩa cấu trúc dữ liệu, các trường và ràng buộc của từng bảng trong MongoDB.

3. **Serializers**:  
   - Chuyển đổi dữ liệu từ **Model → JSON** để trả về API.  
   - Có 3 loại chính: `Base` (lấy thông tin), `Create`, `Update`.

4. **Repositories**:  
   - Thực hiện **CRUD trực tiếp với MongoDB**.  
   - Không chứa logic phân quyền, chỉ xử lý dữ liệu.

5. **Services**:  
   - Gọi Repository và thực hiện **logic nghiệp vụ**.  
   - Phân quyền truy cập dựa trên hàm Middleware.  
   - Ví dụ: Manager role có thể thêm, sửa, xóa; Staff chỉ xem.

6. **Views**:  
   - Xây dựng API endpoints cho Swagger.  
   - Nhận request từ client, gọi Service, trả về response JSON.

---------------------------------------------------------------------------------------------------------------------------------------------------------

## 💻 Hướng dẫn cài đặt
1. Clone repo:
```bash
git clone https://github.com/TiCoder-coder/Z00_MANAGEMENT_PYTHON.git
cd Z00_MANAGEMENT_PYTHON

2. Tạo virtual environment:
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

3. Cài đặt dependencies:
pip install -r requirements.txt

4. Chạy migrations:
python manage.py migrate

5. Chạy server:
python manage.py runserver

6. Truy cập Swagger API:
http://127.0.0.1:8000/

---------------------------------------------------------------------------------------------------------------------------------------------------------

📝 Hướng dẫn sử dụng:

Sử dụng Swagger UI để test API.

Các endpoints được phân theo từng model:
 - /animals/
 - /enclosures/
 - /foods/
 - /feedRecords/
 - /managers/

Phân quyền theo role và xác thực bằng JWT token.
