-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 12, 2022 at 03:13 PM
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
(1, 94, 137, '2022-02-12 19:25:00', 95, 0, 'File'),
(2, 93, 138, '2022-02-12 20:34:06', 95, 0, 'File'),
(3, 95, 139, '2022-02-12 20:59:59', 93, 0, 'File');

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
(111, 'comments-Copy.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 91, NULL, 1, NULL, 1, '2022-02-06 10:05:05', NULL, 0, 0, 49, '91comments-Copy.docx'),
(112, 'weconnect (3).sql', 'sql', 1, 'application/octet-stream', 91, 'paulian829@gmail.com', 1, NULL, 1, '2022-02-06 10:05:23', NULL, 0, 0, 0, '91weconnect (3).sql'),
(120, 'comments-Copy.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 95, NULL, 1, NULL, 1, '2022-02-06 23:37:19', NULL, 0, 0, 49, '95comments-Copy.docx'),
(121, 'comments-Copy.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 95, NULL, 1, NULL, 1, '2022-02-06 23:40:50', NULL, 0, 0, 50, '95comments-Copy.docx'),
(122, 'winrar-x64-610.exe', 'exe', 1, 'application/x-msdownload', 93, 'paulian829@gmail.com', 1, NULL, 1, '2022-02-07 08:04:46', NULL, 0, 0, 0, '93winrar-x64-610.exe'),
(123, 'comments-Copy.docx', 'docx', 1, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 95, NULL, 1, NULL, 1, '2022-02-07 23:30:37', NULL, 0, 0, 51, '95comments-Copy.docx'),
(124, 'database.py', 'py', 1, 'text/plain', 94, 'username@paul', 1, NULL, 1, '2022-02-12 18:53:36', NULL, 0, 0, 0, '94database.py'),
(125, 'package-lock.json', 'json', 1, 'application/json', 94, 'username@paul', 1, NULL, 1, '2022-02-12 18:55:08', NULL, 0, 0, 0, '94package-lock.json'),
(126, 'package.json', 'json', 1, 'application/json', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:15:05', NULL, 0, 0, 0, '94package.json'),
(127, 'package.json', 'json', 1, 'application/json', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:15:59', NULL, 0, 0, 0, '94package.json'),
(128, '.gitignore', 'gitignore', 1, 'text/plain', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:16:19', NULL, 0, 0, 0, '94.gitignore'),
(129, '.gitignore', 'gitignore', 1, 'text/plain', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:19:21', NULL, 0, 0, 0, '94.gitignore'),
(130, '.gitignore', 'gitignore', 1, 'text/plain', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:19:44', NULL, 0, 0, 0, '94.gitignore'),
(131, 'database.py', 'py', 1, 'text/plain', 94, 'teacher@gmail.com', 1, NULL, 1, '2022-02-12 19:20:53', NULL, 0, 0, 0, '94database.py'),
(132, '.gitignore', 'gitignore', 1, 'text/plain', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:22:10', NULL, 0, 0, 0, '94.gitignore'),
(133, 'package.json', 'json', 1, 'application/json', 94, 'username@paul', 1, NULL, 1, '2022-02-12 19:22:57', NULL, 0, 0, 0, '94package.json'),
(134, 'package.json', 'json', 1, 'application/json', 94, 'username@paul', 1, NULL, 1, '2022-02-12 19:23:19', NULL, 0, 0, 0, '94package.json'),
(135, 'package-lock.json', 'json', 1, 'application/json', 94, 'paulian829@gmail.com', 1, NULL, 1, '2022-02-12 19:23:57', NULL, 0, 0, 0, '94package-lock.json'),
(136, 'package-lock.json', 'json', 1, 'application/json', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:24:29', NULL, 0, 0, 0, '94package-lock.json'),
(137, 'flask_app.py', 'py', 1, 'text/plain', 94, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 19:25:00', NULL, 0, 0, 0, '94flask_app.py'),
(138, 'pyvenv.cfg', 'cfg', 1, 'application/octet-stream', 93, 'teacher1@gmail.com', 1, NULL, 1, '2022-02-12 20:34:06', NULL, 0, 0, 0, '93pyvenv.cfg'),
(139, 'flask.exe', 'exe', 1, 'application/x-msdownload', 95, 'principal@gmail.com', 1, NULL, 1, '2022-02-12 20:59:59', NULL, 0, 0, 0, '95flask.exe');

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
(5, 'Principal');

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
  `TaskSchedule` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`TaskID`, `TaskName`, `TaskImage`, `TaskCreatedBy`, `TaskDateCreated`, `TaskDeadline`, `TaskDescription`, `TaskStatus`, `TaskSchedule`) VALUES
(49, 'Individual daily log and accomplishment report (IDLAR)', '', 82, '2021-12-30 22:04:16', '2022-02-12 22:03:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending Principal', 'Weekly'),
(50, 'Weekly Assesment', '', 82, '2022-01-06 22:39:41', '2022-02-19 22:39:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending Principal', 'Weekly'),
(51, 'Weekly home learning plan', '', 82, '2022-01-06 22:49:33', '2022-01-15 22:49:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending Principal', 'Weekly'),
(52, 'Idea lesson exemplar', '', 82, '2022-01-06 22:50:04', '2022-01-15 22:49:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', 'Pending Teachers', 'Weekly'),
(53, 'Form 148 of the Daily Time record (DTR)', '', 82, '2022-01-06 22:51:36', '2022-01-29 22:51:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending Teachers', 'Monthly'),
(54, 'Students’ grades', '', 82, '2022-01-06 22:52:00', '2022-01-23 22:51:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending District Supervisor', 'Quarterly'),
(55, 'Number of enrollment and number of drop out', '', 82, '2022-01-06 23:26:14', '2022-03-05 23:25:00', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'Pending District Supervisor', 'Quarterly'),
(60, 'test123', '', 93, '2022-02-02 23:34:53', '2022-02-06 23:34:00', 'test123', 'Done', 'Monthly');

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
(82, 'admin@gmail.com', '89805776bf3dbcf0bad0bce14704d89eccde55cef2cd7cf6f068010d2ceb9480', 'admin1', 'account', '+639751160135', 1, '2021-11-18 08:36:42', '/static/uploads/ProfilePictures/82_2874.png'),
(86, 'weconnect.thesis@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Super', '2', '+639071882953', 1, '2021-11-22 00:17:06', '/static/uploads/ProfilePictures/86_18.jpg'),
(91, 'teacher@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher5', 'Account1', '+639071882953', 4, '2021-12-21 10:27:00', '/static/uploads/ProfilePictures/91_18.jpg'),
(93, 'principal@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Principal', 'User', '+639071882953', 5, '2021-12-30 10:58:31', '/static/uploads/ProfilePictures/93_47.jpg'),
(94, 'districtsupervisor@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'District', 'Supervisor', '+639071882953', 2, '2021-12-30 10:59:02', '/static/uploads/ProfilePictures/94_52.jpg'),
(95, 'teacher1@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Teacher', 'One', '+639071882953', 4, '2021-12-30 11:02:07', '/static/uploads/ProfilePictures/95_66.jpg'),
(96, 'teacher2@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'teacher', 'two', '+639071882953', 4, '2021-12-30 11:02:33', '/static/uploads/ProfilePictures/96_85.jpg'),
(97, 'gradeChairman@gmail.com', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Grade', 'Chairman', '+639071882953', 3, '2021-12-31 12:29:37', '/static/uploads/ProfilePictures/97_33.jpg'),
(99, 'cp.merene@mseuf.edu.ph', 'cbdc324449652371c3ee4253adc7fc2c0403185a8f824d31e545a3a58db1935b', 'Camille', 'Panaligan', '+639463370901', 2, '2022-02-05 16:09:22', '/static/uploads/ProfilePictures/99_85.jpg');

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
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `EventID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `FileID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;

--
-- AUTO_INCREMENT for table `position`
--
ALTER TABLE `position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `TaskID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=120;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
