-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2022 at 05:24 PM
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

CREATE  PROCEDURE `addProfilePicDB` (IN `str` VARCHAR(200), IN `uID` INT(11))  BEGIN
UPDATE users SET profilePic = str WHERE id = uID;
END$$

CREATE  PROCEDURE `AddTask` (IN `Name` VARCHAR(100), IN `createdBy` INT(11), IN `dateCreated` DATETIME, IN `deadline` DATETIME, IN `description` TEXT, IN `Tstatus` VARCHAR(100), IN `scheduled` VARCHAR(50))  BEGIN
INSERT INTO tasks (TaskName, TaskCreatedBy, TaskDateCreated, TaskDeadline, TaskDescription,TaskStatus, TaskSchedule) VALUES (Name, createdBy,dateCreated, deadline, description, Tstatus, scheduled);
SELECT last_insert_id();
END$$

CREATE  PROCEDURE `addUser` (IN `uEmail` VARCHAR(50), IN `uPassword` VARCHAR(100), IN `uFirstName` VARCHAR(50), IN `uLastName` VARCHAR(50), IN `uPhoneNumber` VARCHAR(15), IN `uPosition` INT(1))  BEGIN
INSERT INTO users (Email, Pass, FirstName, LastName, PhoneNumber, Position) VALUES (uEmail, uPassword, uFirstName, uLastName, uPhoneNumber, uPosition);
END$$

CREATE  PROCEDURE `checkUserUpload` (IN `userID` INT, IN `TtaskID` INT)  BEGIN
	SELECT * FROM files WHERE (UploadedByID = userID AND taskID = TtaskID);
END$$

CREATE  PROCEDURE `createEvent` (IN `uploaded_by` INT(11), IN `file_ID` INT(11), IN `date_uploaded` DATETIME, IN `share_to_user` INT(11), IN `seen` INT(11), IN `event_type` VARCHAR(100))  BEGIN
	INSERT INTO event (Uploader,FileID,DateUploaded,TargetUserID,Seen,EventType) VALUES (uploaded_by,file_ID,date_uploaded,share_to_user,seen,event_type);
END$$

CREATE  PROCEDURE `deleteCommentDB` (IN `uid` INT)  BEGIN
DELETE FROM comments WHERE ID = uid;
END$$

CREATE  PROCEDURE `deleteFile` (IN `uid` INT)  BEGIN
DELETE FROM files WHERE FileID = uid;

END$$

CREATE  PROCEDURE `deleteTaskDb` (IN `uid` INT(11))  BEGIN
DELETE FROM tasks WHERE TaskID = uid;
END$$

CREATE  PROCEDURE `deleteUser` (IN `uid` INT(11))  BEGIN
DELETE FROM users WHERE id = uid;
END$$

CREATE  PROCEDURE `emptyTrash` (IN `uid` INT)  BEGIN
DELETE FROM files WHERE status = 4 AND UploadedByID = uid;

END$$

CREATE  PROCEDURE `getAllComments` ()  BEGIN
	SELECT * FROM comments;
END$$

CREATE  PROCEDURE `getAllFiles` (IN `uid` INT, IN `uemail` VARCHAR(100))  BEGIN
SELECT * FROM files where UploadedByID = uid OR Share_to_user = uemail ORDER BY FileName ASC;

END$$

CREATE  PROCEDURE `getAllFilesForAdmin` ()  BEGIN
SELECT * FROM files ORDER BY FileID ASC;
END$$

CREATE  PROCEDURE `getAllFileSortedByName` ()  BEGIN
SELECT * FROM files ORDER BY FileName ASC;
END$$

CREATE  PROCEDURE `getAllFileSortedByType` ()  BEGIN
SELECT * FROM files ORDER BY FileType ASC;
END$$

CREATE  PROCEDURE `getAllFilesType` (IN `uid` INT, IN `uemail` VARCHAR(100))  BEGIN
SELECT * FROM files where UploadedByID = uid OR Share_to_user = uemail ORDER BY FileType ASC;

END$$

CREATE  PROCEDURE `getCommentsDB` (IN `uid` INT)  BEGIN
	SELECT * FROM comments WHERE FileID = uid ORDER BY ID DESC;
END$$

CREATE  PROCEDURE `getDone` ()  BEGIN
	SELECT * FROM tasks WHERE TaskStatus = 'Done' ;
END$$

CREATE  PROCEDURE `getEvent` (IN `user` INT)  BEGIN
	SELECT * FROM event WHERE TargetUserID = user;
END$$

CREATE  PROCEDURE `getFile` (IN `uid` INT(11))  BEGIN
	SELECT * FROM files WHERE FileID = uid;
END$$

CREATE  PROCEDURE `getFileTask` (IN `uid` INT(11), IN `uTaskID` INT(11))  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND taskID = uTaskID;
END$$

CREATE  PROCEDURE `getNFiles` (IN `uid` INT, IN `number` INT, IN `uemail` VARCHAR(100))  BEGIN
SELECT * FROM files WHERE (UploadedByID = uid OR Share_to_user = uemail)AND status=0 ORDER BY FileID DESC LIMIT number;
END$$

CREATE  PROCEDURE `getNumberOfFilesPassed` (IN `uid` INT, IN `estatus` VARCHAR(100))  BEGIN
	SELECT * FROM tasks;
END$$

CREATE  PROCEDURE `getNumberOfFilesUploaded` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=0;
END$$

CREATE  PROCEDURE `getPassedForGradeChairman` ()  BEGIN
	SELECT * FROM tasks WHERE NOT TaskStatus = 'Pending Teachers' AND NOT TaskStatus = 'Pending Grade Chairman';
END$$

CREATE  PROCEDURE `getPassedForPrincipal` ()  BEGIN
	SELECT * FROM tasks WHERE NOT TaskStatus = 'Pending Teachers' AND NOT TaskStatus = 'Pending Grade Chairman' AND NOT TaskStatus = 'Pending Principal';
END$$

CREATE  PROCEDURE `getPending` (IN `uStatus` VARCHAR(100))  BEGIN
	SELECT * FROM tasks WHERE TaskStatus = uStatus ;
END$$

CREATE  PROCEDURE `getPendingTeachers` (IN `estatus` VARCHAR(100))  BEGIN
	SELECT * FROM tasks WHERE TaskStatus = estatus;
END$$

CREATE  PROCEDURE `getTaskByStatus` (IN `statusText` VARCHAR(100))  BEGIN
	SELECT * FROM tasks WHERE TaskStatus = statusText;
END$$

CREATE  PROCEDURE `getTasksDB` (IN `sched` VARCHAR(100))  BEGIN
	SELECT * FROM tasks WHERE TaskSchedule = sched;
END$$

CREATE  PROCEDURE `getTeachers` ()  BEGIN
	SELECT * FROM users WHERE Position = 4;
END$$

CREATE  PROCEDURE `getUserViaEmail` (IN `Uemail` VARCHAR(100))  BEGIN
	SELECT * FROM users WHERE Email = Uemail;
END$$

CREATE  PROCEDURE `moveFileToThrash` (IN `id` INT)  BEGIN
UPDATE files SET status = 4 where FileID = id;
END$$

CREATE  PROCEDURE `newComment` (IN `userID` INT, IN `fileID` INT, IN `TimeToday` INT(20), IN `Tcomment` VARCHAR(300))  BEGIN
	INSERT INTO comments (FileID,UserID,DateCreated,CommentMsg  ) VALUES (fileID, userID, TimeToday,Tcomment );
END$$

CREATE  PROCEDURE `number_of_files_deadline` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=2;
END$$

CREATE  PROCEDURE `number_of_files_nearing_Deadline` (IN `uid` INT)  BEGIN
	SELECT * FROM files WHERE UploadedByID = uid AND status=3;
END$$

CREATE  PROCEDURE `resetPassword` (IN `NewPass` VARCHAR(100), IN `uID` INT)  BEGIN
UPDATE users SET Pass = NewPass WHERE id = uID;

END$$

CREATE  PROCEDURE `Restore` (IN `uID` INT)  BEGIN
UPDATE files SET status = 0 WHERE FileID = uID;
END$$

CREATE  PROCEDURE `saveFile` (IN `uFileName` VARCHAR(100), IN `uFileType` VARCHAR(20), IN `uFileSize` INT(11), IN `uFileContentType` VARCHAR(100), IN `uUploadedByID` INT(11), IN `uShare_to_user` VARCHAR(100), IN `uShare_to_group` INT(11), IN `uDeadLine` DATETIME, IN `uRevision` INT(11), IN `date` DATETIME, IN `tID` INT, IN `filepath` VARCHAR(100))  BEGIN
INSERT INTO files (FileName, FileType,FileSize, FileContentType, UploadedByID, Share_to_user, Share_to_group, DeadLine, Revision,dateUploaded,taskID,FilePathName) VALUES (uFileName, uFileType, uFileSize, uFileContentType, uUploadedByID, uShare_to_user, uShare_to_group, uDeadLine, uRevision,date,tID,filepath);
SELECT last_insert_id();
END$$

CREATE  PROCEDURE `SelectAllPostions` ()  BEGIN
	SELECT * FROM position;
END$$

CREATE  PROCEDURE `SelectAllTask` ()  BEGIN
	SELECT * FROM tasks;
END$$

CREATE  PROCEDURE `SelectAllUsers` ()  BEGIN
	SELECT * FROM users;
END$$

CREATE  PROCEDURE `SelectOneTask` (IN `uid` INT)  BEGIN
	SELECT * FROM tasks WHERE TaskID = uid;
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

CREATE  PROCEDURE `SetPinned` (IN `uID` INT, IN `PinStatus` INT)  BEGIN
UPDATE files SET pinned = PinStatus WHERE FileID = uID;
END$$

CREATE  PROCEDURE `Update Task` (IN `ID` INT, IN `name` VARCHAR(100), IN `imageBlob` BLOB, IN `deadline` DATETIME, IN `description` TEXT)  BEGIN
UPDATE tasks SET TaskName = name, TaskImage = imageBlob, TaskDeadline = deadline, TaskDescription = description WHERE TaskID = ID;

END$$

CREATE  PROCEDURE `Update Task Status` (IN `ID` INT, IN `tstatus` VARCHAR(100))  BEGIN
UPDATE tasks SET TaskStatus = tstatus WHERE TaskID = ID;

END$$

CREATE  PROCEDURE `updateDOC` (IN `json` LONGTEXT, IN `uID` INT)  BEGIN
UPDATE files SET block_doc_json = json WHERE FileID = uID;

END$$

CREATE  PROCEDURE `updateTask` (IN `uID` INT, IN `name` VARCHAR(100), IN `deadline` DATETIME, IN `description` TEXT, IN `Tstatus` VARCHAR(100), IN `Tschedule` VARCHAR(50))  BEGIN
UPDATE tasks SET taskName  = name, TaskDeadline = deadline, TaskDescription= description, TaskStatus=Tstatus, TaskSchedule = Tschedule WHERE TaskID  = uID;

END$$

CREATE  PROCEDURE `updateTaskStatus` (IN `statusText` VARCHAR(100), IN `ID` INT)  BEGIN
UPDATE tasks SET TaskStatus = statusText WHERE TaskID = ID;

END$$

CREATE  PROCEDURE `updateUser` (IN `uEmail` VARCHAR(50), IN `uFirstname` VARCHAR(50), IN `uLastName` VARCHAR(50), IN `uPhoneNumber` VARCHAR(100), IN `uPosition` INT(11), IN `uID` INT(11))  BEGIN
UPDATE users SET Email = uEmail, FirstName = uFirstname, LastName= uLastName, PhoneNumber=uPhoneNumber, Position = uPosition WHERE id = uID;

END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `ID` int(11) NOT NULL,
  `FileID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `DateCreated` int(20) NOT NULL,
  `CommentMsg` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `EventID` int(11) NOT NULL,
  `Uploader` int(11) NOT NULL,
  `FileID` int(11) NOT NULL,
  `DateUploaded` datetime NOT NULL,
  `TargetUserID` int(11) NOT NULL,
  `Seen` int(11) NOT NULL,
  `EventType` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`EventID`, `Uploader`, `FileID`, `DateUploaded`, `TargetUserID`, `Seen`, `EventType`) VALUES
(60, 97, 53, '2022-03-10 01:17:57', 93, 1, 'Task Forward'),
(61, 129, 69, '2022-03-12 17:22:01', 127, 1, 'New Task'),
(62, 127, 67, '2022-03-12 17:41:14', 129, 1, 'Task Upload'),
(63, 127, 67, '2022-03-12 17:41:59', 129, 1, 'Task Upload'),
(64, 127, 67, '2022-03-12 17:41:59', 128, 1, 'Task Upload'),
(65, 133, 67, '2022-03-12 18:14:24', 129, 1, 'Task Upload'),
(66, 133, 67, '2022-03-12 18:14:24', 134, 1, 'Task Upload'),
(67, 127, 69, '2022-03-12 19:40:45', 129, 1, 'Task Upload'),
(68, 127, 69, '2022-03-12 19:40:45', 128, 1, 'Task Upload'),
(69, 127, 67, '2022-03-12 19:42:03', 129, 1, 'Task Upload'),
(70, 127, 67, '2022-03-12 19:42:03', 128, 1, 'Task Upload'),
(71, 136, 67, '2022-03-13 10:42:16', 129, 1, 'Task Upload'),
(72, 136, 67, '2022-03-13 10:42:16', 128, 1, 'Task Upload'),
(74, 128, 67, '2022-03-13 13:05:40', 129, 1, 'Task Forward'),
(75, 129, 70, '2022-03-13 21:13:41', 127, 1, 'New Task'),
(76, 129, 70, '2022-03-13 21:13:41', 135, 0, 'New Task'),
(77, 129, 70, '2022-03-13 21:13:41', 136, 0, 'New Task'),
(78, 127, 70, '2022-03-13 21:14:34', 129, 1, 'Task Upload'),
(79, 127, 70, '2022-03-13 21:14:34', 128, 1, 'Task Upload'),
(80, 133, 70, '2022-03-13 21:16:17', 129, 1, 'Task Upload'),
(81, 133, 70, '2022-03-13 21:16:17', 134, 1, 'Task Upload'),
(82, 127, 69, '2022-03-13 21:40:52', 129, 1, 'Task Upload'),
(83, 127, 69, '2022-03-13 21:40:52', 128, 1, 'Task Upload'),
(84, 129, 71, '2022-03-13 23:45:58', 127, 1, 'New Task'),
(85, 129, 71, '2022-03-13 23:45:58', 135, 0, 'New Task'),
(86, 129, 71, '2022-03-13 23:45:58', 136, 0, 'New Task'),
(87, 127, 71, '2022-03-13 23:47:06', 129, 1, 'Task Upload'),
(88, 127, 71, '2022-03-13 23:47:06', 128, 1, 'Task Upload'),
(89, 129, 71, '2022-03-13 23:50:52', 155, 1, 'Task Forward');

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
  `UploadedByID` int(11) DEFAULT NULL,
  `Share_to_user` varchar(100) DEFAULT NULL,
  `Share_to_group` int(11) DEFAULT NULL,
  `DeadLine` datetime DEFAULT NULL,
  `Revision` int(11) DEFAULT NULL,
  `DateUploaded` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `block_doc_json` longtext DEFAULT NULL,
  `status` int(11) NOT NULL,
  `pinned` int(11) NOT NULL,
  `taskID` int(11) NOT NULL,
  `FilePathName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `files`
--

INSERT INTO `files` (`FileID`, `FileName`, `FileType`, `FileSize`, `FileContentType`, `UploadedByID`, `Share_to_user`, `Share_to_group`, `DeadLine`, `Revision`, `DateUploaded`, `block_doc_json`, `status`, `pinned`, `taskID`, `FilePathName`) VALUES
(158, 'vaccination_certificate.pdf', 'pdf', 1, 'application/pdf', 133, NULL, 1, NULL, 1, '2022-03-12 18:14:24', NULL, 0, 0, 67, '133vaccination_certificate.pdf'),
(160, '121121CCMS_Indorsement-Capstone-Thesis.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 127, NULL, 1, NULL, 1, '2022-03-12 19:42:03', NULL, 0, 0, 67, '127121121CCMS_Indorsement-Capstone-Thesis.docx'),
(161, '121121CCMS_Indorsement-Capstone-Thesis.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 136, NULL, 1, NULL, 1, '2022-03-13 10:42:16', NULL, 0, 0, 67, '136121121CCMS_Indorsement-Capstone-Thesis.docx'),
(162, '121121CCMS_Indorsement-Capstone-Thesis.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 127, NULL, 1, NULL, 1, '2022-03-13 21:14:34', NULL, 0, 0, 70, '127121121CCMS_Indorsement-Capstone-Thesis.docx'),
(163, 'APPLICATION FORM.DOCX', 'DOCX', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 133, NULL, 1, NULL, 1, '2022-03-13 21:16:17', NULL, 0, 0, 70, '133APPLICATION FORM.DOCX'),
(164, 'APPLICATION FORM.DOCX', 'DOCX', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 127, NULL, 1, NULL, 1, '2022-03-13 21:40:52', NULL, 0, 0, 69, '127APPLICATION FORM.DOCX'),
(165, '121121CCMS_Indorsement-Capstone-Thesis.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 127, NULL, 1, NULL, 1, '2022-03-13 23:47:06', NULL, 0, 0, 71, '127121121CCMS_Indorsement-Capstone-Thesis.docx');

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
(1, 'Admin'),
(2, 'District Supervisor'),
(5, 'Principal'),
(39, 'Teacher 1'),
(40, 'Teacher 2'),
(41, 'Teacher 3'),
(42, 'Teacher 4'),
(43, 'Teacher 5'),
(44, 'Teacher 6'),
(45, 'Grade Chairman 1'),
(46, 'Grade Chairman 2'),
(47, 'Grade Chairman 3'),
(48, 'Grade Chairman 4'),
(49, 'Grade Chairman 5'),
(50, 'Grade Chairman 6');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `TaskID` int(11) NOT NULL,
  `TaskName` varchar(100) NOT NULL,
  `TaskImage` longblob NOT NULL,
  `TaskCreatedBy` int(11) NOT NULL,
  `TaskDateCreated` datetime NOT NULL,
  `TaskDeadline` datetime NOT NULL,
  `TaskDescription` text NOT NULL,
  `TaskStatus` varchar(100) NOT NULL,
  `TaskSchedule` varchar(50) NOT NULL,
  `GC_Status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`TaskID`, `TaskName`, `TaskImage`, `TaskCreatedBy`, `TaskDateCreated`, `TaskDeadline`, `TaskDescription`, `TaskStatus`, `TaskSchedule`, `GC_Status`) VALUES
(67, 'test', '', 129, '2022-03-12 17:15:49', '2022-03-08 17:15:00', 'test', 'Pending Teachers', 'Weekly', ''),
(69, 'test123', '', 129, '2022-03-12 17:22:01', '2022-03-16 17:21:00', 'test123', 'Pending Teachers', 'Weekly', ''),
(70, 'asdasd', '', 129, '2022-03-13 21:13:41', '2022-03-20 21:13:00', 'test 123123123123', 'Pending Teachers', 'Weekly', ''),
(71, 'Test Task', '', 129, '2022-03-13 23:45:58', '2022-03-20 23:45:00', 'test 123', 'Pending Teachers', 'Weekly', '');

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
  `PhoneNumber` varchar(100) NOT NULL,
  `Position` int(12) NOT NULL,
  `DateCreated` datetime NOT NULL DEFAULT current_timestamp(),
  `profilePic` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Email`, `Pass`, `FirstName`, `LastName`, `PhoneNumber`, `Position`, `DateCreated`, `profilePic`) VALUES
(82, 'admin@gmail.com', '89805776bf3dbcf0bad0bce14704d89eccde55cef2cd7cf6f068010d2ceb9480', 'Paul Ian', 'Masendo', '+639751160135', 1, '2021-11-18 08:36:42', '/static/uploads/ProfilePictures/82_47.jpg'),
(127, 'teacher1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher', 'One', '+631234567890', 39, '2022-03-12 16:40:06', ''),
(128, 'gradeChairmanOne@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman', '+631234567890', 45, '2022-03-12 16:40:28', '/static/uploads/ProfilePictures/128_85.jpg'),
(129, 'principal@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Principal', 'User', '+631234567890', 5, '2022-03-12 16:40:47', ''),
(133, 'teacher2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'two', '+631234567890', 40, '2022-03-12 18:12:47', ''),
(134, 'gradeChairman2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman', '+631234567890', 46, '2022-03-12 18:13:01', ''),
(135, 'teacher1-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher', 'Account', '+631234567890', 39, '2022-03-12 23:34:05', ''),
(136, 'teacher1-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher', 'One three', '+631234567890', 39, '2022-03-12 23:34:18', ''),
(137, 'teacher2-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher', 'Account', '+631234567890', 40, '2022-03-12 23:34:34', ''),
(138, 'teacher2-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'two', '+631234567890', 40, '2022-03-12 23:34:49', ''),
(139, 'teacher3-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher three', 'two', '+631234567890', 41, '2022-03-12 23:36:23', ''),
(140, 'teacher3-1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher Three', 'One', '+631234567890', 41, '2022-03-12 23:37:12', ''),
(141, 'teacher3-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'three three', '+631234567890', 41, '2022-03-13 10:21:36', ''),
(142, 'teacher4-1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'four-one', '+631234567890', 42, '2022-03-13 10:22:29', ''),
(143, 'teacher4-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'four-two', '+631234567890', 42, '2022-03-13 10:22:57', ''),
(144, 'teacher4-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'four-three', '+631234567890', 42, '2022-03-13 10:28:30', ''),
(145, 'teacher5-1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'five-one', '+631234567890', 43, '2022-03-13 10:30:40', ''),
(146, 'teacher5-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'five-two', '+631234567890', 43, '2022-03-13 10:31:05', ''),
(147, 'teacher5-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'five-two', '+631234567890', 43, '2022-03-13 10:31:55', ''),
(148, 'teacher6-1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'six-one', '+631234567890', 44, '2022-03-13 10:32:20', ''),
(149, 'teacher6-2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'six-two', '+631234567890', 44, '2022-03-13 10:36:14', ''),
(150, 'teacher6-3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'six-three', '+631234567890', 44, '2022-03-13 10:37:16', ''),
(151, 'gradeChairman3@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman 3', '+631234567890', 47, '2022-03-13 10:37:40', ''),
(152, 'gradeChairman4@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman4', '+631234567890', 48, '2022-03-13 10:37:57', ''),
(153, 'gradeChairman5@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman5', '+631234567890', 49, '2022-03-13 10:40:19', ''),
(154, 'gradeChairman6@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman6', '+631234567890', 50, '2022-03-13 10:40:55', ''),
(155, 'districtSupervisor@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'District', 'Supervisor', '+631234567890', 2, '2022-03-13 21:34:54', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`EventID`);

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
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`TaskID`);

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
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `EventID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;

--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `FileID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=166;

--
-- AUTO_INCREMENT for table `position`
--
ALTER TABLE `position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `TaskID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=156;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
