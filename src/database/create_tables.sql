SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Bookings;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Vendor;
SET FOREIGN_KEY_CHECKS = 1;

DROP DATABASE SE_Project;

CREATE DATABASE SE_Project;
USE SE_Project;

CREATE TABLE Customer (
  customer_id int(11) PRIMARY KEY AUTO_INCREMENT,
  email varchar(100) UNIQUE,
  first_name varchar(20) NOT NULL,
  middle_name varchar(20) DEFAULT NULL,
  last_name varchar(20) NOT NULL,
  phone_number varchar(13) DEFAULT 0000000000,
  pwd varchar(100) NOT NULL,
  activation_status boolean DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Events (
  event_id int(11) PRIMARY KEY AUTO_INCREMENT,
  event_name varchar(100) NOT NULL,
  customer_id int(11),
  budget int(11) NOT NULL,
  num_people int(11) DEFAULT NULL,
  date_event date DEFAULT NULL,
  details varchar(500) DEFAULT NULL,
  FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Vendor (
  vendor_id int(11) PRIMARY KEY AUTO_INCREMENT,
  vendor_name varchar(100) DEFAULT NULL,
  vendor_location varchar(150) DEFAULT NULL,
  email varchar(100) UNIQUE,
  phone_number char(10) DEFAULT 0000000000,
  pwd varchar(100) NOT NULL,
  activation_status boolean DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Services (
  service_id int(11) PRIMARY KEY AUTO_INCREMENT,
  vendor_id int(11),
  service_name varchar(100) NOT NULL,
  price_per_unit decimal(10,0) NOT NULL,
  service_type varchar(100) DEFAULT NULL,
  description varchar(100) DEFAULT NULL,
  FOREIGN KEY (vendor_id) REFERENCES Vendor(vendor_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Bookings (
  event_id int(11),
  vendor_id int(11),
  customer_id int(11),
  service_id int(11),
  booking_status boolean DEFAULT FALSE,
  FOREIGN KEY (event_id) REFERENCES Events(event_id),
  FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  FOREIGN KEY (service_id) REFERENCES Services(service_id),
  PRIMARY KEY (event_id, customer_id, vendor_id, service_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;