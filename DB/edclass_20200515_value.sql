-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2020 at 12:36 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.3

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `edclass`
--

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(38, 'room', 'edchangepass'),
(7, 'room', 'edcoach'),
(37, 'room', 'edcoachfile'),
(16, 'room', 'edcolla'),
(39, 'room', 'edcollafile'),
(40, 'room', 'edcollaopengraph'),
(41, 'room', 'edcollareply'),
(36, 'room', 'edcoteacher'),
(8, 'room', 'edcourse'),
(35, 'room', 'edenrolment'),
(9, 'room', 'edgroup'),
(34, 'room', 'edgroupmember'),
(10, 'room', 'edlevel'),
(33, 'room', 'edlive'),
(32, 'room', 'edlog'),
(11, 'room', 'edmember'),
(12, 'room', 'edpost'),
(31, 'room', 'edpostfile'),
(30, 'room', 'edreply'),
(13, 'room', 'edresource'),
(29, 'room', 'edresourcefile'),
(28, 'room', 'edresourceopengraph'),
(14, 'room', 'edscaffolding'),
(27, 'room', 'edscaffoldingfile'),
(15, 'room', 'edscaffoldingtype'),
(26, 'room', 'edsocialfile'),
(25, 'room', 'edsocialopengraph'),
(24, 'room', 'edsublevel'),
(42, 'room', 'edsubtask'),
(43, 'room', 'edsubtaskfile'),
(17, 'room', 'edtask'),
(23, 'room', 'edtaskfile'),
(22, 'room', 'edtaskopengraph'),
(18, 'room', 'edturnedin'),
(21, 'room', 'edturnedinfile'),
(20, 'room', 'edturnedinopengraph'),
(19, 'room', 'edusertype'),
(6, 'sessions', 'session');

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-05-13 17:33:29.870403'),
(2, 'auth', '0001_initial', '2020-05-13 17:33:30.028010'),
(3, 'admin', '0001_initial', '2020-05-13 17:33:30.535500'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-05-13 17:33:30.649804'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-05-13 17:33:30.656523'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-05-13 17:33:30.709273'),
(7, 'auth', '0002_alter_permission_name_max_length', '2020-05-13 17:33:30.812006'),
(8, 'auth', '0003_alter_user_email_max_length', '2020-05-13 17:33:30.867206'),
(9, 'auth', '0004_alter_user_username_opts', '2020-05-13 17:33:30.874181'),
(10, 'auth', '0005_alter_user_last_login_null', '2020-05-13 17:33:30.919804'),
(11, 'auth', '0006_require_contenttypes_0002', '2020-05-13 17:33:30.922807'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2020-05-13 17:33:30.930566'),
(13, 'auth', '0008_alter_user_username_max_length', '2020-05-13 17:33:30.950655'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2020-05-13 17:33:30.965311'),
(15, 'auth', '0010_alter_group_name_max_length', '2020-05-13 17:33:31.044079'),
(16, 'auth', '0011_update_proxy_permissions', '2020-05-13 17:33:31.051923'),
(17, 'room', '0001_initial', '2020-05-13 17:33:33.118562'),
(18, 'sessions', '0001_initial', '2020-05-13 17:33:34.904737'),
(19, 'room', '0002_auto_20200513_1810', '2020-05-13 18:10:47.779573'),
(20, 'room', '0003_edcollafile_edcollaopengraph', '2020-05-13 18:12:16.550322'),
(21, 'room', '0004_auto_20200513_2343', '2020-05-13 23:43:41.368781'),
(22, 'room', '0005_edcolla_group', '2020-05-13 23:45:50.631804'),
(23, 'room', '0006_edcollareply', '2020-05-14 13:31:25.086678'),
(24, 'room', '0007_edsubtask_edsubtaskfile', '2020-05-15 17:34:47.691829');

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('44ebm7j4rw6j90cxudighrxpqhwwqq0g', 'OGVjNGM5YmM3MDIwNjE3ZTFjMTBjYzVmNjQ2YWZhODg4MGM0ZWI3Yzp7fQ==', '2020-05-27 20:48:31.059023'),
('tsmy5es5bs8lzhc4d86zcqnz9k5trzt2', 'NjVjNzBmYTA2ZjY2OGE4YmUwNTZiNWQyZDFiMTI2YWM5Y2E5NWVhOTp7ImVtYWlsIjoiMTIzNEBnbWFpbC5jb20iLCJ0eXBlIjoiU1RVREVOVCJ9', '2020-05-29 16:44:47.391609'),
('vhtho07us9cgss6a774e94wrgotkacgc', 'NjVjNzBmYTA2ZjY2OGE4YmUwNTZiNWQyZDFiMTI2YWM5Y2E5NWVhOTp7ImVtYWlsIjoiMTIzNEBnbWFpbC5jb20iLCJ0eXBlIjoiU1RVREVOVCJ9', '2020-05-28 16:02:30.826815'),
('zw962if4cy6vdenpzl0tyatuhge4zcq4', 'OGU4MDkxNTMyOGEzYWNiOWZmMTk1ODg2MDU1MjczMTYyYzhhZjIyNjp7ImVtYWlsIjoidGVhY2hlckBnbWFpbC5jb20iLCJ0eXBlIjoiVEVBQ0hFUiJ9', '2020-05-27 17:45:53.907027');

--
-- Dumping data for table `ed_coach`
--

INSERT INTO `ed_coach` (`id`, `name`, `email`, `status`, `timestamp`, `task_id`, `teacher_id`) VALUES
(1, 'ผอ จำรัส  หรรษาวงศ์', '', 'ACTIVE', '2020-04-28 17:20:39.129660', 7, 32),
(2, 'asasd', '', 'ACTIVE', '2020-04-28 17:21:43.120846', 6, 32);

--
-- Dumping data for table `ed_coach_file`
--

INSERT INTO `ed_coach_file` (`id`, `file_name`, `file_link`, `file_type`, `status`, `timestamp`, `coach_id`) VALUES
(1, 'coach.jpg', '/uploads/course_id_2/coach/files/2020-04-28/coach.jpg', 'image/png', 'ACTIVE', '2020-04-28 17:20:28.000308', 1),
(2, 'coach.jpg', '/uploads/course_id_2/coach/files/2020-04-28/coach_m1G9QEg.jpg', 'image/png', 'ACTIVE', '2020-04-28 17:21:42.158990', 2);

--
-- Dumping data for table `ed_colla`
--

INSERT INTO `ed_colla` (`id`, `description`, `status`, `timestamp`, `task_id`, `member_id`, `group_id`) VALUES
(1, 'asdasd', 'DELETE', '2020-04-27 11:41:37.019551', 6, 32, NULL),
(2, 'aaaaa', 'DELETE', '2020-04-27 11:45:15.647640', 6, 32, NULL),
(3, '', 'DELETE', '2020-04-27 11:45:58.822854', 6, 32, NULL),
(4, '', 'DELETE', '2020-04-27 11:46:38.751696', 6, 32, NULL),
(5, 'asasd', 'DELETE', '2020-04-27 12:02:24.797206', 6, 32, NULL),
(6, 'asdasdasd', 'DELETE', '2020-04-27 12:02:27.521769', 6, 32, NULL),
(7, '', 'DELETE', '2020-04-27 13:31:15.711423', 6, 32, NULL),
(8, '', 'DELETE', '2020-04-27 13:31:33.848635', 6, 32, NULL),
(9, '<a href=\"https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables\" target=\"_blank\"><a href=\"https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables\" target=\"_blank\">https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables</a>https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables</a><div><br></div><div><br></div><div><a href=\"https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables\" target=\"_blank\">https://getbootstrap.com/docs/4.5/content/tables/#responsive-tables</a><br></div>', 'ACTIVE', '2020-05-13 23:47:27.708112', 6, 32, 3),
(11, '', 'DELETE', '2020-05-14 00:04:32.240392', 6, 32, 1),
(12, '', 'DELETE', '2020-05-14 00:05:33.812337', 6, 32, 1),
(13, '', 'DELETE', '2020-05-14 00:06:00.804815', 6, 32, 1),
(14, '', 'DELETE', '2020-05-14 13:26:06.982618', 6, 32, 1),
(15, 'ทดสอบ<div><br></div>', 'ACTIVE', '2020-05-14 13:58:05.452249', 6, 32, 3),
(16, '<a href=\"stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url\" target=\"_blank\">stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url</a>', 'DELETE', '2020-05-14 14:21:47.113725', 6, 32, 1),
(17, '<a href=\"http://boxicons.com\" target=\"_blank\">boxicons.com</a>', 'ACTIVE', '2020-05-14 14:25:35.197682', 6, 32, 1),
(18, 'asdasd', 'DELETE', '2020-05-14 15:54:43.718662', 6, 32, NULL),
(19, '', 'DELETE', '2020-05-14 15:58:09.744658', 6, 32, NULL),
(20, 'asdasd', 'DELETE', '2020-05-14 21:08:04.815531', 6, 31, NULL),
(21, 'asdasdasd', 'DELETE', '2020-05-14 21:08:18.739785', 6, 31, NULL),
(22, 'asdasdasdasd', 'DELETE', '2020-05-14 21:15:48.277559', 6, 32, NULL),
(23, 'rrrrrr', 'DELETE', '2020-05-14 21:16:16.455323', 6, 32, NULL),
(24, 'asdasd<div><br></div>', 'DELETE', '2020-05-14 21:18:20.012580', 6, 32, NULL),
(25, 'asdasdsad', 'ACTIVE', '2020-05-14 21:25:53.844991', 6, 31, NULL),
(26, 'asdasdasd', 'ACTIVE', '2020-05-15 17:07:31.216292', 6, 31, 3);

--
-- Dumping data for table `ed_colla_file`
--

INSERT INTO `ed_colla_file` (`id`, `file_name`, `file_link`, `file_type`, `status`, `timestamp`, `colla_id`) VALUES
(2, 'DSCF2249.JPG', '/uploads/course_id_2/collaborations/files/2020-05-14/DSCF2249.JPG', 'image/jpeg', 'ACTIVE', '2020-05-14 00:04:30.815296', 13),
(3, 'DSCF2249.JPG', '/uploads/course_id_2/collaborations/files/2020-05-14/DSCF2249_rdLH79b.JPG', 'image/jpeg', 'ACTIVE', '2020-05-14 13:26:04.423759', 14),
(4, 'แผ่นพับ-2-g2.jpg', '/uploads/course_id_2/collaborations/files/2020-05-14/%E0%B9%81%E0%B8%9C%E0%B9%88%E0%B8%99%E0%B8%9E%E0%B8%B1%E0%B8%9A-2-g2.jpg', 'image/jpeg', 'ACTIVE', '2020-05-14 15:57:44.032111', NULL),
(5, 'แผ่นพับ-2-g2.jpg', '/uploads/course_id_2/collaborations/files/2020-05-14/%E0%B9%81%E0%B8%9C%E0%B9%88%E0%B8%99%E0%B8%9E%E0%B8%B1%E0%B8%9A-2-g2.jpg', 'image/jpeg', 'ACTIVE', '2020-05-14 15:58:08.757303', 19),
(6, 'DSCF2249.JPG', '/uploads/course_id_2/collaborations/files/2020-05-15/DSCF2249.JPG', 'image/jpeg', 'ACTIVE', '2020-05-15 17:07:27.257184', 26);

--
-- Dumping data for table `ed_colla_reply`
--

INSERT INTO `ed_colla_reply` (`id`, `description`, `status`, `timestamp`, `colla_id`, `member_id`) VALUES
(1, 'asfaas', 'ACTIVE', '2020-05-14 15:32:14.792278', 17, 32),
(2, 'asdasd<br><br>KKK', 'ACTIVE', '2020-05-14 15:32:20.910565', 17, 32),
(3, 'aasdsaadddddddddddddddddddddddddddddddddddddddd', 'ACTIVE', '2020-05-14 15:32:58.740415', 17, 32),
(4, 'ทดสอบแทรกลิงก์&nbsp;<a href=\"http://boxicons.com\" target=\"_blank\">boxicons.com</a>', 'ACTIVE', '2020-05-14 15:33:27.802711', 15, 32),
(5, '<a href=\"http://https://boxicons.com/\" target=\"_blank\">https://boxicons.com/</a>', 'ACTIVE', '2020-05-14 15:35:50.840823', 15, 32),
(6, '<a href=\"https://boxicons.com/\" target=\"_blank\">https://boxicons.com/</a>', 'ACTIVE', '2020-05-14 15:40:51.526079', 15, 32),
(7, 'ทดสอบการคอมเมนต์', 'ACTIVE', '2020-05-14 15:55:17.376270', 18, 32);

--
-- Dumping data for table `ed_course`
--

INSERT INTO `ed_course` (`id`, `course_name`, `description`, `cover_pic`, `uid`, `status`, `timestamp`, `catagory_id`, `teacher_id`) VALUES
(2, 'ทดสอบห้องเรียน', 'ss', '/uploads/course_id_2/cover/cover_EEkZrW0.jpg', 'VtzLq', 'ACTIVE', '2020-04-23 00:39:21.731632', 5, 32),
(3, 'adasdasd', 'asdasd', '/uploads/0/cover/cover1.png', 'xoWzf', 'ACTIVE', '2020-04-28 12:42:37.737051', 5, 32);

--
-- Dumping data for table `ed_enrolment`
--

INSERT INTO `ed_enrolment` (`id`, `timestamp`, `course_id`, `member_id`) VALUES
(1, '0000-00-00 00:00:00.000000', 2, 31),
(2, '2020-04-25 11:25:05.000000', 2, 30),
(6, '2020-04-28 12:55:10.614034', 3, 31);

--
-- Dumping data for table `ed_group`
--

INSERT INTO `ed_group` (`id`, `title`, `timestamp`, `status`, `task_id`) VALUES
(1, 'กลุ่มที่ 1', '2020-05-13 17:46:12.377162', 'ACTIVE', 6),
(2, 'กลุ่มที่ 2', '2020-05-13 17:47:43.255640', 'DELETE', 6),
(3, 'กลุ่มที่ 2', '2020-05-13 18:18:58.281042', 'ACTIVE', 6);

--
-- Dumping data for table `ed_group_member`
--

INSERT INTO `ed_group_member` (`id`, `timestamp`, `group_id`, `member_id`) VALUES
(1, '2020-05-13 17:46:12.380106', 1, 30),
(2, '2020-05-13 17:47:43.258174', 2, 31),
(3, '2020-05-13 18:18:58.284015', 3, 31);

--
-- Dumping data for table `ed_level`
--

INSERT INTO `ed_level` (`id`, `prefix`, `title`) VALUES
(1, 'Primary', 'ต่ำกว่าอุดมศึกษา'),
(2, 'Higer', 'อุดมศึกษา');

--
-- Dumping data for table `ed_live`
--

INSERT INTO `ed_live` (`id`, `url`, `password`, `platform`, `status`, `timestamp`, `course_id`, `teacher_id`) VALUES
(1, 'asdasdasd', NULL, 'meet', 'ACTIVE', '2020-04-25 16:15:01.981229', 2, 32),
(2, 'adasdasd', 'aaaa', 'zoom', 'ACTIVE', '2020-04-25 16:15:09.679409', 2, 32);

--
-- Dumping data for table `ed_log`
--

INSERT INTO `ed_log` (`id`, `ip`, `device`, `location`, `timestamp`, `ed_member_id`) VALUES
(1, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:24:59.332585', 31),
(2, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:31:18.256763', 31),
(3, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:32:55.539572', 31),
(4, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:33:38.608237', 31),
(5, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:33:57.486967', 31),
(6, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 22:56:55.882759', 31),
(7, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-21 23:26:13.514338', 31),
(8, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-22 21:07:05.456746', 31),
(9, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-22 21:20:55.519508', 31),
(10, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-22 21:24:36.585374', 31),
(11, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-22 22:46:20.927685', 32),
(12, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-23 02:15:40.204723', 32),
(13, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-23 05:29:58.409862', 32),
(14, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-25 09:31:52.408243', 32),
(15, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-25 09:37:45.734979', 32),
(16, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-25 17:55:28.058513', 33),
(17, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-25 17:55:41.328232', 32),
(18, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-26 05:56:21.801471', 31),
(19, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-26 05:59:09.130363', 32),
(20, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-26 20:31:19.649121', 32),
(21, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 12:10:35.481378', 31),
(22, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 12:11:12.468968', 31),
(23, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 12:41:58.294191', 32),
(24, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 12:43:09.824531', 31),
(25, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 14:06:52.121603', 32),
(26, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-28 16:34:16.707020', 31),
(27, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-05-13 17:45:53.897100', 32),
(28, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-05-13 20:47:00.468430', 33),
(29, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-05-13 20:47:13.712543', 31),
(30, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-05-14 16:02:30.821840', 31),
(31, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-05-15 16:44:47.381235', 31);

--
-- Dumping data for table `ed_member`
--

INSERT INTO `ed_member` (`id`, `password`, `firstname`, `lastname`, `email`, `picture`, `timestamp`, `status`, `catagory_id`, `user_type_id`) VALUES
(30, '0ea46fdf7fc44bcfb17abc9af0b039d0', 'asdasdasd@hotmail.com', 'asdasdasd@hotmail.com', 'asdasdasd@hotmail.com', '/uploads/0/img/user.png', '2020-04-21 09:14:56.727157', 'ACTIVE', 1, 1),
(31, '81dc9bdb52d04dc20036dbd8313ed055', 'ปรมินทร์', 'อัตตะเนย์', '1234@gmail.com', '/uploads/0/img/user.png', '2020-04-21 21:53:41.440061', 'ACTIVE', 5, 1),
(32, '8d788385431273d11e8b43bb78f3aa41', 'teacher', 'Fame', 'teacher@gmail.com', '/uploads/member_id_32/picture/2020-04-25/profile.jpg', '2020-04-22 22:46:07.087709', 'ACTIVE', 1, 2),
(33, '698d51a19d8a121ce581499d7b701668', '1111', '1111', '111@gmail.com', '/uploads/0/img/user.png', '2020-04-25 17:55:20.470325', 'ACTIVE', 5, 1);

--
-- Dumping data for table `ed_post`
--

INSERT INTO `ed_post` (`id`, `description`, `timestamp`, `status`, `course_id`, `member_id`) VALUES
(67, 'asdsad', '2020-04-26 20:32:02.555922', 'ACTIVE', 2, 32);

--
-- Dumping data for table `ed_reply`
--

INSERT INTO `ed_reply` (`id`, `description`, `status`, `timestamp`, `member_id`, `post_id`) VALUES
(1, 'บทความนี้เล่านิยายกำลังภายในที่โด่งดังที่สุดเรื่องหนึ่งของโกวเล้ง “ฤทธิ์มีดสั้น” ที่จอมยุทธแต่ละคนมีสโลแกนประจำตัวคล้าย personal branding และมีการจัดอันดับในตำราอาวุธ เหมือนการจัด ranking\r\nไม่น่าแปลกใจที่มีผู้อ่านบทความนี้จำนวนมาก เพราะเป็นเรื่องของนิยายกำลังภายในที่คนส่วนใหญ่รู้จักดี แต่เขียนให้เข้ากับยุคสมัยใหม่ครับ', 'ACTIVE', '2020-04-24 14:54:43.000000', 32, 36),
(2, 'เข้าสู่กระบวนการ', 'ACTIVE', '2020-04-24 08:39:32.957878', 32, 36),
(3, 'lll', 'ACTIVE', '2020-04-24 11:18:54.322292', 32, 48),
(4, 'ทดสอบการตอบ', 'ACTIVE', '2020-04-28 17:05:36.100861', 32, 67),
(5, 'ตอบด้วยคร้าบ', 'ACTIVE', '2020-04-28 17:08:11.096213', 31, 67);

--
-- Dumping data for table `ed_resource`
--

INSERT INTO `ed_resource` (`id`, `description`, `status`, `timestamp`, `task_id`, `teacher_id`) VALUES
(4, 'asdasdasd', 'DELETE', '2020-04-27 06:38:57.464787', 6, 32),
(5, '', 'ACTIVE', '2020-04-27 06:39:06.589226', 6, 32),
(7, '<div><a href=\"https://drive.google.com/drive/u/2/folders/1wk45N-vMj1-Pxqdb5JJmL0S54QWx9Ul1\" target=\"_blank\">https://drive.google.com/drive/u/2/folders/1wk45N-vMj1-Pxqdb5JJmL0S54QWx9Ul1</a><br><div><br></div></div>', 'DELETE', '2020-04-27 10:01:11.651800', 6, 32),
(8, 'ppppppppppppppppasd', 'DELETE', '2020-04-27 11:40:00.551929', 6, 32),
(9, 'asdasd', 'DELETE', '2020-04-27 11:40:40.902291', 6, 32),
(10, '<a href=\"http://boxicons.com\" target=\"_blank\">boxicons.com</a>\n                              \n                            <div><br></div>', 'ACTIVE', '2020-05-14 14:26:58.626048', 6, 32);

--
-- Dumping data for table `ed_resource_opengraph`
--

INSERT INTO `ed_resource_opengraph` (`id`, `title`, `description`, `url`, `image`, `resource_id`) VALUES
(18, 'โรงเรียนโพนงามพิทยานุกูล อำเภอโกสุมพิสัย จังหวัดมหาสารคาม', 'ประกาศการรับสมัครนักเรียน ม.1 และ ม.4 ประจำปีการศึกษา 2563\nเนื่องจากสถานการณ์การแพร่ระบาดของเชื้อไวรัสโคโรนา 2019 (COVID - 19) โรงเรียนโพนงามพิทยานุกูล จึงเลื่อนวันรับสมัครเป็นวันที่ 3 พ.ค. 2563 - 12...', 'https://www.facebook.com/phonngampittayanukul/posts/1284324348423936', 'https://scontent.fnak1-1.fna.fbcdn.net/v/t1.0-9/94429664_1284324231757281_279897263424143360_o.jpg?_nc_cat=111&_nc_sid=8024bb&_nc_ohc=v4YsdxJSgpEAX9jIhge&_nc_ht=scontent.fnak1-1.fna&oh=b7dd82b95c45fcc56411b56e61ce9f55&oe=5ECD734B', 5),
(28, 'Why does urllib.request.urlopen sometimes does not work, but browsers work?', 'I am trying to download some content using Python\'s urllib.request. The following command yields an exception:\n\nimport urllib.request\nprint(urllib.request.urlopen(\"https://fpgroup.foreignpolicy.com/', 'https://stackoverflow.com/questions/41469938/why-does-urllib-request-urlopen-sometimes-does-not-work-but-browsers-work', 'https://cdn.sstatic.net/Sites/stackoverflow/img/apple-touch-icon@2.png?v=73d79a89bded', NULL),
(30, 'SECRET vs OG SEED - EU Division - WePlay! Pushka League DOTA 2', 'Tournaments, esports news, everything WePlay! https://bit.ly/2VT13ov Commentary by TobiWan Pieliedie ►Watch the games live here: https://www.twitch.tv/weplay...', 'https://www.youtube.com/watch?v=kuFsMwpWh2c', 'https://i.ytimg.com/vi/kuFsMwpWh2c/maxresdefault.jpg', NULL);

--
-- Dumping data for table `ed_scaffolding`
--

INSERT INTO `ed_scaffolding` (`id`, `description`, `status`, `timestamp`, `scaff_type_id`, `task_id`, `teacher_id`) VALUES
(1, 'lkkjljsdf', 'DELETE', '2020-04-27 13:32:48.438303', 1, 6, 32),
(2, 'aaaaa', 'DELETE', '2020-04-27 13:33:36.485075', 1, 6, 32),
(3, 'aaa', 'DELETE', '2020-04-27 13:33:47.468077', 2, 6, 32),
(5, '', 'DELETE', '2020-04-27 13:38:52.960777', 1, 6, 32),
(6, 'adasdasd', 'DELETE', '2020-04-27 13:42:20.928355', 1, 6, 32),
(7, 'กลยุทธ์', 'DELETE', '2020-04-27 13:42:34.665432', 2, 6, 32),
(8, '', 'DELETE', '2020-04-27 14:26:03.749495', 1, 6, 32),
(9, 'asdasdasd', 'DELETE', '2020-04-27 14:26:14.163713', 1, 6, 32),
(10, 'aaaasdasd', 'ACTIVE', '2020-04-27 14:26:37.975359', 1, 6, 32),
(11, 'adasdasdsad', 'ACTIVE', '2020-04-27 14:27:33.539804', 2, 6, 32);

--
-- Dumping data for table `ed_scaffolding_type`
--

INSERT INTO `ed_scaffolding_type` (`id`, `prefix`, `title`) VALUES
(1, 'conceptual', 'ฐานความช่วยเหลือด้านความคิดรวบยอด'),
(2, 'strategy', 'ฐานความช่วยเหลือด้านกลยุทธ์');

--
-- Dumping data for table `ed_sub_level`
--

INSERT INTO `ed_sub_level` (`id`, `prefix`, `title`, `ed_level_id`) VALUES
(1, 'graduate', 'บัณฑิตศึกษา', 2),
(2, 'bachelor', 'ปริญญาตรี', 2),
(3, 'elementary', 'อนุบาล', 1),
(4, 'middle', 'ประถมศึกษา', 1),
(5, 'high', 'มัธยมศึกษา', 1);

--
-- Dumping data for table `ed_task`
--

INSERT INTO `ed_task` (`id`, `description`, `status`, `timestamp`, `course_id`, `teacher_id`) VALUES
(6, 'ทดสอบสร้างภารกิจ<a class=\"btn-link\" href=\"https://www.facebook.com/\" target=\"_blank\">https://www.facebook.com/</a><div>ฟหกกหดหกด</div>', 'ACTIVE', '2020-04-24 20:59:49.695736', 2, 32),
(7, '', 'ACTIVE', '2020-04-28 14:07:14.461358', 2, 32);

--
-- Dumping data for table `ed_task_file`
--

INSERT INTO `ed_task_file` (`id`, `file_name`, `file_link`, `file_type`, `status`, `timestamp`, `task_id`) VALUES
(1, '74525054_956602731377047_8648344128590970880_n.jpg', '/uploads/course_id_2/task/files/2020-04-28/74525054_956602731377047_8648344128590970880_n.jpg', 'image/jpeg', 'ACTIVE', '2020-04-28 14:07:13.209638', 7);

--
-- Dumping data for table `ed_task_opengraph`
--

INSERT INTO `ed_task_opengraph` (`id`, `title`, `description`, `url`, `image`, `task_id`) VALUES
(14, 'SECRET vs ALLIANCE - EUROPE DIVISION - WePlay! Pushka League DOTA 2', 'Tournaments, esports news, everything WePlay! https://bit.ly/2VT13ov Commentary by ODPixel Fogged ►Watch the games live here: https://www.twitch.tv/weplayesp...', 'https://www.youtube.com/watch?v=mU3JHbmmJmw', 'https://i.ytimg.com/vi/mU3JHbmmJmw/maxresdefault.jpg', 23),
(16, 'Video Conferencing, Web Conferencing, Webinars, Screen Sharing', 'Zoom is the leader in modern enterprise video communications, with an easy, reliable cloud platform for video and audio conferencing, chat, and webinars across mobile, desktop, and room systems. Zoom Rooms is the original software-based conference room solution used around the world in board, conference, huddle, and training rooms, as well as executive offices and classrooms. Founded in 2011, Zoom helps businesses and organizations bring their teams together in a frictionless environment to get more done. Zoom is a publicly traded company headquartered in San Jose, CA.', 'https://zoom.us/', 'https://d24cgw3uvb9a9h.cloudfront.net/static/93938/image/thumb.png', 24),
(17, '【MV Full】โดดดิด่ง Ost. ไทบ้าน x BNK48 จากใจผู้สาวคนนี้ / BNK48', '『โดดดิด่ง Ost. ไทบ้าน x BNK48 จากใจผู้สาวคนนี้』 Lyrics: Yui Manasak Producer: Jiny Phuthai Executive Producer: Mr.Pong Thibaan the series BNK48 Members Natru...', 'https://www.youtube.com/watch?v=Ek8itihPQgE', 'https://i.ytimg.com/vi/Ek8itihPQgE/maxresdefault.jpg', 25);

--
-- Dumping data for table `ed_turnedin`
--

INSERT INTO `ed_turnedin` (`id`, `description`, `score`, `status`, `timestamp`, `member_id`, `task_id`) VALUES
(1, NULL, 10, 'DELETE', '2020-04-25 04:53:19.000000', 31, 6),
(2, NULL, 12, 'TURNEDIN', '2020-04-25 04:53:19.000000', 30, 6),
(5, '', 0, 'DELETE', '2020-04-28 15:23:44.671689', 31, 7),
(6, 'asdasd', 0, 'DELETE', '2020-04-28 15:32:53.876311', 31, 7),
(7, 'asdasdasdasd', 0, 'DELETE', '2020-04-28 15:47:03.744159', 31, 6),
(8, 'aaaa', 0, 'DELETE', '2020-04-28 15:47:43.269743', 31, 7),
(9, 'ส่งหมดทั้งสามรูปแบบ', 0, 'TURNEDIN', '2020-04-28 15:49:37.483570', 31, 6);

--
-- Dumping data for table `ed_turnedin_file`
--

INSERT INTO `ed_turnedin_file` (`id`, `file_name`, `file_link`, `file_type`, `status`, `timestamp`, `turnedin_id`) VALUES
(6, '74525054_956602731377047_8648344128590970880_n.jpg', '/uploads/course_id_2/turnedin/files/2020-04-28/74525054_956602731377047_8648344128590970880_n.jpg', 'image/jpeg', 'ACTIVE', '2020-04-28 15:23:37.254285', 5),
(7, '74525054_956602731377047_8648344128590970880_n.jpg', '/uploads/course_id_2/turnedin/files/2020-04-28/74525054_956602731377047_8648344128590970880_n_97KbkYz.jpg', 'image/jpeg', 'ACTIVE', '2020-04-28 15:49:24.945947', 9);

--
-- Dumping data for table `ed_turnedin_opengraph`
--

INSERT INTO `ed_turnedin_opengraph` (`id`, `title`, `description`, `url`, `image`, `turnedin_id`) VALUES
(4, 'Boxicons : Premium web friendly icons for free', 'Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines', 'https://boxicons.com/', 'http://boxicons.com/static/img/og-image.png', 5),
(5, 'Boxicons : Premium web friendly icons for free', 'Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines', 'https://boxicons.com/', 'http://boxicons.com/static/img/og-image.png', 8),
(6, 'Boxicons : Premium web friendly icons for free', 'Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines', 'https://boxicons.com/', 'http://boxicons.com/static/img/og-image.png', 9);

--
-- Dumping data for table `ed_user_type`
--

INSERT INTO `ed_user_type` (`id`, `prefix`, `title`) VALUES
(1, 'STUDENT', 'นักเรียน'),
(2, 'TEACHER', 'ครู');
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
