USE JobSeeker;

CREATE TABLE FIRMS (
	cmpID INT NOT NULL AUTO_INCREMENT,
	cmpID_Zhilian       VARCHAR(255),   -- 企业ID（智联内部ID）
	cmpName             VARCHAR(255),   -- 企业名称
	cmpLink_Zhilian     VARCHAR(2048),  -- 智联招聘企业标准主页URL
	cmpLink_Zhilian_vip VARCHAR(2048),  -- 智联招聘企业Special主页URL
	cmpLink_58          VARCHAR(2048),  -- 58同城企业主页URL
	cmpLink_58_Credit   VARCHAR(2048),  -- 58同城企业信用档案链接
	cmpDescri           TEXT,           -- 企业简介
	cmpLoc              VARCHAR(255),   -- 企业地址
	cmpCity             VARCHAR(255),   -- 企业所在城市
	PRIMARY KEY ( cmpID )
);

CREATE TABLE JOBS (
	jobID INT NOT NULL AUTO_INCREMENT,
	jobID_ori  VARCHAR(255),   -- 职位ID（智联内部）
	jobName    VARCHAR(255),   -- 职位名称
	cmpName    VARCHAR(255),   -- 企业名称
	welfare    VARCHAR(100),   -- 福利标签
	jobDescri  TEXT,           -- 职位介绍（应聘条件、岗位职责）
	cmpDescri  TEXT,           -- 公司简介
	payMonthly     VARCHAR(255),   -- 职位月薪
	cmpLoc     VARCHAR(255),   -- 企业地址
	jobUpdate  VARCHAR(255),   -- 更新日期
	jobType    VARCHAR(255),   -- 就职类型（全职、兼职）
	workingAge VARCHAR(255),   -- 工作经验
	eduReq     VARCHAR(255),   -- 学历要求
	jobAmount  VARCHAR(255),   -- 招聘数量
	occupCode  VARCHAR(255),   -- 职业代码
	cmpSize    VARCHAR(255),   -- 企业规模
	cmpType    VARCHAR(255),   -- 企业类型
	industry   VARCHAR(255),   -- 所属行业
	cmpLink    VARCHAR(2048),  -- 企业主页
	PRIMARY KEY ( jobID )
);

CREATE TABLE TEMP_SEARCHRESULTS_ZHILIAN (
	tmpID INT NOT NULL AUTO_INCREMENT,
	jobName    VARCHAR(255),   -- 职位名称
	cmpName    VARCHAR(255),   -- 企业名称
	feedback   VARCHAR(50),    -- 反馈率
	workingAge VARCHAR(255),   -- 工作经验
	eduReq     VARCHAR(255),   -- 学历要求
	cmpType    VARCHAR(255),   -- 企业类型
	cmpSize    VARCHAR(255),   -- 企业规模
	jobDescri  VARCHAR(255),   -- 职位描述
	jobLink    VARCHAR(2048),  -- 职位链接
	cmpLink    VARCHAR(2048),  -- 企业主页
	jobPay     VARCHAR(255),   -- 职位月薪
	cmpLoc     VARCHAR(255),   -- 企业地址
	jobUpdate  VARCHAR(255),   -- 更新时间
	PRIMARY KEY ( tmpID )
);

CREATE TABLE TEST (
	tid INT NOT NULL AUTO_INCREMENT,
	Txt VARCHAR(255), 
	PRIMARY KEY ( tid )
);
