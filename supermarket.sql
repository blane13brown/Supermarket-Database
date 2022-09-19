CREATE DATABASE IF NOT EXISTS `supermarket`;
USE `supermarket`;


CREATE TABLE IF NOT EXISTS `customer` (
  `CustomerID` int(11) NOT NULL AUTO_INCREMENT,
  `CFName` varchar(50) DEFAULT NULL,
  `CLName` varchar(50) DEFAULT NULL,
  `Points` int(11) DEFAULT NULL,
  `CEmail` varchar(50) DEFAULT NULL,
  `CPhoneNumber` varchar(50) DEFAULT NULL,
  `CAddress` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;


INSERT INTO `customer` (`CustomerID`, `CFName`, `CLName`, `Points`, `CEmail`, `CPhoneNumber`, `CAddress`) VALUES
	(1, 'John', 'Smith', 20, 'jsmith@gmail.com', '8012213213', '209 Holly drive, Lubbock TX'),
	(2, 'Jane', 'Smith', 60, 'janes@gmail.com', '8674462334', '102 University Ave, Lubbock TX'),
	(3, 'Mark', 'Collins', 5, 'mc223@yahoo.com', '2013657693', '9872 50th st, Lubbock TX');

CREATE TABLE IF NOT EXISTS `department` (
  `DepartmentID` int(11) NOT NULL AUTO_INCREMENT,
  `DepartmentName` varchar(50) NOT NULL,
  `MgrId` int(11) NOT NULL DEFAULT 0,
  `MgrSSN` varchar(50) NOT NULL DEFAULT '0',
  `DepartmentPhoneNumber` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`DepartmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

INSERT INTO `department` (`DepartmentID`, `DepartmentName`, `MgrId`, `MgrSSN`, `DepartmentPhoneNumber`) VALUES
	(1, 'Management', 1, '2234461234', '5562347437'),
	(2, 'Produce', 2, '5477789456', '4537762345'),
	(3, ' Butcher', 3, '1234552343', '8863458468'),
	(4, 'Bakery', 4, '5531221652', '2125236634'),
	(5, 'Receiving', 5, '4567348356', '1237752354');

CREATE TABLE IF NOT EXISTS `employee` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `SSN` varchar(50) DEFAULT NULL,
  `Fname` varchar(50) DEFAULT NULL,
  `Lname` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Phone_Number` varchar(50) DEFAULT NULL,
  `EmergencyContactNumber` varchar(50) DEFAULT NULL,
  `DepartmentNumber` int(11) DEFAULT NULL,
  `Address` varchar(100) DEFAULT NULL,
  `Salary` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `SSN` (`SSN`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;


INSERT INTO `employee` (`ID`, `SSN`, `Fname`, `Lname`, `Email`, `Phone_Number`, `EmergencyContactNumber`, `DepartmentNumber`, `Address`, `Salary`) VALUES
	(1, '2234461234', 'Joshua', 'Gonzales', 'joshg@gmail.com', '4568763456', '2344436689', 1, '1703 Akron Drive, Lubbock TX', '80000'),
	(2, '5477789456', 'Daisy', 'Conners', 'daisy44@yahoo.com', '6674458456', '5546789567', 2, '1802 John St, Lubbock TX', '40000'),
	(3, '1234552343', 'Marcus', 'Martin', 'mm65@hotmail.com', '9723476543', '7659971266', 3, '901 29th St, Lubbock TX', '40000'),
	(4, '5531221652', 'Jeffery', 'Johnson', 'jeffery@gmail.com', '2142236423', '9725680945', 4, '1509 Milwakee, Lubbock TX', '50000'),
	(5, '4567348356', 'Katie', 'Mckinney', 'kmckinney@gmail.com', '6743358765', '2347673546', 5, '485 105th, Lubbock TX', '30000'),
	(6, '6436784667', 'Christine', 'White', 'cwhite4@yahoo.com', '7676465745', '6745677456', 2, '5542 107th, Lubbock TX', '70000'),
	(7, '8465746575', 'Kelly', 'Cross', 'kelly.cross@gmail.com', '4765745676', '9586745786', 1, '4554 115th, Lubbock TX', '60000'),
	(8, '4536345654', 'David', 'Williams', 'dww@gmail.com', '5867564784', '4567846574', 4, '6656 Quaker Rd, Lubbock TX', '30000'),
	(9, '345634565', 'Cameron', 'Carter', 'ccarter@yahoo.com', '8675567876', '4356345654', 3, '6695 Slide Rd, Lubbock TX', '20000'),
	(10, '967896745', 'Jessie', 'Jones', 'jessie776@gmail.com', '4764576556', '3456776564', 5, '1234 1st st, Lubbock TX', '50000');


CREATE TABLE IF NOT EXISTS `inventory` (
  `ItemID` int(11) NOT NULL AUTO_INCREMENT,
  `Price` double DEFAULT NULL,
  `ItemName` varchar(50) DEFAULT NULL,
  `SupplierID` int(11) DEFAULT NULL,
  `ItemCount` int(11) DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;


INSERT INTO `inventory` (`ItemID`, `Price`, `ItemName`, `SupplierID`, `ItemCount`) VALUES
	(1, 1.99, 'Bread', 1, 140),
	(2, 0.99, 'Tomatoes', 2, 548),
	(3, 10.99, 'Pizza', 3, 65),
	(4, 0.4, 'Lemons', 2, 200),
	(5, 1, 'Tomato Soup', 4, 50),
	(6, 10.99, 'Chicken Breasts', 5, 35),
	(7, 14.99, 'Sirloin Steak', 5, 25),
	(8, 1, 'Chicken Noodle Soup', 4, 75);

CREATE TABLE IF NOT EXISTS `supplier` (
  `SupplierID` int(11) NOT NULL AUTO_INCREMENT,
  `SupplierName` varchar(50) DEFAULT NULL,
  `SAddress` varchar(100) DEFAULT NULL,
  `SPhoneNumber` varchar(50) DEFAULT NULL,
  `SEmail` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;


INSERT INTO `supplier` (`SupplierID`, `SupplierName`, `SAddress`, `SPhoneNumber`, `SEmail`) VALUES
	(1, 'Oat Bakery', '1112 SH 13, Amarillo TX', '3456734565', 'general@oatbakery.com'),
	(2, 'Farm Fresh Produce', '2321 90th St, Lubbock TX', '4764567656', 'stores@ffproduce.com'),
	(3, 'Frozen Goods To Go', '1029 120th St, Lubbock TX', '7456745645', 'concerns@fgtg.com'),
	(4, 'Campbells Soup', '500 NW Loop 286, Paris TX', '9037843341', 'campbell@soup.com'),
	(5, 'Butchs Butchery', '9908 N Quaker, Lubbock TX', '6745674567', 'meat@butchs.com');


CREATE TABLE IF NOT EXISTS `supplies` (
  `SupplierID` int(11) NOT NULL,
  `ItemID` int(11) DEFAULT NULL,
  `OrderAmount` int(11) DEFAULT NULL,
  KEY `ItemID` (`ItemID`),
  KEY `SupplierID` (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `supplies` (`SupplierID`, `ItemID`, `OrderAmount`) VALUES
	(1, 1, 120),
	(5, 4, 23),
	(3, 3, 25);  