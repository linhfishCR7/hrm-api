# Chuẩn bị các thư viện trên máy để chạy phần mềm
## 1. Cài đặt python 3
      <img width="1419" alt="image" src="https://user-images.githubusercontent.com/59117535/174609597-7d865faf-31cf-4a75-b0f5-f49d7a2d516c.png">
      Truy cập vào https://www.python.org/downloads/ để cài về máy
## 2. Cài công cụ lập trình VS Code
      <img width="1410" alt="image" src="https://user-images.githubusercontent.com/59117535/174609961-798a7d73-4ac4-4a0b-a943-dd56fb713488.png">
      Truy cập vào https://code.visualstudio.com/ để tải về máy
## 3. Git clone source trên git hub hoặc download về https://github.com/linhfishCR7/hrm-api/releases/tag/v1.0.0
      3.1 Tạo file .env tập hợp key và cấu hình ở những bước tiếp theo
## 4. Cài đặt môi trường ảo - django - django rest framework
   4.1 Máy MacOS
        - Follow theo trang [Hướng dẫn tạo môi trường ảo và django]https://linhfishcr7.wordpress.com/2022/03/12/install-python3-virtualenv-django-and-start-a-new-project-on-your-macos/ để cài đặt môi trường ảo và django.
        - Follow theo [Trang Chủ Django Rest Framework](https://www.django-rest-framework.org/#installation) để cài đặt django rest framework
   4.2 Máy Window
        - Follow theo [Hướng dẫn cài django trên window]https://docs.djangoproject.com/en/4.0/howto/windows/
        - Follow theo [Trang Chủ Django Rest Framework](https://www.django-rest-framework.org/#installation) để cài đặt django rest framework
## 5. Cài đặt các dịch vụ trên AWS (Cognito, RDS - PostgressSQL, S3)
   5.1 Cognito 
        - Truy cập [aws.amazon.com](https://aws.amazon.com/)
        - Đăng ký Account
        - Vào Dashboard chọn <img width="1416" alt="image" src="https://user-images.githubusercontent.com/59117535/174612360-ed6bf9a2-d01e-4b24-8387-0790f4b482a1.png">
        - Tạo User Pool <img width="1436" alt="image" src="https://user-images.githubusercontent.com/59117535/174612512-448f55af-fc97-4dee-b3f1-67bdd29b39c1.png"> - Hướng dẫn tạo https://www.youtube.com/watch?v=0Wsov5vePjo
        - Lấy Key <img width="1412" alt="image" src="https://user-images.githubusercontent.com/59117535/174612956-cee4256e-4fd1-4934-9780-0a46c3bea51e.png">
    5.2 RDS
        - Follow https://www.youtube.com/watch?v=XDMgXZUfa10 để tạo và kết nối Database PostgressSQL
    5.3 S3
        - Chọn S3 <img width="1412" alt="image" src="https://user-images.githubusercontent.com/59117535/174613384-cc778e50-7535-4a5d-8fe0-49449811bf2a.png">
        - Follow https://aws.amazon.com/s3/getting-started/ để tạo S3
## 6. Firebase
        - <img width="1404" alt="image" src="https://user-images.githubusercontent.com/59117535/174613909-ee8506b5-81e8-43af-92ad-289200907b3f.png">
        - Truy cập vào https://firebase.google.com/ để tạo 
        - Truy cập vào tài khoản
## 7.  Chạy chương trình
        - pip install -r requirement.txt
        - python manage.py makemigrations
        - python manage.py migrate
        - python manage.py runserver
              
        
