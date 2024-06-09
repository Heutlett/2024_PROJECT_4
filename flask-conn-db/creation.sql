-- Description: This script creates the database schema for the project.
-- SQL Server 2019 syntax
-- Table for different restaurants
CREATE TABLE Restaurants (
    Restaurant_ID INT IDENTITY(1, 1) PRIMARY KEY,
    Name NVARCHAR(100),
    Location NVARCHAR(200),
    Opening_Time TIME,
    Closing_Time TIME
);
CREATE TABLE Food (
    ID INT IDENTITY(1, 1) PRIMARY KEY,
    Name NVARCHAR(70)
);
CREATE TABLE Food_Type (
    ID INT IDENTITY(1, 1) PRIMARY KEY,
    Name NVARCHAR(70)
);
CREATE TABLE Food_Type_Association (
    Type_ID INT,
    Food_ID INT,
    PRIMARY KEY (Type_ID, Food_ID)
);
-- Recommendation table without restaurant ID
CREATE TABLE Recommendation (
    ID INT IDENTITY(1, 1) PRIMARY KEY,
    Main_Dish_ID INT,
    Drink_ID INT,
    Dessert_ID INT
);
CREATE TABLE Tables (
    Table_Number INT PRIMARY KEY,
    Restaurant_ID INT,
    Chairs INT,
    FOREIGN KEY (Restaurant_ID) REFERENCES Restaurants(Restaurant_ID)
);
-- Calendar table with Restaurant ID
CREATE TABLE Reservations (
    Reservation_ID INT IDENTITY(1, 1) PRIMARY KEY,
    User_ID NVARCHAR(70),
    Restaurant_ID INT,
    Number_Of_People INT,
    Date_Reserved DATE,
    Start_Time TIME,
    End_Time TIME,
    FOREIGN KEY (Restaurant_ID) REFERENCES Restaurants(Restaurant_ID)
);
-- Shows the availability of each table
CREATE TABLE Table_Availability (
    Table_ID INT,
    Date_Reserved DATE,
    Start_Time TIME,
    End_Time TIME,
    PRIMARY KEY (Table_ID, Date_Reserved, Start_Time, End_Time),
    FOREIGN KEY (Table_ID) REFERENCES Tables(Table_Number)
);
-- Shows which tables are used for each reservation
CREATE TABLE Reservation_Tables_Association (
    Reservation_ID INT,
    Table_ID INT,
    PRIMARY KEY (Reservation_ID, Table_ID),
    FOREIGN KEY (Reservation_ID) REFERENCES Reservations(Reservation_ID),
    FOREIGN KEY (Table_ID) REFERENCES Tables(Table_Number)
);
CREATE TABLE User_ (
    Username NVARCHAR(70) PRIMARY KEY,
    Encrypted_Password NVARCHAR(70),
    First_Name NVARCHAR(70),
    Last_Name1 NVARCHAR(70),
    Last_Name2 NVARCHAR(70),
    Security_Question NVARCHAR(70),
    Security_Answer NVARCHAR(70)
);
CREATE TABLE User_Type (
    ID INT IDENTITY(1, 1) PRIMARY KEY,
    Type_Name NVARCHAR(70)
);
CREATE TABLE User_Type_Association (
    Username NVARCHAR(70),
    Type_ID INT,
    PRIMARY KEY (Username, Type_ID),
    FOREIGN KEY (Username) REFERENCES User_(Username),
    FOREIGN KEY (Type_ID) REFERENCES User_Type(ID)
);
-- Adding foreign key constraints
ALTER TABLE Food_Type_Association
ADD CONSTRAINT FK_Food_Type_Association_Food_Type FOREIGN KEY (Type_ID) REFERENCES Food_Type(ID);
ALTER TABLE Food_Type_Association
ADD CONSTRAINT FK_Food_Type_Association_Food FOREIGN KEY (Food_ID) REFERENCES Food(ID);
ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Main_Dish FOREIGN KEY (Main_Dish_ID) REFERENCES Food(ID);
ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Drink FOREIGN KEY (Drink_ID) REFERENCES Food(ID);
ALTER TABLE Recommendation
ADD CONSTRAINT FK_Recommendation_Dessert FOREIGN KEY (Dessert_ID) REFERENCES Food(ID);
ALTER TABLE Reservations
ADD CONSTRAINT FK_Reservations_User FOREIGN KEY (User_ID) REFERENCES User_(Username);
ALTER TABLE Table_Availability
ADD CONSTRAINT FK_Table_Availability_Tables FOREIGN KEY (Table_ID) REFERENCES Tables(Table_Number);
ALTER TABLE Reservation_Tables_Association
ADD CONSTRAINT FK_Reservation_Tables_Association_Reservation FOREIGN KEY (Reservation_ID) REFERENCES Reservations(Reservation_ID);
ALTER TABLE Reservation_Tables_Association
ADD CONSTRAINT FK_Reservation_Tables_Association_Table FOREIGN KEY (Table_ID) REFERENCES Tables(Table_Number);