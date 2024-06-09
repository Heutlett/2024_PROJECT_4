-- Insert initial data into Restaurants
INSERT INTO Restaurants (Name, Location, Opening_Time, Closing_Time)
VALUES ('Restaurant A', 'Location A', '08:00', '22:00'),
    ('Restaurant B', 'Location B', '09:00', '23:00'),
    ('Restaurant C', 'Location C', '10:00', '20:00');
-- Insert tipos de alimentos
INSERT INTO Food_Type (Name)
VALUES ('MainCourse'),
    ('Drink'),
    ('Dessert');
-- Insert MainCourses
INSERT INTO Food (Name)
VALUES ('Pizza Margarita'),
    ('Spaghetti Carbonara'),
    ('Lasagna'),
    ('Chicken Alfredo'),
    ('Beef Wellington'),
    ('Sushi'),
    ('Burger'),
    ('Risotto'),
    ('Pad Thai'),
    ('Tacos'),
    ('Paella'),
    ('Fish and Chips'),
    ('Pho'),
    ('Curry'),
    ('Fajitas'),
    ('Pasta Carbonara'),
    ('Steak'),
    ('Roast Chicken'),
    ('Sushi'),
    ('Hamburger');
-- Insert Desserts
INSERT INTO Food (Name)
VALUES ('Tiramisu'),
    ('Cheesecake'),
    ('Chocolate Fondant'),
    ('Apple Pie'),
    ('Creme Brulee'),
    ('Banoffee Pie'),
    ('Panna Cotta'),
    ('Key Lime Pie'),
    ('Red Velvet Cake'),
    ('Cannoli'),
    ('Baklava'),
    ('Pavlova'),
    ('Cupcakes'),
    ('Chocolate Mousse'),
    ('Gelato'),
    ('Creme Brulee'),
    ('Tiramisu'),
    ('Chocolate Cake'),
    ('Apple Crisp'),
    ('Peach Cobbler');
-- Insert Drinks
INSERT INTO Food (Name)
VALUES ('Mojito'),
    ('Margarita'),
    ('Martini'),
    ('Cosmopolitan'),
    ('Gin and Tonic'),
    ('Pina Colada'),
    ('Daiquiri'),
    ('Tequila Sunrise'),
    ('Bloody Mary'),
    ('Mai Tai'),
    ('Old Fashioned'),
    ('White Russian'),
    ('Long Island Iced Tea'),
    ('Singapore Sling'),
    ('Moscow Mule'),
    ('Margarita'),
    ('Gin and Tonic'),
    ('Martini'),
    ('Sangria'),
    ('Negroni');
-- Insertar las asociaciones entre los tipos de comida y las comidas
-- Obtener los IDs de los tipos de comida
DECLARE @MainCourseID INT;
DECLARE @DessertID INT;
DECLARE @DrinkID INT;
SELECT @MainCourseID = ID
FROM Food_Type
WHERE Name = 'MainCourse';
SELECT @DessertID = ID
FROM Food_Type
WHERE Name = 'Dessert';
SELECT @DrinkID = ID
FROM Food_Type
WHERE Name = 'Drink';
-- Asociar MainCourses
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @MainCourseID,
    ID
FROM Food
WHERE Name IN (
        'Pizza Margarita',
        'Spaghetti Carbonara',
        'Lasagna',
        'Chicken Alfredo',
        'Beef Wellington',
        'Sushi',
        'Burger',
        'Risotto',
        'Pad Thai',
        'Tacos',
        'Paella',
        'Fish and Chips',
        'Pho',
        'Curry',
        'Fajitas',
        'Pasta Carbonara',
        'Steak',
        'Roast Chicken'
    );
-- Asociar Desserts
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @DessertID,
    ID
FROM Food
WHERE Name IN (
        'Tiramisu',
        'Cheesecake',
        'Chocolate Fondant',
        'Apple Pie',
        'Creme Brulee',
        'Banoffee Pie',
        'Panna Cotta',
        'Key Lime Pie',
        'Red Velvet Cake',
        'Cannoli',
        'Baklava',
        'Pavlova',
        'Cupcakes',
        'Chocolate Mousse',
        'Gelato',
        'Creme Brulee',
        'Tiramisu',
        'Chocolate Cake',
        'Apple Crisp',
        'Peach Cobbler'
    );
-- Asociar Drinks
INSERT INTO Food_Type_Association (Type_ID, Food_ID)
SELECT @DrinkID,
    ID
FROM Food
WHERE Name IN (
        'Mojito',
        'Margarita',
        'Martini',
        'Cosmopolitan',
        'Gin and Tonic',
        'Pina Colada',
        'Daiquiri',
        'Tequila Sunrise',
        'Bloody Mary',
        'Mai Tai',
        'Old Fashioned',
        'White Russian',
        'Long Island Iced Tea',
        'Singapore Sling',
        'Moscow Mule',
        'Margarita',
        'Gin and Tonic',
        'Martini',
        'Sangria',
        'Negroni'
    );
-- Insertar tipos de usuarios
INSERT INTO User_Type (Type_Name)
VALUES ('Admin'),
    ('Client');
-- Insertar usuarios
-- password = "admin1"
-- security answer = "Blue"
INSERT INTO User_ (
        Username,
        Encrypted_Password,
        First_Name,
        Last_Name1,
        Last_Name2,
        Security_Question,
        Security_Answer
    )
VALUES (
        'admin1',
        '25F43B1486AD95A1398E3EEB3D83BC4010015FCC9BEDB35B432E00298D5021F7',
        'Jimena',
        'Leon',
        'Huertas',
        'What is your favorite color?',
        'EC7D56A01607001E6401366417C5E2EB00FFA0DF17CA1A9A831E0B32C8F11BF7'
    ),
    -- password = "client1"
    -- security answer = "Blue"
    (
        'client1',
        '1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223',
        'Fulana',
        'Perez',
        'Gonzalez',
        'What is your favorite color?',
        'EC7D56A01607001E6401366417C5E2EB00FFA0DF17CA1A9A831E0B32C8F11BF7'
    );
-- Asocia usuarios con el tipo de usuario Admin
INSERT INTO User_Type_Association (Username, Type_ID)
VALUES ('admin1', 1);
-- Asocia usuarios con el tipo de usuario Client
INSERT INTO User_Type_Association (Username, Type_ID)
VALUES ('client1', 2);
-- Insertar mesas
INSERT INTO Tables (Table_Number, Restaurant_ID, Chairs)
VALUES (1, 1, 4),
    (2, 1, 6),
    (3, 1, 2),
    (4, 1, 8),
    (5, 1, 4),
    (6, 1, 6),
    (7, 1, 2),
    (8, 1, 8),
    (9, 1, 4),
    (10, 1, 6),
    (11, 2, 4),
    (12, 2, 6),
    (13, 2, 2),
    (14, 2, 8),
    (15, 2, 4),
    (16, 2, 6),
    (17, 2, 2),
    (18, 2, 8),
    (19, 2, 4),
    (20, 2, 6),
    (21, 3, 4),
    (22, 3, 6),
    (23, 3, 2),
    (24, 3, 8),
    (25, 3, 4),
    (26, 3, 6),
    (27, 3, 2),
    (28, 3, 8),
    (29, 3, 4),
    (30, 3, 6);
-- Insertar reservaciones
INSERT INTO Reservations (
        User_ID,
        Restaurant_ID,
        Number_Of_People,
        Date_Reserved,
        Start_Time,
        End_Time
    )
VALUES (
        'client1',
        1,
        4,
        '2021-12-01',
        '18:00:00',
        '20:00:00'
    ),
    (
        'client1',
        1,
        2,
        '2021-12-01',
        '16:00:00',
        '18:00:00'
    ),
    (
        'client1',
        1,
        6,
        '2021-12-01',
        '15:00:00',
        '17:00:00'
    ),
    (
        'client1',
        1,
        8,
        '2021-12-01',
        '20:00:00',
        '22:00:00'
    ),
    (
        'client1',
        1,
        4,
        '2021-12-01',
        '19:00:00',
        '21:00:00'
    );
-- Insertar disponibilidad de mesas
INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time)
VALUES (1, '2021-12-01', '18:00:00', '20:00:00'),
    (2, '2021-12-01', '16:00:00', '18:00:00'),
    (3, '2021-12-01', '15:00:00', '17:00:00'),
    (4, '2021-12-01', '20:00:00', '22:00:00'),
    (5, '2021-12-01', '19:00:00', '21:00:00'),
    (8, '2021-12-01', '19:00:00', '21:00:00');
-- Insertar asociaciones entre reservaciones y mesas
INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID)
VALUES (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (5, 8);
-- Insertar datos en la tabla Recommendation
-- Obtener los IDs de los platos principales, bebidas y postres

SELECT @MainCourseID = MIN(Food_ID)
FROM Food_Type_Association
WHERE Type_ID = @MainCourseID;

SELECT @DrinkID = MIN(Food_ID)
FROM Food_Type_Association
WHERE Type_ID = @DrinkID;

SELECT @DessertID = MIN(Food_ID)
FROM Food_Type_Association
WHERE Type_ID = @DessertID;

DECLARE @Counter1 INT = @MainCourseID+1;
DECLARE @Counter2 INT = @DessertID+1;
DECLARE @Counter3 INT = @DrinkID+1;
-- Insertar recomendaciones emparejando platos principales con bebidas y postres
WHILE @Counter1 <21 BEGIN
    INSERT INTO Recommendation (Main_Dish_ID, Drink_ID, Dessert_ID)
    VALUES (@MainCourseID, @DrinkID, @DessertID);
    -- Obtener los siguientes IDs
    SELECT @Counter1
    FROM Food_Type_Association
    WHERE Type_ID = @MainCourseID
    AND Food_ID > @MainCourseID;

    SELECT @Counter3
    FROM Food_Type_Association
    WHERE Type_ID = @DrinkID
    AND Food_ID > @DrinkID;

    SELECT @Counter2
    FROM Food_Type_Association
    WHERE Type_ID = @DessertID
    AND Food_ID > @DessertID;

    SET @MainCourseID = @Counter1;
    SET @DrinkID =@Counter3;
    SET @DessertID=@Counter2;

    SET @Counter1 = @Counter1+1;
    SET @Counter2 = @Counter2+1;
    SET @Counter3 = @Counter3+1;
END;
-- Insertar una recomendación adicional
INSERT INTO Recommendation (Main_Dish_ID, Drink_ID, Dessert_ID)
VALUES (20, 60, 40);