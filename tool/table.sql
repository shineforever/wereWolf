-- 创建数据库werewolf

CREATE DATABASE werewolfwechat DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER DATABASE werewolfwechat CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 登录验证
create table Token
(
    token_id nvarchar(100) primary key comment '主键',
    user_id nvarchar(100) comment '用户ID',
    createtime datetime comment '创建时间',
    validity int comment '有效时长'
);
ALTER TABLE token CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--图片信息
create table ImgPath
(
    imgpath_id nvarchar(100) primary key comment '主键',
    imgpath nvarchar(1000) comment '图片路径',
    foreign_id nvarchar(100) comment '关联ID'
);
ALTER TABLE ImgPath CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 管理员信息
create table AdminInfo(
    admin_id nvarchar(100) primary key comment '管理员ID',
    admin_name nvarchar(100) comment '管理员用户名',
    tel nvarchar(100) comment '手机号',
	password nvarchar(100) comment '管理员密码'
);
ALTER TABLE AdminInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--创建表userInfo,用户列表
create table UserInfo
(
    user_id nvarchar(100) primary key comment '主键',
    open_id nvarchar(100) comment '微信小程序用户ID',
    user_name nvarchar(100) comment '昵称',
    score int default 0 comment '用户积分',
    createtime datetime comment '创建时间'
);
ALTER TABLE UserInfo CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--创建表club, 俱乐部表
create table Club
(
    club_id nvarchar(100) primary key comment '主键',
    club_name nvarchar(100) comment '俱乐部名称',
    user_id nvarchar(100) comment '用户ID',
    area text comment '详细地址',
    createtime datetime comment '创建时间'
);
ALTER TABLE Club CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

alter table Club add constraint club_FK_adminInfo foreign key(user_id) references AdminInfo(admin_id);

--activity，活动
create table Activity
(
    activity_id nvarchar(100) primary key comment '主键',
    user_id nvarchar(100) comment '创建者',
    startdate date comment '比赛开始时间',
    fee nvarchar(100)  comment '报名费用',
    activity_name nvarchar(100) comment '活动标题',
    min_number int comment '最少参加活动人数',
    max_number int comment '最多参加活动人数',
    type_id smallint comment '区分活动类型，欢乐局为１，俱乐部为２',
    club_id  nvarchar(100) comment '预约俱乐部ID',
    description text comment '活动要求',
    area text comment '活动地址',
    activity_state int comment '活动状态,1表示已经创建,可以参加活动,2表示活动开始,3表示活动结束',
    createtime datetime comment '创建时间'
);
ALTER TABLE Activity CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
alter table  Activity add constraint activity_FK_club foreign key(club_id) references Club(club_id);

--狼人杀角色类型
create table RoleType
(
    type_id nvarchar(100) primary key comment '主键',
    type_name nvarchar(100) comment '俱乐部名称'
);
ALTER TABLE RoleType CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

--activity，活动
create table Participate
(
    participate_id nvarchar(100) primary key comment '主键',
    user_id nvarchar(100) comment '加入者ID',
    activity_id nvarchar(100) comment '活动ID',
    roletype_id nvarchar(100) comment '角色类型ID',
    location int comment '座位号',
    state boolean comment '玩家状态，true表示出局',
    score int default 0 comment '积分',
    createtime datetime comment '加入时间'
);
ALTER TABLE Participate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
alter table  Participate add constraint participate_FK_activity foreign key(activity_id) references Activity(activity_id);
alter table  Participate add constraint participate_FK_userInfo foreign key(user_id) references UserInfo(user_id);
alter table  Participate add constraint participate_FK_roleType foreign key(roleType_id) references Roletype(type_id);


--operate，法官操作
create table Operate
(
    operate_id nvarchar(100) primary key comment '主键',
    type_id nvarchar(100) comment '操作类型ID',
    activity_id nvarchar(100) comment '活动ID',
    foreign_id nvarchar(100) comment '被操作对象ID',
    user_id nvarchar(100) comment '操作对象ID',
    level_number int comment '操作顺序',
    createtime datetime comment '创建时间'
);

ALTER TABLE Operate CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



--ClubScore，俱乐部积分
create table ClubScore
(
    score_id nvarchar(100) primary key comment '主键',
    club_id nvarchar(100) comment '俱乐部ID',
    club_number nvarchar(100) comment '俱乐部积分',
    user_id nvarchar(100) comment '用户ID'
);

ALTER TABLE ClubScore CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;









