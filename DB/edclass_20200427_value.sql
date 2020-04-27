-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2020 at 09:44 AM
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
-- Dumping data for table `ed_course`
--

INSERT INTO `ed_course` (`id`, `course_name`, `description`, `cover_pic`, `status`, `uid`, `catagory_id`, `teacher_id`, `timestamp`) VALUES
(2, 'ทดสอบห้องเรียน', 'ss', '/uploads/course_id_2/cover/cover_EEkZrW0.jpg', 'ACTIVE', 'VtzLq', 5, 32, '2020-04-23 00:39:21.731632');

--
-- Dumping data for table `ed_enrolment`
--

INSERT INTO `ed_enrolment` (`id`, `timestamp`, `course_id`, `member_id`) VALUES
(1, '0000-00-00 00:00:00.000000', 2, 31),
(2, '2020-04-25 11:25:05.000000', 2, 30);

--
-- Dumping data for table `ed_level`
--

INSERT INTO `ed_level` (`id`, `prefix`, `title`) VALUES
(1, 'Primary', 'ต่ำกว่าอุดมศึกษา'),
(2, 'Higer', 'อุดมศึกษา');

--
-- Dumping data for table `ed_live`
--

INSERT INTO `ed_live` (`id`, `url`, `password`, `platform`, `status`, `timestamp`, `teacher_id`, `course_id`) VALUES
(1, 'asdasdasd', NULL, 'meet', 'ACTIVE', '2020-04-25 16:15:01.981229', 32, 2),
(2, 'adasdasd', 'aaaa', 'zoom', 'ACTIVE', '2020-04-25 16:15:09.679409', 32, 2);

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
(20, '127.0.0.1', 'Device(family=\'Other\', brand=None, model=None)', NULL, '2020-04-26 20:31:19.649121', 32);

--
-- Dumping data for table `ed_member`
--

INSERT INTO `ed_member` (`id`, `password`, `firstname`, `lastname`, `email`, `picture`, `timestamp`, `catagory_id`, `user_type_id`) VALUES
(30, '0ea46fdf7fc44bcfb17abc9af0b039d0', 'asdasdasd@hotmail.com', 'asdasdasd@hotmail.com', 'asdasdasd@hotmail.com', '/uploads/0/img/user.png', '2020-04-21 09:14:56.727157', 1, 1),
(31, '81dc9bdb52d04dc20036dbd8313ed055', '1234@gmail.com', '1234@gmail.com', '1234@gmail.com', '/uploads/0/img/user.png', '2020-04-21 21:53:41.440061', 5, 1),
(32, '8d788385431273d11e8b43bb78f3aa41', 'teacher', 'Fame', 'teacher@gmail.com', '/uploads/member_id_32/picture/2020-04-25/profile.jpg', '2020-04-22 22:46:07.087709', 1, 2),
(33, '698d51a19d8a121ce581499d7b701668', '1111', '1111', '111@gmail.com', '/uploads/0/img/user.png', '2020-04-25 17:55:20.470325', 5, 1);

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
(3, 'lll', 'ACTIVE', '2020-04-24 11:18:54.322292', 32, 48);

--
-- Dumping data for table `ed_resource`
--

INSERT INTO `ed_resource` (`id`, `description`, `status`, `timestamp`, `task_id`, `teacher_id`) VALUES
(4, 'asdasdasd', 'DELETE', '2020-04-27 06:38:57.464787', 6, 32),
(5, '', 'ACTIVE', '2020-04-27 06:39:06.589226', 6, 32),
(7, '<div><a href=\"https://drive.google.com/drive/u/2/folders/1wk45N-vMj1-Pxqdb5JJmL0S54QWx9Ul1\" target=\"_blank\">https://drive.google.com/drive/u/2/folders/1wk45N-vMj1-Pxqdb5JJmL0S54QWx9Ul1</a><br><div><br></div></div>', 'DELETE', '2020-04-27 10:01:11.651800', 6, 32),
(8, 'ppppppppppppppppasd', 'DELETE', '2020-04-27 11:40:00.551929', 6, 32),
(9, 'asdasd', 'DELETE', '2020-04-27 11:40:40.902291', 6, 32);

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

INSERT INTO `ed_scaffolding` (`id`, `description`, `status`, `timestamp`, `task_id`, `teacher_id`, `scaff_type_id`) VALUES
(1, 'lkkjljsdf', 'DELETE', '2020-04-27 13:32:48.438303', 6, 32, 1),
(2, 'aaaaa', 'DELETE', '2020-04-27 13:33:36.485075', 6, 32, 1),
(3, 'aaa', 'DELETE', '2020-04-27 13:33:47.468077', 6, 32, 2),
(5, '', 'DELETE', '2020-04-27 13:38:52.960777', 6, 32, 1),
(6, 'adasdasd', 'DELETE', '2020-04-27 13:42:20.928355', 6, 32, 1),
(7, 'กลยุทธ์', 'DELETE', '2020-04-27 13:42:34.665432', 6, 32, 2),
(8, '', 'DELETE', '2020-04-27 14:26:03.749495', 6, 32, 1),
(9, 'asdasdasd', 'DELETE', '2020-04-27 14:26:14.163713', 6, 32, 1),
(10, 'aaaasdasd', 'ACTIVE', '2020-04-27 14:26:37.975359', 6, 32, 1),
(11, 'adasdasdsad', 'ACTIVE', '2020-04-27 14:27:33.539804', 6, 32, 2);

--
-- Dumping data for table `ed_scaffolding_type`
--

INSERT INTO `ed_scaffolding_type` (`id`, `prefix`, `title`) VALUES
(1, 'conceptual', 'ฐานความช่วยเหลือด้านความคิดรวบยอด'),
(2, 'strategy', 'ฐานความช่วยเหลือด้านกลยุทธ์');

--
-- Dumping data for table `ed_social`
--

INSERT INTO `ed_social` (`id`, `description`, `status`, `timestamp`, `task_id`, `teacher_id`) VALUES
(1, 'asdasd', 'DELETE', '2020-04-27 11:41:37.019551', 6, 32),
(2, 'aaaaa', 'DELETE', '2020-04-27 11:45:15.647640', 6, 32),
(3, '', 'ACTIVE', '2020-04-27 11:45:58.822854', 6, 32),
(4, '', 'ACTIVE', '2020-04-27 11:46:38.751696', 6, 32),
(5, 'asasd', 'DELETE', '2020-04-27 12:02:24.797206', 6, 32),
(6, 'asdasdasd', 'DELETE', '2020-04-27 12:02:27.521769', 6, 32),
(7, '', 'DELETE', '2020-04-27 13:31:15.711423', 6, 32),
(8, '', 'DELETE', '2020-04-27 13:31:33.848635', 6, 32);

--
-- Dumping data for table `ed_social_file`
--

INSERT INTO `ed_social_file` (`id`, `file_name`, `file_link`, `file_type`, `status`, `timestamp`, `social_id`) VALUES
(2, '67354581_1613922928740181_4657308926277058560_n.jpg', '/uploads/course_id_2/social/files/2020-04-27/67354581_1613922928740181_4657308926277058560_n.jpg', 'image/jpeg', 'ACTIVE', '2020-04-27 11:46:34.558586', 4),
(3, '74525054_956602731377047_8648344128590970880_n.jpg', '/uploads/course_id_2/social/files/2020-04-27/74525054_956602731377047_8648344128590970880_n.jpg', 'image/jpeg', 'ACTIVE', '2020-04-27 11:46:37.270055', 4);

--
-- Dumping data for table `ed_social_opengraph`
--

INSERT INTO `ed_social_opengraph` (`id`, `title`, `description`, `url`, `image`, `social_id`) VALUES
(2, 'Boxicons : Premium web friendly icons for free', 'Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines', 'https://boxicons.com/', 'http://boxicons.com/static/img/og-image.png', 3),
(3, 'Boxicons : Premium web friendly icons for free', 'Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines', 'https://boxicons.com/', 'http://boxicons.com/static/img/og-image.png', NULL);

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

INSERT INTO `ed_task` (`id`, `description`, `status`, `timestamp`, `teacher_id`, `course_id`) VALUES
(6, 'ทดสอบสร้างภารกิจ<a class=\"btn-link\" href=\"https://www.facebook.com/\" target=\"_blank\">https://www.facebook.com/</a><div>ฟหกกหดหกด</div>', 'ACTIVE', '2020-04-24 20:59:49.695736', 32, 2);

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

INSERT INTO `ed_turnedin` (`id`, `status`, `timestamp`, `member_id`, `task_id`, `description`, `score`) VALUES
(1, 'TURNEDIN', '2020-04-25 04:53:19.000000', 31, 6, NULL, 10),
(2, 'TURNEDIN', '2020-04-25 04:53:19.000000', 30, 6, NULL, 12);

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
