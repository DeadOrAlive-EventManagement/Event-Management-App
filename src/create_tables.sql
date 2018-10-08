/* User is a keyword in sql, using customer instead  */

-- CREATE TABLE Customer(
--     customer_id INTEGER  PRIMARY KEY AUTO_INCREMENT,
--     email VARCHAR(100) NOT NULL UNIQUE,
--     /* 320 is usually used */
--     first_name VARCHAR(20) NOT NULL,
--     middle_name VARCHAR(20) NULL,
--     last_name VARCHAR(20) NOT NULL,
--     phone_number CHAR(10) DEFAULT '0000000000',
--     /* Default was added just for testing purposes, no need to keep inventing phone numbers */
--     pwd VARCHAR(100) NOT NULL
--     /* 255 is usually used */
-- );
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `SE_Project` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `SE_Project`;

CREATE TABLE `Bookings` (
  `book_id` int(11) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL,
  `booking_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Bookings` (`book_id`, `vendor_id`, `customer_id`, `service_id`, `booking_status`) VALUES
(60, 20, 2, 90, 'Pending'),
(61, 21, 1, 91, 'Accepted');

CREATE TABLE `Customer` (
  `customer_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `middle_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) NOT NULL,
  `phone_number` char(10) DEFAULT '0000000000',
  `pwd` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Customer` (`customer_id`, `email`, `first_name`, `middle_name`, `last_name`, `phone_number`, `pwd`) VALUES
(1, 'acb@gmail.com', 'acb', 'ed', 'efg', '9658741230', 'acbedefg'),
(2, 'xyz@gmail.com', 'xyz', NULL, 'uvw', '6758942536', 'uvwxyz');

CREATE TABLE `Events` (
  `event_id` int(11) NOT NULL,
  `event_name` varchar(100) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `budget` int(11) NOT NULL,
  `num_people` int(11) DEFAULT NULL,
  `date_event` date DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Events` (`event_id`, `event_name`, `customer_id`, `budget`, `num_people`, `date_event`, `service_id`) VALUES
(300, 'birthday', 1, 10000, 50, '2018-10-31', 90);

CREATE TABLE `Services` (
  `service_id` int(11) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `price_per_unit` decimal(10,0) NOT NULL,
  `service_type` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Services` (`service_id`, `vendor_id`, `service_name`, `price_per_unit`, `service_type`) VALUES
(90, 20, 'lunch food', '30', 'food'),
(91, 21, 'lights', '50', 'lights');

CREATE TABLE `Vendor` (
  `vendor_id` int(11) NOT NULL,
  `vendor_name` varchar(100) DEFAULT NULL,
  `vendor_location` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Vendor` (`vendor_id`, `vendor_name`, `vendor_location`) VALUES
(20, 'creepers', 'blore'),
(21, 'sleepers', 'MUMBAI');


ALTER TABLE `Bookings`
  ADD PRIMARY KEY (`book_id`),
  ADD KEY `vendor_id` (`vendor_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `service_id` (`service_id`);

ALTER TABLE `Customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

ALTER TABLE `Events`
  ADD PRIMARY KEY (`event_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `service_id` (`service_id`);

ALTER TABLE `Services`
  ADD PRIMARY KEY (`service_id`,`vendor_id`),
  ADD KEY `vendor_id` (`vendor_id`);

ALTER TABLE `Vendor`
  ADD PRIMARY KEY (`vendor_id`);


ALTER TABLE `Bookings`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

ALTER TABLE `Customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

ALTER TABLE `Events`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=301;

ALTER TABLE `Vendor`
  MODIFY `vendor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;


ALTER TABLE `Bookings`
  ADD CONSTRAINT `Bookings_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `Vendor` (`vendor_id`),
  ADD CONSTRAINT `Bookings_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`),
  ADD CONSTRAINT `Bookings_ibfk_3` FOREIGN KEY (`service_id`) REFERENCES `Services` (`service_id`);

ALTER TABLE `Events`
  ADD CONSTRAINT `Events_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customer` (`customer_id`),
  ADD CONSTRAINT `Events_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `Services` (`service_id`);

ALTER TABLE `Services`
  ADD CONSTRAINT `Services_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `Vendor` (`vendor_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
