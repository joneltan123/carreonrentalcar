-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 19, 2023 at 06:00 PM
-- Server version: 5.7.44-cll-lve
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `carreonr_db_rental_car_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminlogin_info`
--

CREATE TABLE `adminlogin_info` (
  `AdminFirstName` varchar(100) DEFAULT NULL,
  `AdminLastName` varchar(100) DEFAULT NULL,
  `Admin_UserName` varchar(100) DEFAULT NULL,
  `Admin_Password` varchar(100) DEFAULT NULL,
  `AdminPosition` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `adminlogin_info`
--

INSERT INTO `adminlogin_info` (`AdminFirstName`, `AdminLastName`, `Admin_UserName`, `Admin_Password`, `AdminPosition`) VALUES
('Jojo', 'Carreon', '@admin', '@admin', 'CRC Staff'),
('!', '?', 'hiadmin', ')(!@@))!', 'Secret Admin');

-- --------------------------------------------------------

--
-- Table structure for table `car_list`
--

CREATE TABLE `car_list` (
  `CarNo` int(11) NOT NULL,
  `Car_Name` varchar(255) DEFAULT NULL,
  `Car_Price_NoPromo` int(255) DEFAULT NULL,
  `Car_Price_WithPromo` int(255) DEFAULT NULL,
  `Image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `car_list`
--

INSERT INTO `car_list` (`CarNo`, `Car_Name`, `Car_Price_NoPromo`, `Car_Price_WithPromo`, `Image`) VALUES
(6, 'Red Mica Metallic Innova Manual', 1600, 5600, 'RedMicaMetallicInnovaManual.png'),
(7, 'Blackish Red Innova Automatic', 1500, 5600, 'BlackishRedInnovaAutomatic.png'),
(9, 'Pearl White Two Tone GI-Grandia', 1500, 5600, 'PearlWhiteTwoToneGI-Grandia.png'),
(11, 'Salver Metallic GI-Grandia', 1500, 5600, 'SilverMetallicGI-Grandia.png');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_customer_info`
--

CREATE TABLE `tbl_customer_info` (
  `id` int(11) DEFAULT NULL,
  `Car_Name` varchar(255) DEFAULT NULL,
  `CarNo` varchar(255) DEFAULT NULL,
  `Last_Name` varchar(255) DEFAULT NULL,
  `First_Name` varchar(255) DEFAULT NULL,
  `Gender` varchar(255) DEFAULT NULL,
  `Age` int(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Email_Address` varchar(255) DEFAULT NULL,
  `Mobile_Number` varchar(255) DEFAULT NULL,
  `Date_of_pickup` date DEFAULT NULL,
  `Date_of_return` date DEFAULT NULL,
  `Time_of_pickup` time DEFAULT NULL,
  `No_of_Days` int(255) DEFAULT NULL,
  `Car_per_days` int(255) DEFAULT NULL,
  `Transaction_ID` varchar(255) DEFAULT NULL,
  `Amount_to_Pay` int(255) DEFAULT NULL,
  `Down_Payment` int(255) DEFAULT NULL,
  `Total_Amount_to_Pay` int(255) DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL,
  `Id_Image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_customer_info`
--

INSERT INTO `tbl_customer_info` (`id`, `Car_Name`, `CarNo`, `Last_Name`, `First_Name`, `Gender`, `Age`, `Address`, `Email_Address`, `Mobile_Number`, `Date_of_pickup`, `Date_of_return`, `Time_of_pickup`, `No_of_Days`, `Car_per_days`, `Transaction_ID`, `Amount_to_Pay`, `Down_Payment`, `Total_Amount_to_Pay`, `Status`, `Id_Image`) VALUES
(9, 'Red Mica Metallic Innova Manual', '6', 'Tan', 'Jonel', 'Male', 19, 'San Isidro', 'jonel@yahoo.com', '09111111111', '2023-10-20', '2023-10-22', '18:29:00', 2, 2300, '9T8664849T907533C', 4600, 1500, 3100, 'Completed', 'id.png'),
(26, 'Red Mica Metallic Innova Manual', '6', 'ss', 'ss', 'Male', 21, 'ss', 'cust1@gmail.com', '09111111111', '2023-10-29', '2023-10-30', '12:19:00', 1, 1500, '4E293414VY7769500', 1500, 750, 750, 'Ongoing', 'id(2).png'),
(28, 'Red Mica Metallic Innova Manual', '6', 'Tan', 'Jonel', 'Male', 22, 'San Isidro Santa Rita Pampanga', 'joneltan123@gmail.com', '09505815582', '2023-10-31', '2023-11-06', '08:00:00', 6, 1500, '5LH80925KB766473F', 9000, 2250, 6750, 'Ongoing', 'id(3).png');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_register_customer_info`
--

CREATE TABLE `tbl_register_customer_info` (
  `CustomerID` int(11) NOT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `LastName` varchar(255) DEFAULT NULL,
  `Gender` varchar(255) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `EmailAddress` varchar(100) DEFAULT NULL,
  `MobileNumber` varchar(15) DEFAULT NULL,
  `UserName` varchar(50) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Valid_Id_Image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_register_customer_info`
--

INSERT INTO `tbl_register_customer_info` (`CustomerID`, `FirstName`, `LastName`, `Gender`, `Age`, `Address`, `EmailAddress`, `MobileNumber`, `UserName`, `Password`, `Valid_Id_Image`) VALUES
(9, 'Jonel', 'Tan', 'Male', 19, 'San Isidro', 'jonel@yahoo.com', '09111111111', '21', '12', 'id.png'),
(25, 'Bong Bong', 'Marcos', 'Male', 67, 'Manila', 'bbm@yahoo.com', '09564213587', 'bbm12345', 'bbm12345', 'id(1).png'),
(26, 'ss', 'ss', 'Male', 21, 'ss', 'cust1@gmail.com', '09111111111', 'sss12345', 'sss12345', 'id(2).png'),
(27, 'Catherine', 'Haitani', 'Female', 22, 'San Jose Santa Rita Pampanga', 'tolosacath10@gmail.com', '09364489096', 'catherine12', '123456qwerty', '20160421123729-car-rental.jpeg'),
(28, 'Jonel', 'Tan', 'Male', 22, 'San Isidro Santa Rita Pampanga', 'joneltan123@gmail.com', '09505815582', 'jonelt123', 'joneltan123', 'id(3).png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `car_list`
--
ALTER TABLE `car_list`
  ADD PRIMARY KEY (`CarNo`);

--
-- Indexes for table `tbl_register_customer_info`
--
ALTER TABLE `tbl_register_customer_info`
  ADD PRIMARY KEY (`CustomerID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `car_list`
--
ALTER TABLE `car_list`
  MODIFY `CarNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `tbl_register_customer_info`
--
ALTER TABLE `tbl_register_customer_info`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
