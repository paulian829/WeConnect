-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 10, 2021 at 02:20 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `weconnect`
--

DELIMITER $$
--
-- Procedures
--
CREATE  PROCEDURE `addPosition` (IN `test` VARCHAR(50))  BEGIN
	INSERT INTO position (position_name) VALUES (test);
END$$

CREATE  PROCEDURE `addUser` (IN `uEmail` VARCHAR(50), IN `uPassword` VARCHAR(100), IN `uFirstName` VARCHAR(50), IN `uLastName` VARCHAR(50), IN `uPhoneNumber` VARCHAR(11), IN `uPosition` INT(1))  BEGIN
INSERT INTO users (Email, Pass, FirstName, LastName, PhoneNumber, Position) VALUES (uEmail, uPassword, uFirstName, uLastName, uPhoneNumber, uPosition);
END$$

CREATE  PROCEDURE `deleteUser` (IN `uid` INT(11))  BEGIN
DELETE FROM users WHERE id = uid;
END$$

CREATE  PROCEDURE `emptyTrash` (IN `uid` INT)  BEGIN
DELETE FROM files WHERE status = 4 AND UploadedByID = uid;

END$$

CREATE  PROCEDURE `getAllFiles` (IN `uid` INT)  BEGIN
SELECT * FROM files where UploadedByID = uid ORDER BY FileID DESC;

END$$

CREATE  PROCEDURE `getFile` (IN `uid` INT(11))  BEGIN
	SELECT * FROM files WHERE FileID = uid;
END$$

CREATE  PROCEDURE `getNFiles` (IN `uid` INT, IN `number` INT)  BEGIN
SELECT * FROM files WHERE UploadedByID = uid AND status=0 ORDER BY FileID DESC LIMIT number;
END$$

CREATE  PROCEDURE `getNumberOfFilesPassed` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=1;
END$$

CREATE  PROCEDURE `getNumberOfFilesUploaded` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=0;
END$$

CREATE  PROCEDURE `moveFileToThrash` (IN `id` INT)  BEGIN
UPDATE files SET status = 4 where FileID = id;
END$$

CREATE  PROCEDURE `number_of_files_deadline` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=2;
END$$

CREATE  PROCEDURE `number_of_files_nearing_Deadline` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=3;
END$$

CREATE  PROCEDURE `Restore` (IN `uID` INT)  BEGIN
UPDATE files SET status = 0 WHERE FileID = uID;
END$$

CREATE  PROCEDURE `saveFile` (IN `uFileName` VARCHAR(100), IN `uFileType` VARCHAR(20), IN `uFileSize` INT(11), IN `uFileContentType` VARCHAR(100), IN `uUploadedByID` INT(11), IN `uShare_to_user` INT(11), IN `uShare_to_group` INT(11), IN `uDeadLine` DATE, IN `uRevision` INT(11), IN `date` DATE)  BEGIN
INSERT INTO files (FileName, FileType,FileSize, FileContentType, UploadedByID, Share_to_user, Share_to_group, DeadLine, Revision,dateUploaded) VALUES (uFileName, uFileType, uFileSize, uFileContentType, uUploadedByID, uShare_to_user, uShare_to_group, uDeadLine, uRevision,date);
SELECT last_insert_id();
END$$

CREATE  PROCEDURE `SelectAllPostions` ()  BEGIN
	SELECT * FROM position;
END$$

CREATE  PROCEDURE `SelectAllUsers` ()  BEGIN
	SELECT * FROM users;
END$$

CREATE  PROCEDURE `selectPositionID` (IN `uID` INT(11))  BEGIN
	SELECT * FROM position WHERE id = uID;
END$$

CREATE  PROCEDURE `selectUserEmail` (IN `uEmail` VARCHAR(50))  BEGIN
	SELECT * FROM users WHERE email = uEmail;
END$$

CREATE  PROCEDURE `selectUserID` (IN `uID` INT(11))  BEGIN
	SELECT * FROM users WHERE id = uID;
END$$

CREATE  PROCEDURE `updateDOC` (IN `json` LONGTEXT, IN `uID` INT)  BEGIN
UPDATE files SET block_doc_json = json WHERE FileID = uID;

END$$

CREATE  PROCEDURE `updateUser` (IN `uEmail` VARCHAR(50), IN `uFirstname` VARCHAR(50), IN `uLastName` VARCHAR(50), IN `uPhoneNumber` VARCHAR(11), IN `uPosition` INT(11), IN `uID` INT(11))  BEGIN
UPDATE users SET Email = uEmail, FirstName = uFirstname, LastName= uLastName, PhoneNumber=uPhoneNumber, Position = uPosition WHERE id = uID;

END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `FileID` int(11) NOT NULL,
  `FileName` varchar(100) NOT NULL,
  `FileType` varchar(20) NOT NULL,
  `FileSize` int(11) NOT NULL,
  `FileContentType` varchar(100) NOT NULL,
  `UploadedByID` int(11) NOT NULL,
  `Share_to_user` int(11) NOT NULL,
  `Share_to_group` int(11) NOT NULL,
  `DeadLine` date NOT NULL,
  `Revision` int(11) NOT NULL,
  `DateUploaded` date NOT NULL,
  `block_doc_json` longtext NOT NULL DEFAULT '[{"id":"xPmqz3gBHy","type":"header","data":{"text":"This is the Heading!","level":1}}]',
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`FileID`, `FileName`, `FileType`, `FileSize`, `FileContentType`, `UploadedByID`, `Share_to_user`, `Share_to_group`, `DeadLine`, `Revision`, `DateUploaded`, `block_doc_json`, `status`) VALUES
(31, 'test', 'block doc', 1, 'test', 83, 0, 1, '1231-03-12', 1, '2021-11-27', '[{\"id\":\"xPmqz3gBHy\",\"type\":\"header\",\"data\":{\"text\":\"This is the Heading!\",\"level\":1}},{\"id\":\"XNKBJiLbTV\",\"type\":\"header\",\"data\":{\"text\":\"1234567890\",\"level\":2}}]', 4),
(57, 'CAMILLE-P.-MERENE.pdf', 'raw file', 1, 'application/pdf', 82, 0, 1, '1111-11-11', 1, '2021-12-10', '[{\"id\":\"xPmqz3gBHy\",\"type\":\"header\",\"data\":{\"text\":\"This is the Heading!\",\"level\":1}}]', 0);

-- --------------------------------------------------------

--
-- Table structure for table `position`
--

CREATE TABLE `position` (
  `id` int(11) NOT NULL,
  `position_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `position`
--

INSERT INTO `position` (`id`, `position_name`) VALUES
(1, 'admin'),
(2, 'District Supervisor'),
(3, 'Grade Chairman'),
(4, 'Teacher'),
(5, 'Principal'),
(38, 'test');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Pass` varchar(100) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `PhoneNumber` varchar(11) NOT NULL,
  `Position` int(11) NOT NULL,
  `DateCreated` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Email`, `Pass`, `FirstName`, `LastName`, `PhoneNumber`, `Position`, `DateCreated`) VALUES
(82, 'admin@gmail.com', '89805776bf3dbcf0bad0bce14704d89eccde55cef2cd7cf6f068010d2ceb9480', 'super', 'admin', '+4497511601', 1, '2021-11-18 08:36:42'),
(83, 'test@gmail.com', '89805776bf3dbcf0bad0bce14704d89eccde55cef2cd7cf6f068010d2ceb9480', 'test', 'test', '+4497511601', 2, '2021-11-18 09:06:53'),
(86, 'weconnect.thesis@gmail.com', '89805776bf3dbcf0bad0bce14704d89eccde55cef2cd7cf6f068010d2ceb9480', 'Super', '2', '01234567890', 1, '2021-11-22 00:17:06');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`FileID`);

--
-- Indexes for table `position`
--
ALTER TABLE `position`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `FileID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `position`
--
ALTER TABLE `position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
