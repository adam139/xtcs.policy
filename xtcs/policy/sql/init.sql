/* This file contains table definitions 
 */


use xtcs;

-- online pay 

create table if not exists onlinepay (
    id integer unsigned not null auto_increment primary key,
    did integer unsigned not null,
    aname varchar(65) not null default '',    
    money varchar(65) not null default '',
    goods varchar(65) not null default '',
    atime DATETIME not null DEFAULT CURRENT_TIMESTAMP,
    openid varchar(32) not null default 'noweixin',
    status tinyint(1) not null  default 0,
    index pay_openid(openid) 
    
) engine=InnoDB DEFAULT CHARSET=utf8;


