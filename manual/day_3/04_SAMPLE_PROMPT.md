# Prompt ที่ต้องเตรียมก่อน

## ภาษาไทย 
สร้าง github repo ส่วนตัว ชื่อ eda-app
ใช้ branch main

## English
Create a personal GitHub repository named eda-app.
Use the main branch.


# EDA CSV Data Processing Application Prompt

## ภาษาไทย

สร้างแอปพลเคชัน Exploratory Data Analysis (EDA) สำหรับไฟล์ synthetic_sales_1M.csv
ช่วยวิเคราห์ข้อมูล และตัดสินว่าจะต้องทำกราฟวิเคราะห์ข้อมูลแบบใดบ้าง และสร้างกราฟเหล่านั้น

เป็นระบบที่มีการล็อกอินด้วย username และ password
ภาษา Python
เก็บข้อมูลไว้ในฐานข้อมูล Postgresql ใช้ ORM SQLAlchemy
องค์ประกอบของแอปพลิเคชันให้รันผ่าน docker compose
Pydantic + Ruff + Mypy สำหรับตรวจสอบข้อมูลและจัดรูปแบบโค้ด


## English

Create an Exploratory Data Analysis (EDA) application for the synthetic_sales_1M.csv file.
The application should analyze the data and determine which types of graphs are needed for analysis, and then
generate those graphs.

The system should have a login feature with username and password.
Use Python as the programming language.
Store data in a PostgreSQL database using SQLAlchemy ORM.
Compose the application to run through Docker Compose.
Use Pydantic + Ruff + Mypy for data validation and code formatting.
