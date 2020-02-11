/* This file contains table definitions 
 */


use xtcs;

-- online pay 

create table if not exists onlinepay (
    id integer unsigned not null auto_increment primary key,
    projectId integer unsigned not null,
    aname varchar(64) not null default '',    
    money decimal(13,2) not null default 0.00,
    goods varchar(64) not null default '',
    atime DATETIME not null DEFAULT CURRENT_TIMESTAMP,
    openid varchar(128) not null default 'noweixin',
    status tinyint(1) not null  default 0,
    index pay_openid(openid),
    index pay_name(aname)
    
) engine=InnoDB DEFAULT CHARSET=utf8;

-- openid accesstoken cache table for weixin jsapi
-- every user has self openid and accesstoken

create table if not exists accesstoken (
    id integer unsigned not null auto_increment primary key,
    openid varchar(128)  UNIQUE not null default 'weixindefaultopenid',
    token varchar(128) not null default 'weixindefaultaccesstoken', 
    index weixin_openid(openid)
    
) engine=InnoDB DEFAULT CHARSET=utf8;
