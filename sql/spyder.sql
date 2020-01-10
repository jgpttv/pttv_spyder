CREATE DATABASE  IF NOT EXISTS `pttv_spider_channel`  DEFAULT CHARACTER SET utf8;

USE `pttv_spider_channel`;


DROP TABLE IF EXISTS `channels`;
CREATE TABLE channels (
  channel_id int(11) NOT NULL AUTO_INCREMENT,
  channel_name varchar(50) DEFAULT NULL,
  channel_type varchar(50) DEFAULT NULL,
  channel_source text DEFAULT NULL,
  PRIMARY KEY (channel_id)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
