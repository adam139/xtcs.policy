/* This file contains table definitions 
 */


use xtcs;

-- cishan xiangmu table

create table if not exists xiangmu (
    id integer unsigned not null auto_increment primary key,
    mingcheng varchar(64) not null default '',
    jieshao  varchar(256) null default '',
    zhuceshijian DATETIME not null DEFAULT CURRENT_TIMESTAMP,
    youxiao TINYINT(1) not null default 1,
    index xiangmu_mingcheng(mingcheng)
) engine=InnoDB DEFAULT CHARSET=utf8;

-- some cishan xiangmu 's juanzeng jilu table

create table if not exists juanzeng (
    id integer unsigned not null auto_increment primary key,
    xiangmu_id integer unsigned not null,
    xingming varchar(64) not null default '',
    xianjin decimal(13,2) null default 0.00,
    wuzi varchar(128) null default '',
    wuzi_jiazhi decimal(13,2) null default 0.00,
    juanzeng_shijian DATETIME not null DEFAULT CURRENT_TIMESTAMP,
    openid varchar(128) null default 'noweixin',
    status tinyint(1) null  default 0,
    index weixin_openid(openid),
    index juanzeng_xingming(xingming),
    index juanzeng_xianjin(xianjin),
    index juanzeng_wuzijiazhi(wuzi_jiazhi),
    foreign key(xiangmu_id)
        references xiangmu(id)
            on update restrict
            on delete restrict
) engine=InnoDB DEFAULT CHARSET=utf8;


-- openid accesstoken cache table for weixin jsapi
-- every user has self openid and accesstoken

create table if not exists accesstoken (
    id integer unsigned not null auto_increment primary key,
    openid varchar(128)  UNIQUE not null default 'weixindefaultopenid',
    token varchar(128) not null default 'weixindefaultaccesstoken',
    expiredtime  DATETIME not null,
    index weixin_openid(openid)
    
) engine=InnoDB DEFAULT CHARSET=utf8;
