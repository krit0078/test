-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2020 at 02:25 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.3

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
(7, 'room', 'edcatagory'),
(11, 'room', 'edlevel'),
(9, 'room', 'edlog'),
(8, 'room', 'edmember'),
(12, 'room', 'edsublevel'),
(10, 'room', 'edusertype'),
(6, 'sessions', 'session');

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-04-21 00:08:16.447774'),
(2, 'auth', '0001_initial', '2020-04-21 00:08:16.647521'),
(3, 'admin', '0001_initial', '2020-04-21 00:08:17.370231'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-04-21 00:08:17.540327'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-04-21 00:08:17.550790'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-04-21 00:08:17.633528'),
(7, 'auth', '0002_alter_permission_name_max_length', '2020-04-21 00:08:17.720466'),
(8, 'auth', '0003_alter_user_email_max_length', '2020-04-21 00:08:17.811051'),
(9, 'auth', '0004_alter_user_username_opts', '2020-04-21 00:08:17.823019'),
(10, 'auth', '0005_alter_user_last_login_null', '2020-04-21 00:08:17.893832'),
(11, 'auth', '0006_require_contenttypes_0002', '2020-04-21 00:08:17.896823'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2020-04-21 00:08:17.907796'),
(13, 'auth', '0008_alter_user_username_max_length', '2020-04-21 00:08:17.934721'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2020-04-21 00:08:17.959796'),
(15, 'auth', '0010_alter_group_name_max_length', '2020-04-21 00:08:18.041506'),
(16, 'auth', '0011_update_proxy_permissions', '2020-04-21 00:08:18.056395'),
(17, 'room', '0001_initial', '2020-04-21 00:08:18.216970'),
(18, 'sessions', '0001_initial', '2020-04-21 00:08:18.405464'),
(19, 'room', '0002_edusertype', '2020-04-21 00:08:40.084419'),
(20, 'room', '0003_edmember_ed_user_type', '2020-04-21 00:09:28.196170'),
(21, 'room', '0004_auto_20200421_0715', '2020-04-21 00:15:52.713282'),
(22, 'room', '0005_auto_20200421_0716', '2020-04-21 00:16:27.404509'),
(23, 'room', '0006_edsublevel', '2020-04-21 00:20:13.871790');

--
-- Dumping data for table `ed_level`
--

INSERT INTO `ed_level` (`id`, `prefix`, `title`) VALUES
(1, 'Primary', 'ต่ำกว่าอุดมศึกษา'),
(2, 'Higer', 'อุดมศึกษา');

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
-- Dumping data for table `ed_user_type`
--

INSERT INTO `ed_user_type` (`id`, `prefix`, `title`) VALUES
(1, 'STUDENT', 'นักเรียน'),
(2, 'TEACHER', 'ครู');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
