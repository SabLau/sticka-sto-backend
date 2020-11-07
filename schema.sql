DROP TABLE IF EXISTS Stickers CASCADE;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Orders_Stickers;
DROP TABLE IF EXISTS Customer_Orders;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS user_login;

create extension pgcrypto;

-- TODO: Review Schema to host DB on heroku
CREATE TABLE Stickers(
  sticker_id SERIAL PRIMARY KEY,
  sticker_name VARCHAR (50) NOT NULL UNIQUE,
  img BYTEA NOT NULL,
  -- Updated img_url -> img
  price NUMERIC (5, 2),
  sticker_description VARCHAR(100)
);

CREATE TABLE Inventory(
  sticker_id INTEGER NOT NULL PRIMARY KEY,
  quantity INTEGER NOT NULL,
  CONSTRAINT sticker_fkey FOREIGN KEY (sticker_id)
    REFERENCES Stickers (sticker_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE Users(
  id SERIAL PRIMARY KEY,
  email VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE,
  shipping_address VARCHAR(355)
);

 CREATE TABLE user_login(
   user_id INTEGER NOT NULL,
   hashed_password TEXT NOT NULL,
   PRIMARY KEY (user_id),
   CONSTRAINT user_fkey FOREIGN KEY (user_id)
     REFERENCES Users (id) MATCH SIMPLE
     ON UPDATE NO ACTION ON DELETE NO ACTION
 );

CREATE TABLE Orders(
  order_id VARCHAR(12) PRIMARY KEY,
  user_id INTEGER NOT NULL,
  shipping_address VARCHAR (355) NOT NULL,
  order_date DATE NOT NULL DEFAULT CURRENT_DATE,
  ship_date DATE,
  CONSTRAINT user_fkey FOREIGN KEY (user_id)
    REFERENCES Users (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE Orders_Stickers(
  order_id VARCHAR(20) NOT NULL,
  sticker_id INTEGER NOT NULL,
  sticker_quantity INTEGER NOT NULL,
  PRIMARY KEY (order_id, sticker_id),
  CONSTRAINT sticker_fkey FOREIGN KEY (sticker_id)
    REFERENCES Stickers (sticker_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT order_fkey FOREIGN KEY (order_id)
    REFERENCES Orders (order_id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- CREATE TABLE Customer_Orders(
--   user_id INTEGER NOT NULL,
--   customer_name VARCHAR(50) NOT NULL,
--   customer_email VARCHAR(355) NOT NULL,
--   order_id VARCHAR(20) NOT NULL,
--   PRIMARY KEY (user_id, order_id),
--   CONSTRAINT user_fkey FOREIGN KEY (user_id)
--     REFERENCES Users (user_id) MATCH SIMPLE
--     ON UPDATE NO ACTION ON DELETE NO ACTION,
--   CONSTRAINT order_fkey FOREIGN KEY (order_id)
--     REFERENCES Orders (order_id) MATCH SIMPLE
--     ON UPDATE NO ACTION ON DELETE NO ACTION
-- );

