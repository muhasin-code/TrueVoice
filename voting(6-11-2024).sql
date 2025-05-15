/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - blockchain_based_voting
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`blockchain_based_voting` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `blockchain_based_voting`;

/*Table structure for table `campaigns` */

DROP TABLE IF EXISTS `campaigns`;

CREATE TABLE `campaigns` (
  `campaign_id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_name` varchar(20) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `venue` varchar(20) DEFAULT NULL,
  `campaign_date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`campaign_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `campaigns` */

insert  into `campaigns`(`campaign_id`,`campaign_name`,`date`,`venue`,`campaign_date`) values 
(1,'collage day','2024-11-06','seminar hall','2024-12-05');

/*Table structure for table `candidate` */

DROP TABLE IF EXISTS `candidate`;

CREATE TABLE `candidate` (
  `candidate_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`candidate_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `candidate` */

insert  into `candidate`(`candidate_id`,`student_id`,`election_id`,`date`,`status`,`post_id`) values 
(10,10,3,'2024-11-06','approved',7),
(3,8,2,'2024-11-06','approved',4),
(4,7,2,'2024-11-06','approved',4),
(9,9,3,'2024-11-06','approved',7),
(8,2,3,'2024-11-06','approved',8),
(7,1,3,'2024-11-06','approved',8);

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) DEFAULT NULL,
  `complaint` varchar(256) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `reply` varchar(20) DEFAULT NULL,
  `usertype` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaint_id`,`id`,`complaint`,`date`,`reply`,`usertype`) values 
(1,5,'bad','2024-11-06','pending','student');

/*Table structure for table `course` */

DROP TABLE IF EXISTS `course`;

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `course` */

insert  into `course`(`course_id`,`course_name`) values 
(1,'bsc computer science'),
(2,'BA english'),
(3,'MCA'),
(4,'BA malayalam');

/*Table structure for table `election` */

DROP TABLE IF EXISTS `election`;

CREATE TABLE `election` (
  `election_id` int(11) NOT NULL AUTO_INCREMENT,
  `election_name` varchar(20) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `venue` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`election_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `election` */

insert  into `election`(`election_id`,`election_name`,`date`,`venue`,`status`) values 
(2,'collage election','2024-11-20','seminar hall','completed'),
(3,'union election','2024-11-20','collage auditorium','completed');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `usertype` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`id`,`date`,`feedback`,`usertype`) values 
(1,5,'2024-11-06','good','student');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `usertype` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','123','admin'),
(2,'amal','123','candidate'),
(3,'abi','123','candidate'),
(4,'sree','123','student'),
(5,'kiran','123','student'),
(6,'akash','123','student'),
(7,'akku','123','student'),
(8,'naveen','123','candidate'),
(9,'aswin','123','candidate'),
(10,'fathima','123','candidate'),
(11,'diya','123','candidate');

/*Table structure for table `post` */

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_name` varchar(20) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `post` */

insert  into `post`(`post_id`,`post_name`,`date`,`election_id`) values 
(8,'magazine editor ','2024-11-06',3),
(7,'collage chairman','2024-11-06',3),
(4,'secretary','2024-11-06',2);

/*Table structure for table `result` */

DROP TABLE IF EXISTS `result`;

CREATE TABLE `result` (
  `result_id` int(11) NOT NULL AUTO_INCREMENT,
  `candidate_id` int(11) DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `result` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`result_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `result` */

insert  into `result`(`result_id`,`candidate_id`,`election_id`,`post_id`,`result`) values 
(5,10,3,7,'2'),
(4,8,3,8,'3'),
(3,3,2,4,'4');

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `dob` varchar(20) DEFAULT NULL,
  `house_name` varchar(20) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`student_id`,`login_id`,`course_id`,`first_name`,`last_name`,`email`,`phone`,`gender`,`dob`,`house_name`,`place`,`pincode`) values 
(1,2,1,'amal','A','shahanavs786@gmail.com','9074331344','male','2002-02-12','house','kaloor','688524'),
(2,3,1,'abi','a','shahanavs786@gmail.com','1234567890','male','2002-03-12','ho','kaloor','688524'),
(3,4,2,'sree','vs','shahanavs786@gmail.com','9074332345','female','2000-02-15',' ALAPPUZHA','cherthala','688524'),
(4,5,2,'kiran','kiran','shahanavs786@gmail.com','9123433199','male','2000-03-12',' HOUSE  ','cherthala','688524'),
(5,6,2,'akash','a','shahanavs786@gmail.com','9074234997','male','2000-12-12','ALAPPUZHA','cherthala','688524'),
(6,7,2,'akku','s','shahanavs786@gmail.com','9074331997','female','2000-03-12','CHERTHALA ','CHERTHALA ','688524'),
(7,8,4,'naveen','s','shahanavs786@gmail.com','9074331997','male','2000-03-12','as','kaloor','688524'),
(8,9,2,'aswin','a','shahanavs786@gmail.com','9074331997','male','2000-02-12','qw','q','688524'),
(9,10,2,'fathima','s','shahanavs786@gmail.com','9074331997','female','2002-02-12','as','kaloor','688524'),
(10,11,3,'diya','d','shahanavs786@gmail.com','9074335667','female','2003-03-12','ALAPPUZHA','kaloor','688524');

/*Table structure for table `vote` */

DROP TABLE IF EXISTS `vote`;

CREATE TABLE `vote` (
  `vote_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `election_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`vote_id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

/*Data for the table `vote` */

insert  into `vote`(`vote_id`,`student_id`,`election_id`,`post_id`,`status`) values 
(1,3,1,1,'completed'),
(2,3,1,2,'completed'),
(3,10,1,1,'completed'),
(4,10,1,2,'completed'),
(5,9,1,1,'completed'),
(6,9,1,2,'completed'),
(7,8,1,1,'completed'),
(8,4,1,1,'completed'),
(9,4,1,2,'completed'),
(10,1,2,4,'completed'),
(11,3,2,4,'completed'),
(12,8,2,4,'completed'),
(13,5,2,4,'completed'),
(14,4,2,4,'completed'),
(15,1,3,8,'completed'),
(16,2,3,8,'completed'),
(17,3,3,8,'completed'),
(18,7,3,8,'completed'),
(19,7,3,7,'completed'),
(20,4,3,7,'completed'),
(21,5,3,7,'completed');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
