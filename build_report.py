from pathlib import Path
import json, html, re
from datetime import datetime

OUT = Path(__file__).resolve().parent / 'docs'
OUT.mkdir(exist_ok=True)
AS_OF='2026-09-28'

def src(id,title,url,issuer,published,kind,status,scope):
    return dict(id=id,title=title,url=url,issuer=issuer,published=published,kind=kind,status=status,scope=scope,checked_on=AS_OF)
SOURCES=[
src('S01','杭州市区流动人口随迁子女积分入学实施办法（杭教基〔2019〕5号）','https://zfgb.hangzhou.gov.cn/11/105220253/t124220253054/520011.shtml','杭州市教育局 / 市政府公报','2019-12-31','政策原文','已读原文；历史基础文件，结合拟入学年度通知使用','小学一年级；不能代替初中或插班转学细则'),
src('S02','《杭州市区流动人口随迁子女积分入学实施办法》解读','https://zfgb.hangzhou.gov.cn/15/105220253/t131220253054/524766.shtml','杭州市教育局 / 市政府公报','2019-12-31','官方解读','已读解读；不是2026年新发布政策','积分入学、儿童居住证、人才居住证等路径的区别'),
src('S03','2026年杭州市义务教育招生通知全文转引','https://ori.hangzhou.com.cn/ornews/content/2026-05/22/content_9227480.htm','杭州网、杭州通客户端（转引市教育局文件）','2026-05-22','媒体转引政策','已读转引全文；非政府原始发布页','2026年新生入学、外地小学毕业生升初、长幼随学、转学原则'),
src('S04','2026年杭州市行知小学招生工作方案','https://www.hzxhjy.cn/xzxx/xyzx/xygg/202605/t20260528_758900.shtml','杭州市行知小学 / 西湖教育网','2026-05-29','学校招生方案','已读学校方案；仅作该校当年规则实例','小学一年级；不能代表蒋村学校或西湖区全部转学规则'),
src('S05','《关于2026年杭州市区各类高中招生工作的通知》全文转引','https://ori.hangzhou.com.cn/ornews/content/2026-04/21/content_9209828.htm','杭州网、杭州通客户端（转引市教育局文件）','2026-04-21','媒体转引政策','已读转引全文；最终报名应取得招生主管部门核验','文中“市区”指上城、拱墅、西湖、滨江、钱塘及西湖风景名胜区'),
src('S06','2026年滨江区暑假转学于7月1日启动','https://www.hhtz.gov.cn/col/col1229506924/art/2026/art_471992a6ee304881ac9e62a9c22584c4.html','滨江区教育局','2026-07-10','官方办理通知','已读通知；本次申请窗口已经结束','滨江区2026年暑假转学；具体资格仍须阅读系统申请须知'),
src('S07','关于进一步深化户籍制度改革的实施意见（杭政办函〔2023〕33号）','https://zfgb.hangzhou.gov.cn/10/105220253/t117220253054/518554.shtml','杭州市人民政府办公厅','2023-04-26','政策原文','已读；2023-05-08施行，不能冒充2026年完整落户办事指南','学历、技能、积分等落户和居住证基础规定；当前个案条件须复核'),
src('S08','关于进一步完善杭州市创业场地扶持办法的通知（杭人社发〔2025〕103号）','https://zfgb.hangzhou.gov.cn/11/112220253/t126220253124/530039.shtml','杭州市人力资源和社会保障局','2025-12-29','政策原文','已读；2026-02-01施行','陪跑空间及园外创业场地补贴；限定人群，不是住房补贴'),
src('S09','支持人工智能全产业链高质量发展若干措施（杭政办函〔2024〕40号）','https://zfgb.hangzhou.gov.cn/10/105220253/t117220253054/518968.shtml','杭州市人民政府办公厅','2024-07-18（成文）','政策原文','已读；2024-08-19施行，有效至2027-12-31','市级AI产业支持；还要匹配实际业务与具体申报条件'),
src('S10','城西科创大走廊创新发展专项资金管理办法（杭政函〔2026〕36号）','https://zfgb.hangzhou.gov.cn/10/104220263/t121220263044/530432.shtml','杭州市人民政府','2026-04-22','政策原文','已读；2026-05-13施行，资金安排期2026—2030年','城西科创大走廊规划范围；不是三区所有地址都自动适用'),
src('S11','推动经济高质量发展的若干政策（2026年版）政策解读','https://zfgb.hangzhou.gov.cn/15/102220263/t126220263024/530218.shtml','杭州市发展和改革委员会 / 市政府公报','2026-02-27','官方解读','已读；年度框架，具体项目另查申报通知','软件、数字贸易、文化出海、出海服务载体等支持方向'),
src('S12','杭州高新区（滨江）“AI+OPC”创业护航十条（杭高新〔2026〕4号）','https://www.hhtz.gov.cn/col/col1229225928/art/2026/art_ac2c2c96637e49c6ac4166cadd45afc4.html','杭州高新区（滨江）管委会、政府','2026-06-25','政策原文','页面标注有效；2026-07-25生效，有效期一年','依法注册的AI+OPC及规定的社区运营主体等；不是所有个体创业者'),
src('S13','“AI+OPC”创业护航十条负责人解读','https://www.hhtz.gov.cn/col/col1229247079/art/2026/art_c3716409c56242cb971e501988f12427.html','滨江区政府办；解读机关区科技局','2026-06-25','官方解读','已读；补充工位上限、入库主体定义、住房条件和部门电话','与S12配套；入库条件全文、社区创建名单仍需向主管部门索取'),
src('S14','进一步加快新一代人工智能产业应用发展若干措施（杭高新〔2026〕6号）','https://www.hhtz.gov.cn/col/col1229225928/art/2026/art_5a167e13c395414abfc95de936cd5813.html','杭州高新区（滨江）管委会、政府','2026-08-12','政策原文','页面标注有效；2026-09-11施行，替代杭高新〔2025〕9号','AI算力、模型、场景和产业生态；补贴对象逐条不同'),
src('S15','滨江进一步加快新一代人工智能产业应用发展若干措施解读','https://www.hhtz.gov.cn/col/col1229247079/art/2026/art_ed272d25bc2c4991b50dc6406c21d183.html','滨江区政府办','2026-08-12','官方解读','已读；与S14配套','主体资格、信用、经营及申报责任等条件'),
src('S16','2026年下半年创新型中小企业申报及复核通知','https://www.hhtz.gov.cn/col/col1487002/art/2026/art_6ff680d9472441f6bd1fd995b0f73524.html','滨江区经济和信息化局','2026-09-24','官方申报通知','已读；正文新旧文件及历史年份表述存在不一致，须向经信局确认','2026-10-20 17:00截止；并不等于申报后立即获得现金奖励'),
src('S17','滨江入选国家数字贸易示范区首批创建名单','https://www.hhtz.gov.cn/col/col1487008/art/2026/art_e383cca71f5a427fa864231b88d26d23.html','滨江区政府门户 / 天堂硅谷报','2026-09-17','官方平台动态','已读；产业与服务信息，不是补贴申报办法','数字内容、跨境数据和知识产权相关服务背景'),
src('S18','安滨乐业｜9月就业创业服务活动','https://www.hhtz.gov.cn/col/col1229247394/art/2026/art_b74a7bdea11542b19031f2c48f2e6a01.html','滨江区人力资源和社会保障局','2026-09-04','官方活动与联系人','已读；多数列示活动日期已过，不能当作未来预约名额','可核验的创业陪跑空间、地址、街道服务电话'),
src('S19','滨江区就业创业服务栏目','https://www.hhtz.gov.cn/col/col1229565990/index.html','滨江区政府门户','栏目持续更新','办事栏目','已打开栏目；不是单独的扶持政策','就业创业通知；以各条申报文件为准'),
src('S20','滨江区教育服务栏目','https://www.hhtz.gov.cn/col/col1229565992/index.html','滨江区政府门户','栏目持续更新','办事栏目','已打开栏目；应继续查看目标学期通知','招生、学校及转学信息入口'),
src('S21','亲清在线','https://qinqing.hangzhou.gov.cn/','杭州市政务服务平台','动态平台','申报入口','已确认入口；未登录、未验证个体企业的可申报清单','供企业检索、核对具体惠企事项'),
src('S22','杭州人才网','https://www.hzrc.com/','杭州人才网','动态平台','招聘入口','已确认入口；没有逐一核实当前教师岗位','供妻子检索岗位、雇主和招聘要求'),
src('S23','高新人才网','https://www.hhrc.com.cn/','高新人才网（区政府就业栏目链接）','动态平台','招聘入口','已确认政府栏目链接；未核验具体招聘职位','滨江就业与招聘线索；以招聘单位公告为准'),
src('S24','浙江政务服务网 / 浙里办','https://www.zjzwfw.gov.cn/','浙江政务服务平台','动态平台','综合办事入口','入口由招生文件指引；未登录核验家庭办理结果','入学一件事、居住登记/居住证、落户等事项检索')
]
SMAP={s['id']:s for s in SOURCES}

def refs(*ids):
    return ' '.join(f'<a class="cite" href="#src-{i}" title="{html.escape(SMAP[i]["title"])}">[{i}]</a>' for i in ids)

def original(*ids):
    return ' '.join(f'<a class="original" href="{html.escape(SMAP[i]["url"])}" target="_blank" rel="noopener noreferrer">{i} · {"官方原文" if SMAP[i]["kind"]=="政策原文" else SMAP[i]["kind"]} ↗</a>' for i in ids)

POLICIES=[]
def policy(id,category,title,scope,date,quote,reading,meaning,action,sources,status='条件匹配后再办理'):
    POLICIES.append(dict(id=id,category=category,title=title,scope=scope,date=date,quote=quote,reading=reading,meaning=meaning,action=action,sources=sources,status=status))

policy('P01','教育','小学积分入学：先确认是“入一年级”，还是“插班”','小学一年级 / 以拟入学区当年通知为准','2019年基础办法；2020-01-01起施行','就读小学一年级',
'''办法要求儿童本人具备规定的有效居住证；家长积分用于排序。基础办法的积分截止点为4月10日；若为休息日，提前至此前最后一个工作日，积分不能跨区用于入学排序。最终还要看拟入学年度通知。''',
'''这份政策<strong>不能拿来证明在西安读小学二、三年级的孩子能插班，也不能证明初中能转入</strong>。家长有居住证，不应直接当作孩子已满足证件要求。''',
'''先写清每个孩子的出生年月、现年级和计划入学学期；若不是一年级新生，转到P03及目标区转学规则。''',['S01','S02'],'历史基础规则，限小学一年级')
policy('P02','教育','外地小学毕业升初：与初中在读转学不是同一条路径','2026年杭州市义务教育新生招生','2026-05-22发布的通知转引','小学毕业生',
'''2026年招生通知允许符合条件的外地小学毕业生，向对应户籍或居住证所在区申请升初；具体由区级招生方案衔接。公办、民办报名和未录取后的安排也有顺序要求。''',
'''“孩子上初中”必须拆成两种情况：<strong>明年读初一</strong>，或<strong>已经读初一/初二/初三</strong>。前者核升初招生，后者核插班转学及以后高中报考。''',
'''请区教育部门按孩子实际状态确认报名入口、材料、接收方式和下一学年时间。不要用2026年日期推定2027年的报名窗口。''',['S03'],'媒体全文转引；2027通知待发布/核验')
policy('P03','教育','在读孩子转学：先查年级空位，再走正式审核','滨江区2026年暑假转学实例','2026年7月1日—8月15日申请；现已关闭','查看学位',
'''滨江官方通知列出网上申请、各年级学位查询、材料审核，以及多孩绑定和调剂选项。审核完成时间安排在8月31日前；系统中的初审顺序并非录取顺序。''',
'''它证明滨江有可查的办理流程，<strong>不证明目标小区对应学校一定有该年级空位</strong>，也不证明该家庭已符合接收条件。''',
'''查看新学期公告及系统“转学申请须知”，向区教育局核对现年级、户籍、儿童居住证、租赁材料。2027年春季或暑假新窗口尚未核实。''',['S06'],'2026年暑假窗口已结束')
policy('P04','教育','租在学校旁边，不等于获得那所学校的确定学位','西湖区行知小学2026年一年级方案示例','2026-05-29公布','房、住、户一致优先',
'''该校方案按报名类别和房、住、户等条件排序，非本地户籍儿童还需核验居住证、租赁备案等资料；超出接收能力的情况涉及区级统筹。''',
'''这只能作为“租房不保证指定学校”的现实例子；<strong>行知小学的方案不能代替蒋村、三墩所有学校的规则</strong>。落集体户也不能直接等同于房户一致。''',
'''对每一套候选住房确认实际所属区、门牌、对应学校、目标年级学位和本家庭排序；依据须来自教育部门或学校正式方案，不是房东口头保证。''',['S04'],'学校当年方案，不是全区通用方案')
policy('P05','教育','初中孩子必须把“以后在哪里报考高中”一起确认','上城、拱墅、西湖、滨江、钱塘及西湖风景名胜区','2026年市区高中招生口径','连续3年',
'''2026年文件对外省籍进城务工人员随迁子女的相应报考路径，列有本市区初中连续3年学习经历和学籍、家长稳定就业与住所（含租赁），以及近3年至少1年社保等条件；其他户籍类别另列。''',
'''<strong>初二或初三从西安转入，不能据“转学成功”推定满足上述路径。</strong>文中“市区”有特定招生范围，不包含余杭；不能把这份文件直接套给余杭。''',
'''向实际招生主管部门同时核对：毕业时适用哪类报考资格、是否满足连续学籍要求、改为本地户籍的认定截止日、名额分配资格是否另有要求。未获明确答复前，保留孩子原就读安排。''',['S05'],'最高优先核验；不能用小学政策替代')
policy('P06','户籍','落户与居住证：把历史依据和当前可办条件分开','市级基础规则；由公安窗口确认个案','杭政办函〔2023〕33号；2023-05-08起施行','合法稳定住所',
'''2023年文件涉及大专、硕士、技能和积分等落户路径，也规定居住登记满半年且满足相应条件的居住证基础路径；未满16周岁儿童可依共同居住监护人的居住证申领。''',
'''这是已核到的<strong>2023年基础文件，不是2026年完整落户资格清单</strong>。夫妻学历、年龄、工作和社保未提供，不能断言谁能直接落户；妻子曾任教师也不等于已取得杭州人才资格。''',
'''2023年文件列有：普通高校大专35周岁以下且落实市区就业单位；普通高校硕士45周岁以下可先落户后就业；技能路径另看证书等级、单位社保和住所；积分满100分只是文件中的原则，并保留调整机制。这些历史条件不可直接当作2026年办理承诺。请公安窗口分别预审夫妻当前路径、儿童随迁、租赁或集体户落点，再由教育部门复核完成时间。''',['S07','S02'],'现行细则及本人资格仍须复核')
policy('P07','教育','“长幼随学”是申请协调，不是任意指定学校','2026年义务教育招生与滨江转学办理','2026年通知口径','长幼随学',
'''2026年招生通知提出落实长幼随学；滨江转学系统提供多孩绑定等选项。实际办理仍受所属区方案、接收条件和学位制约。''',
'''这家有小学和初中孩子，<strong>不能直接推定两人会被安排进同一教育集团或同一校区</strong>。跨学段能否协调、是否有接送便利，应单独询问。''',
'''先分别确认每个孩子的基本入学资格，再问多孩协调范围和可选学校。把“同一片区便于接送”作为居住筛选条件，而非未经核实的权利承诺。''',['S03','S06'],'有办理机制，不保证指定结果')
policy('P08','创业','创业场地补贴：先过“人群”门槛，再谈租金上限','杭州市创业陪跑空间及符合规定的园外创业用房','杭人社发〔2025〕103号；2026-02-01施行','重点人群创业者',
'''陪跑空间补贴面向在校生、毕业5年内高校毕业生、登记失业半年以上人员、就业困难人员、持证残疾人及自主就业退役军人。还看持股达到30%、在杭社保、入驻满6个月及首次补贴起点在注册5年内；在校生外的申请人不得由其他用人单位缴纳规定的职工保险。最高3元/㎡·天、50㎡、3年，低于上限按实际支出。''',
'''父亲有创业经历，并不自动满足重点人群身份。<strong>创业办公租金不是全家住房租金</strong>；园区运营方的补助也不是入驻公司补助。不能将宣传上限直接计入家庭收入。''',
'''园外路径主要限登记失业人员、就业困难人员和自主就业退役军人，要求租赁创业用房满12个月及营业证照、租赁、实际经营地址一致；面积上限100㎡，第1年1元/㎡·天，第2、3年0.5元/㎡·天。两类租金补贴不能重复，累计不超3年。申请须在符合条件后的12个月内提出。先核资格，再留存合同、发票、付款和报税凭证，不先垫付高租金赌补贴。''',['S08'],'资格未定，家庭预算暂按0元补贴')
policy('P09','创业','滨江AI+OPC：有AI产品的小团队才进入核验','滨江区入库AI+OPC、纳入创建名单的社区等','杭高新〔2026〕4号；2026-07-25起，有效期一年','人员规模一般10人以下',
'''官方解读要求区内注册、聚焦规定的AI业务、拥有相关创新产品或应用场景并按条件入库。创建社区工位最高100%支持，但每工位每年封顶8000元；人才公寓最高50%减租另须人才、住房及未享受同类优惠证明。''',
'''普通出海App、自媒体或传统SaaS不能只因“用AI办公”就默认符合。Token支持最高60%、每年最高100万元，限定生态伙伴采购及入库额度池；<strong>不能认定任意海外API费用都报销，也不是任意家庭租房打五折</strong>。''',
'''索取现行入库条件、社区创建名单、伙伴供应商清单及兑现流程。先拿真实产品、人员和主体资料申请确认；不要为补贴把普通业务包装成AI项目。''',['S12','S13'],'有条件匹配；尚未核得该家庭入库资格')
policy('P10','创业','杭州市级AI政策：作为项目对接线索，不作普惠现金','杭州AI产业相关企业、平台和项目','杭政办函〔2024〕40号；有效至2027-12-31','从优、从高、不重复',
'''措施涉及算力、模型、场景、项目和人才等支持，不同条款对应不同申报主体与费用口径；并设置同类事项不重复享受的规则。''',
'''这家实际开展AI产品业务时才需逐条比对；单纯有海外客户或购买模型API，不能据此得出有一笔确定补助。基金投资也不等同无偿补贴。''',
'''准备产品说明、研发证据、合同发票和实际经营资料，通过亲清在线或主管部门找当期申报项目；先核同一费用能否与区级项目同时使用。''',['S09'],'业务条件与当期申报需匹配')
policy('P11','创业','滨江AI新办法：2026年9月版本替代旧版本','滨江AI研发、模型应用及相关产业主体','杭高新〔2026〕6号；2026-09-11施行','采购企业',
'''新办法替代杭高新〔2025〕9号，覆盖算力、模型、应用场景及小微企业空间等支持。其中某些软件订阅、API或会员形式的示范应用补贴，受益对象明确是采购企业，不是当然给软件销售方。''',
'''做SaaS的人最容易把“客户采购补助”读成“我有订阅收入就能领钱”。房租、算力等项目仍有口径和申报要求，<strong>不能与AI+OPC同一费用机械叠加</strong>。''',
'''对照原文责任单位咨询：我的角色是研发方、采购方还是平台运营方？项目、供应商、费用期间和信用条件是否符合？由主管部门确认选择何种渠道。''',['S14','S15'],'页面标注有效；已替代2025年版本')
policy('P12','创业','城西科创大走廊：是区域资金框架，不是注册即领钱','大走廊规划范围内的相关项目与主体','杭政函〔2026〕36号；2026-05-13施行','专项资金',
'''资金办法覆盖2026—2030年，涉及创新平台、成果转化、人才和科技服务等方向。适用的是规划范围及对应项目条件，不是西湖、余杭、临安所有地址和企业。''',
'''它支持将城西放入创业考察范围，但<strong>无法单独证明普通出海SaaS可获得房租或现金补助</strong>。“科技服务机构”扶持也不能直接等同“所有做软件的人”。''',
'''向园区或区主管部门索取与本产品相符的申报细则、范围边界及预算年度，区分财政预算、股权投资、项目支持和运营机构奖励。''',['S10'],'区域框架，不等于个人申报承诺')
policy('P13','创业','出海业务应对接软件、数字贸易与服务，而非默认跨境卖货','杭州市2026年经济政策框架','2026年版政策解读；不推定2027年延续','出海服务站',
'''2026年官方解读提及软件、数字贸易、文化出海等方向，并支持钱塘出海服务港、余杭出海服务站建设。框架支持并不能证明某个站点已经开放全部服务或本公司已具备补助资格。''',
'''出海App、订阅SaaS、广告内容、游戏或文化产品，应按<strong>真实产品、收入方式与主体</strong>分别匹配。货物跨境电商政策不能不加区分地套给软件订阅。''',
'''拿一页业务介绍去问商务/经信：对应哪类服务贸易或软件事项？海外合同、平台结算、外汇收款能否作为材料？是否已有面向小团队的服务清单和当前窗口？''',['S11'],'年度方向；具体申报与服务可用性待核')
policy('P14','创业','创新型中小企业：有积累再申报，先确认通知中的版本冲突','浙江注册独立法人等；滨江区受理通知','2026-09-24发布；10月20日17:00截止','独立法人资格',
'''通知面向符合条件的企业开展评价申报及复核，外省迁入按新申报处理。创新型评价与专精特新奖励不是同一事项。正文引用2026年文件，同时又出现旧标准及2021—2023年表述，存在需核对之处。''',
'''这是已经有产品、研发和经营资料的公司可核验的路径，<strong>不是刚搬来注册一家公司就自动拿20万元</strong>，也不应为赶窗口仓促改变现有主体。''',
'''向滨江经信局0571-89520447 / 89520448确认当期标准、迁入处理与材料版本后，再使用官方平台申报。''',['S16'],'当前窗口；标准表述须先确认')

OUT.joinpath('sources.json').write_text(json.dumps({'as_of':AS_OF,'coverage':'家庭迁居核心相关政策与办事入口，非全量政策库','sources':SOURCES},ensure_ascii=False,indent=2),encoding='utf-8')
OUT.joinpath('policy_annotations.json').write_text(json.dumps({'as_of':AS_OF,'policies':POLICIES},ensure_ascii=False,indent=2),encoding='utf-8')

cards=[]
for p in POLICIES:
    cards.append(f'''<article class="policy" id="{p['id']}" data-category="{p['category']}">
<div class="policy-top"><span class="policy-no">{p['id']}</span><span class="tag">{p['category']}</span><span class="status">{p['status']}</span></div>
<h3>{p['title']}</h3><p class="meta">{p['scope']}<br>{p['date']}</p>
<div class="quote"><span class="eyebrow">原文关键词</span><mark>{p['quote']}</mark></div>
<div class="readline"><span class="mini-label">条款要点</span><p>{p['reading']} {refs(*p['sources'])}</p></div>
<div class="meaning"><span class="mini-label">对这家人的含义</span><p>{p['meaning']}</p></div>
<details><summary>办理前要确认什么</summary><p>{p['action']}</p></details>
<div class="source-links">{original(*p['sources'])}</div></article>''')

rows=[]
for s in SOURCES:
    cls='media' if s['kind']=='媒体转引政策' else ('entry' if '入口' in s['kind'] or '栏目' in s['kind'] else '')
    rows.append(f'''<article class="source-item {cls}" id="src-{s['id']}"><div class="source-head"><span class="source-no">{s['id']}</span><span class="tag">{s['kind']}</span></div><h4><a href="{s['url']}" target="_blank" rel="noopener noreferrer">{s['title']} ↗</a></h4><p>{s['issuer']} · {s['published']}</p><p><strong>核验状态：</strong>{s['status']}。</p><p><strong>适用范围：</strong>{s['scope']}。</p><a class="url" href="{s['url']}" target="_blank" rel="noopener noreferrer">{s['url']}</a></article>''')

CHECKS=[
('grades','分别填好孩子现年级、出生年月、学籍地、拟迁入学期。'),
('hukou','核清夫妻和孩子的实际户籍，而不是把“住在西安”直接当作陕西户籍。'),
('exam','初中孩子未来高中报考类别、连续学籍及名额分配条件已获主管部门答复。'),
('school','小学和初中分别有可执行的接收路径；不把中介口头承诺当录取。'),
('permit','儿童居住证、家长证件、社保与租赁备案的办理条件及时间已确认。'),
('siblings','两孩接送距离、多孩协调和备用接收方案已核对。'),
('lease','房东配合登记、备案、材料出具及租约退出条件已写入可审阅的约定。'),
('business','区分现有西安公司迁入、新设杭州公司及个人经营，责任与成本已比较。'),
('subsidy','拟申请项目的主体、人群、地址、费用、时限和兑现方式已书面核验。'),
('wife','妻子的求职方向、资格证明、试用期与社保安排已纳入计划。'),
('runway','按不拿补贴计算家庭与业务现金流；搬家和往返成本已计入。'),
('handoff','接收手续明确后再与原学校依法衔接，不提前中断实际就读。')
]
check_html=''.join(f'<label class="check-row"><input type="checkbox" data-check="{i}"><span>{t}</span></label>' for i,t in CHECKS)

CSS=r'''
:root{--ink:#142e35;--muted:#607179;--navy:#102e38;--teal:#007d79;--mint:#e6f3ed;--paper:#f5f5ee;--white:#fff;--line:#dce4de;--amber:#ffd889;--red:#a93437;--rose:#fff0ec;--radius:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif;font-size:15px;line-height:1.8}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}button,input,select,textarea{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--amber);outline-offset:3px}::selection{background:#ffe2a7}.wrap{max-width:1480px;margin:auto;display:grid;grid-template-columns:244px minmax(0,1fr);gap:42px;padding:30px 40px 60px}.sidebar{position:sticky;top:25px;align-self:start;max-height:calc(100vh - 50px);overflow:auto}.brand{font-weight:800;font-size:19px;letter-spacing:.03em}.brand span{display:block;font-size:11px;color:var(--muted);letter-spacing:.17em;margin-top:4px}.side-line{height:3px;width:36px;background:var(--teal);margin:24px 0}.sidebar nav{display:grid;gap:3px}.sidebar nav a{padding:8px 10px;border-radius:8px;color:var(--muted);font-size:13px}.sidebar nav a:hover,.sidebar nav a.active{background:var(--mint);color:var(--teal);text-decoration:none}.sidebar nav b{display:inline-block;width:26px;font-size:11px;opacity:.6}.side-note{font-size:12px;color:var(--muted);border-top:1px solid var(--line);margin-top:24px;padding-top:18px}.side-note strong{color:var(--ink)}main{min-width:0}.topline{display:flex;align-items:center;justify-content:space-between;gap:15px;margin-bottom:22px}.kicker{font-size:11px;font-weight:750;letter-spacing:.13em;color:var(--teal)}.date{font-size:12px;color:var(--muted)}.btn{border:1px solid var(--line);background:white;color:var(--ink);border-radius:9px;padding:8px 14px;font-size:13px;line-height:1.5}.btn.primary{background:var(--teal);color:white;border-color:var(--teal)}.btn:hover{filter:brightness(.96)}.hero{background:var(--navy);color:#fff;border-radius:23px;overflow:hidden;padding:46px 44px 0;position:relative}.hero .kicker{color:#9ed9c9}.hero h1{font-size:clamp(27px,3vw,43px);line-height:1.35;letter-spacing:-.03em;margin:17px 0 20px}.hero h1 span{color:#aadccd}.hero p{color:#d3e0e2;font-size:15px;max-width:730px;margin:0 0 28px}.hero-flow{border-top:1px solid #37515a;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;padding:21px 0 24px}.hero-flow small{display:block;color:#97bcbf;font-size:10px;letter-spacing:.1em}.hero-flow strong{font-size:15px;font-weight:600}.hero-no{position:absolute;right:28px;top:20px;font-size:90px;font-weight:800;opacity:.045;line-height:1}.notice{background:var(--rose);border-left:4px solid var(--red);border-radius:0 12px 12px 0;padding:19px 22px;margin:22px 0 34px}.notice strong{color:var(--red)}.notice p{margin:3px 0;font-size:14px}.notice.neutral{background:var(--mint);border-color:var(--teal)}.notice.neutral strong{color:var(--teal)}section{margin:50px 0;scroll-margin-top:24px}.section-head{display:flex;align-items:baseline;gap:13px;border-bottom:1px solid var(--line);padding-bottom:13px;margin-bottom:22px}.section-no{font-size:12px;letter-spacing:.12em;color:var(--teal);font-weight:800}h2{font-size:25px;line-height:1.45;margin:0;letter-spacing:-.035em}h3{font-size:18px;line-height:1.6;margin:0 0 12px}h4{font-size:15px;line-height:1.6;margin:10px 0}p{margin:12px 0}strong{font-weight:700}.lead{font-size:18px;line-height:1.9;margin:0 0 20px}.subtle{font-size:13px;color:var(--muted)}.two-col{display:grid;grid-template-columns:1fr 1fr;gap:20px}.panel{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:24px}.panel.soft{background:var(--mint);border-color:transparent}.panel p:last-child{margin-bottom:0}.label{display:inline-block;font-size:11px;font-weight:750;letter-spacing:.1em;color:var(--teal);margin-bottom:9px}.pill{display:inline-block;background:var(--mint);color:var(--teal);border-radius:999px;padding:2px 9px;font-size:11px;margin:0 3px 3px 0}.pill.warn{background:#fff0d1;color:#8d5c18}.pill.danger{background:var(--rose);color:var(--red)}.cite{font-size:11px;vertical-align:super;line-height:0;font-weight:700;margin-left:3px;white-space:nowrap}.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:white}table{border-collapse:collapse;width:100%;font-size:13px;min-width:680px}th{background:#e9efea;color:#344e54;text-align:left;font-size:12px;font-weight:700}th,td{padding:15px 16px;border-bottom:1px solid var(--line);vertical-align:top}tr:last-child td{border-bottom:none}td:first-child{font-weight:700}td p{margin:5px 0}ul,ol{padding-left:22px;margin:10px 0}li{padding-left:1px;margin:7px 0}.routes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:20px}.route{background:white;border:1px solid var(--line);border-top:4px solid var(--teal);border-radius:12px;padding:22px 21px}.route .route-label{font-size:11px;color:var(--teal);letter-spacing:.05em}.route p{font-size:13px;margin:10px 0}.route h3{font-size:18px;margin-top:8px}.route .boundary{font-size:12px;background:#f5f5ee;border-radius:8px;padding:12px}.red-text{color:var(--red)}.flow-steps{counter-reset:steps;display:grid;gap:12px}.flow-step{background:white;border:1px solid var(--line);border-radius:12px;padding:17px 20px 17px 62px;position:relative}.flow-step:before{counter-increment:steps;content:counter(steps);position:absolute;left:20px;top:21px;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:var(--mint);color:var(--teal);font-size:12px;font-weight:bold}.flow-step p{font-size:13px;margin:4px 0}.filterbar{display:flex;align-items:center;gap:10px;background:#e9efea;padding:13px;border-radius:12px;margin:20px 0}.filterbar input{width:100%;min-width:0;border:1px solid #cdd8d3;background:white;border-radius:8px;padding:9px 12px;font-size:13px}.filterbar select{border:1px solid #cdd8d3;background:white;border-radius:8px;padding:9px;font-size:13px}.filter-count{font-size:12px;color:var(--muted);white-space:nowrap}.policies{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}.policy{background:white;border:1px solid var(--line);border-radius:var(--radius);padding:23px;scroll-margin-top:25px}.policy-top{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-bottom:13px}.policy-no{font:750 11px/1.5 ui-monospace,monospace;color:var(--muted)}.tag{background:#edf2ee;padding:2px 7px;border-radius:5px;font-size:10px;line-height:1.7;color:#4e686d}.status{font-size:10px;color:#866020;flex-basis:100%;margin-top:1px}.policy h3{font-size:18px;margin:8px 0}.meta{font-size:11px;line-height:1.7;color:var(--muted);margin:9px 0 15px}.quote{background:#fff8e6;border-left:3px solid #e5b450;padding:10px 13px;margin:14px 0}.eyebrow{font-size:10px;display:block;color:#8a723e;margin-bottom:4px}mark{background:#ffe19b;color:#453b24;border-radius:3px;padding:1px 3px;font-size:15px;font-weight:650}.mini-label{display:block;color:var(--teal);font-size:11px;font-weight:750;letter-spacing:.04em;margin-top:16px}.policy p{font-size:13px;line-height:1.85}.meaning{border-top:1px solid #edf1ed;margin-top:13px}.meaning p{margin-top:7px}.policy details{background:#f5f7f3;border-radius:9px;padding:10px 12px;margin:14px 0}.policy details p{margin:10px 0 0;color:#4e646b}.policy summary{cursor:pointer;font-size:12px;font-weight:650;color:var(--teal)}.source-links{display:flex;flex-wrap:wrap;gap:7px;border-top:1px solid #edf1ed;padding-top:14px;margin-top:13px}.original{font-size:11px;color:var(--teal);border-bottom:1px solid #bbd4c8}.empty{display:none;background:white;border:1px dashed var(--line);padding:25px;text-align:center;color:var(--muted)}.platform-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.platform-card{border:1px solid var(--line);background:white;border-radius:14px;padding:22px}.platform-card p{font-size:13px}.platform-card .phone{display:block;font-size:15px;font-weight:700;margin-top:10px;font-variant-numeric:tabular-nums}.platform-card h3{font-size:17px}.phone small{font-size:12px;font-weight:400}.address{font-size:12px;background:#f4f6f1;border-radius:6px;padding:9px 12px}.contact-table{font-size:13px}.check-tools{display:flex;justify-content:space-between;gap:10px;align-items:center;margin:16px 0}.check-progress{font-size:12px;color:var(--teal);font-weight:700}.check-list{display:grid;grid-template-columns:1fr 1fr;gap:9px 15px}.check-row{display:flex;gap:10px;background:white;border:1px solid var(--line);padding:12px 13px;border-radius:9px;font-size:13px;align-items:start;cursor:pointer}.check-row input{accent-color:var(--teal);width:17px;height:17px;flex:0 0 17px;margin-top:4px}.check-row.checked{background:#e9f3eb;color:#466658}.steps-list{list-style:none;padding:0;display:grid;gap:12px}.steps-list li{background:white;border-left:3px solid var(--teal);padding:17px 20px;margin:0;border-radius:0 10px 10px 0;font-size:13px}.steps-list b{display:block;font-size:15px;margin-bottom:4px}.budget-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.budget-grid label{font-size:12px;display:block;color:var(--muted)}.budget-grid input{display:block;width:100%;border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-top:7px;background:white;color:var(--ink);font-size:15px}.budget-total{display:flex;gap:32px;flex-wrap:wrap;margin-top:22px;padding:20px 22px;background:var(--navy);color:white;border-radius:12px}.budget-total small{display:block;font-size:11px;color:#a8c5c8}.budget-total strong{display:block;font-size:25px;font-variant-numeric:tabular-nums}.budget-total p{font-size:12px;margin:5px 0 0;color:#d0e0df}.copy-card{padding:23px;border:1px solid var(--line);background:white;border-radius:14px;margin:14px 0}.copy-head{display:flex;justify-content:space-between;gap:15px;align-items:center}.copy-head h3{margin:0}.copy-text{white-space:pre-wrap;line-height:1.85;font-size:13px;color:#38545d;margin-top:16px}.source-list{display:grid;grid-template-columns:1fr 1fr;gap:12px}.source-item{background:white;border:1px solid var(--line);border-radius:12px;padding:19px;scroll-margin-top:25px}.source-head{display:flex;gap:7px;align-items:center}.source-no{font:700 11px ui-monospace,monospace;color:var(--teal)}.source-item h4{margin:9px 0;font-size:14px}.source-item p{font-size:11px;color:var(--muted);line-height:1.8;margin:6px 0}.source-item .url{font-size:10px;line-height:1.6;display:block;overflow-wrap:anywhere;color:#728987;margin-top:8px}.source-item.media{border-left:3px solid #daa652}.source-item.entry{background:#f9fbf7}.gap-list{font-size:13px}.gap-list li{margin:10px 0}.footer{border-top:1px solid var(--line);padding-top:24px;font-size:11px;color:var(--muted);margin-top:36px;display:flex;justify-content:space-between;gap:20px}.mobile-nav{display:none}.toast{position:fixed;bottom:25px;left:50%;transform:translateX(-50%);z-index:20;background:var(--navy);color:white;padding:12px 22px;border-radius:10px;font-size:13px;box-shadow:0 8px 24px #102e3820;display:none;max-width:90vw}.nowrap{white-space:nowrap}.notes-field{width:100%;min-height:115px;border:1px solid var(--line);border-radius:10px;padding:13px;background:white;font-size:13px;color:var(--ink);resize:vertical}.sr-only{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(min-width:1500px){.wrap{gap:55px}}
@media(max-width:1150px){.wrap{grid-template-columns:195px minmax(0,1fr);gap:27px;padding:25px}.sidebar nav a{font-size:12px;padding:7px}.hero{padding:36px 30px 0}.routes{grid-template-columns:1fr}.route{display:grid;grid-template-columns:180px 1fr;column-gap:20px}.route .boundary{grid-column:1/-1}.route p{margin:8px 0}.route h3{margin:4px 0}.hero h1{font-size:35px}.policies{gap:14px}.policy{padding:19px}}
@media(max-width:860px){.wrap{display:block;padding:20px 22px 40px}.sidebar{display:none}.mobile-nav{display:flex;overflow-x:auto;gap:6px;white-space:nowrap;margin:0 -2px 18px;padding-bottom:6px}.mobile-nav a{font-size:11px;padding:6px 11px;background:#e6ece5;border-radius:6px;color:var(--teal)}.hero h1{font-size:34px}.hero-flow{gap:10px}section{margin:40px 0}.source-list{gap:10px}.topline{margin-bottom:15px}}
@media(max-width:590px){body{font-size:14px}.wrap{padding:15px 16px 35px}.topline{align-items:start}.kicker{font-size:10px;letter-spacing:.06em}.date{font-size:10px}.hero{padding:29px 23px 0;border-radius:18px}.hero h1{font-size:28px;letter-spacing:-.045em}.hero p{font-size:13px;margin-bottom:22px}.hero-flow{gap:10px;padding:17px 0}.hero-flow strong{font-size:12px}.hero-flow small{font-size:9px}.notice{padding:16px;margin:18px 0 25px}.notice p{font-size:13px}.section-head{gap:10px;margin-bottom:18px}h2{font-size:22px}.lead{font-size:16px}.two-col,.policies,.platform-grid,.source-list,.check-list{grid-template-columns:1fr}.panel{padding:21px}.policy{padding:21px}.filterbar{flex-wrap:wrap;padding:10px}.filterbar input{flex:1 1 100%}.filterbar select{flex:1}.filter-count{flex:1;text-align:right}.route{display:block}.route .boundary{margin-bottom:0}.budget-grid{grid-template-columns:1fr 1fr;gap:12px}.budget-total{gap:20px;padding:18px}.budget-total strong{font-size:23px}.source-item{padding:18px}.copy-card{padding:19px}.copy-head{align-items:start}.copy-head h3{font-size:16px}.copy-head .btn{flex-shrink:0;font-size:11px;padding:7px 10px}.check-tools{flex-wrap:wrap}.footer{display:block}.policy-top .status{font-size:10px}.mobile-nav{margin-bottom:12px}.btn{font-size:12px}section{margin:35px 0}}
@media print{@page{size:A4;margin:14mm 13mm}html{scroll-behavior:auto}body{background:white;font-size:10pt;color:#172e32;line-height:1.55}.wrap{display:block;max-width:none;padding:0}.sidebar,.mobile-nav,.no-print,.filterbar,.toast{display:none!important}.hero{background:#102e38!important;color:white!important;padding:24px 27px 0;-webkit-print-color-adjust:exact;print-color-adjust:exact}.hero h1{font-size:29pt}.hero p{font-size:10pt}.hero-flow{padding:13px 0}.topline{margin-bottom:14px}.notice{break-inside:avoid;-webkit-print-color-adjust:exact;print-color-adjust:exact}.notice p{font-size:10pt}section{margin:26px 0}h2{font-size:18pt}h3{font-size:13pt}h2,h3,h4{break-after:avoid}.section-head{margin-bottom:13px;padding-bottom:8px}.policies,.source-list,.platform-grid{display:block}.policy{display:block!important;break-inside:avoid;margin:13px 0;padding:17px}.policy p{font-size:10pt}.policy h3{font-size:14pt}.policy details{display:block!important}.policy details>p{display:block!important}.policy .quote{margin:10px 0}.source-item{margin:9px 0;break-inside:avoid}.source-item p{font-size:8pt}.source-item .url{font-size:7pt}.source-item h4{font-size:10pt}.routes{grid-template-columns:1fr}.route{display:block;break-inside:avoid;margin-bottom:10px}.platform-card{break-inside:avoid;margin:10px 0}.two-col{gap:12px}.panel{padding:16px;break-inside:avoid}table{min-width:0;font-size:9pt}th,td{padding:9px}.table-wrap{overflow:visible}.check-row{font-size:9pt;break-inside:avoid;padding:8px}.check-list{gap:7px}.copy-card{break-inside:avoid}.copy-text{font-size:9pt}.budget-total{background:#eef4ee!important;color:#142e35!important}.budget-total small,.budget-total p{color:#4e6367!important}.footer{font-size:8pt}.lead{font-size:12pt}a{color:#007d79}mark{background:#ffe19b!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}.meta{font-size:8pt}.tag,.status{font-size:8pt}}
'''

HEADER='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="西安家庭迁居杭州的教育、转学、落户、出海创业政策解读与官方入口，核验截至2026年9月28日。"><title>西安 → 杭州｜家庭迁居与出海创业政策手册</title><style>'''+CSS+'''</style></head><body><a class="sr-only" href="#main">跳到正文</a><div class="wrap"><aside class="sidebar"><div class="brand">杭州 · 家庭迁居<span>FAMILY & FOUNDER FIELD GUIDE</span></div><div class="side-line"></div><nav aria-label="目录">
<a href="#decision"><b>01</b>先看判断</a><a href="#family"><b>02</b>家庭前提</a><a href="#districts"><b>03</b>住在哪里</a><a href="#education"><b>04</b>孩子升学路径</a><a href="#policies"><b>05</b>政策逐条划重点</a><a href="#platforms"><b>06</b>平台与办理入口</a><a href="#wife"><b>07</b>妻子的工作安排</a><a href="#checklist"><b>08</b>签约前确认清单</a><a href="#timeline"><b>09</b>搬迁顺序与时间</a><a href="#budget"><b>10</b>家庭成本试算</a><a href="#questions"><b>11</b>可复制的咨询话术</a><a href="#sources"><b>12</b>原文库与核验边界</a></nav><div class="side-note"><strong>核验截至 2026.09.28</strong><br>14 张政策解读卡<br>24 条来源与办事入口<br><br>黄色：原文关键词<br>红色：影响搬家决定的风险<br>绿色：建议的核验动作<br><br>单文件离线可读。<br>打开原文及政务平台需联网。</div></aside><main id="main"><div class="topline"><div><div class="kicker">西安 → 杭州 · 租房 / 教育 / 出海创业</div><div class="date">政策核验版 · 2026年9月28日 · v1.0</div></div><button class="btn no-print" id="printBtn">打印 / 存为 PDF</button></div><nav class="mobile-nav no-print" aria-label="移动端目录"><a href="#decision">先看判断</a><a href="#education">孩子升学</a><a href="#policies">政策重点</a><a href="#platforms">办理入口</a><a href="#sources">原文库</a></nav><header class="hero"><div class="hero-no" aria-hidden="true">HZ</div><div class="kicker">给一个准备全家迁居的创业家庭</div><h1>先定孩子升学，<br><span>再定创业落点。</span></h1><p>父亲做出海 App、SaaS 与自媒体；母亲有民办学校任教经历；孩子涉及小学和初中。这里把“可以住”“可以读”“可以创业”“可以申请补助”四件事分开核验。</p><div class="hero-flow"><div><small>STEP 01</small><strong>学校与高中报考</strong></div><div><small>STEP 02</small><strong>真实居住与户籍</strong></div><div><small>STEP 03</small><strong>公司与创业支持</strong></div></div></header>'''

BODY=f'''
<div class="notice"><p><strong>先别用“在哪个区补贴高”决定全家搬迁。</strong></p><p>初中孩子转学后能否按相应资格报考杭州高中，必须先核实。2026年部分市区报考路径要求连续初中学习经历和学籍；余杭不能直接套用该招生范围。{refs('S05')}</p></div>

<section id="decision"><div class="section-head"><span class="section-no">01</span><h2>给这家人的可执行判断</h2></div>
<p class="lead">先让父亲验证业务与居住环境；全家是否同步搬，取决于两个孩子是否都有明确、连续的就读方案。</p>
<div class="two-col"><div class="panel soft"><span class="label">居住与创业 · 两条线同时查</span><h3>城西与滨江都列入考察，不急着定唯一答案</h3><p>余杭五常、仓前 / 未来科技城可作为城西工作生活候选；滨江长河、西兴可作为另一组候选。选择依据是<strong>孩子接收结果、真实合作对象、妻子工作和总通勤</strong>，不是大额政策标题。</p><p class="subtle">城西有专项资金框架，滨江有已核到的数字贸易与小团队AI支持文件；这些是核验入口，并不证明本家庭能获资助。{refs('S10','S12','S17')}</p></div><div class="panel"><span class="label">搬家方式 · 先保留回旋余地</span><h3>初中孩子资格未明，先试住，不先中断学业</h3><p>我的方案是：父亲先短期考察或试住，孩子维持真实、连续的现有就读；收到接收与未来升学资格答复后，再安排正式长租和转学。</p><p>这不是建议长期两地分居，而是避免先退租、辞职、转出学籍，最后才发现目标路径走不通。</p></div></div>
<p class="subtle">这里是基于已知家庭情况的决策建议，不是教育部门的录取意见。夫妻实际户籍、孩子年级及家庭预算尚不明，不能据此宣布某个区“保证最合适”。</p></section>

<section id="family"><div class="section-head"><span class="section-no">02</span><h2>先把会改变方案的前提写清楚</h2></div>
<div class="table-wrap"><table><thead><tr><th style="width:18%">事项</th><th style="width:38%">目前知道什么</th><th>还要确认什么，为什么重要</th></tr></thead><tbody>
<tr><td>父亲业务</td><td>有出海App经历，继续做SaaS、自媒体等。</td><td>是否有现成公司、真实AI产品、员工、研发和收入证明；决定能匹配哪类服务或申报。</td></tr>
<tr><td>母亲工作</td><td>曾在民办学校任教，目前未确定下一份工作。</td><td>学科、学段、学历、教师资格、职称、英语及合同诉求。不能把任教经历当人才认定结果。</td></tr>
<tr><td>孩子</td><td>涉及小学和初中。</td><td>逐个填写现年级、学籍、出生年月、拟迁学期；尤其确认是升初一，还是初中插班。</td></tr>
<tr><td>户籍与证件</td><td>目前在西安生活。</td><td><strong>生活地不等于户籍地。</strong>逐一核对实际户籍、浙江居住证、人才居住证及杭州社保。</td></tr>
<tr><td>家庭与预算</td><td>考虑全家租房常驻。</td><td>家庭人数、卧室需求、教育支出、可承受月支出、现金储备及搬迁时点均待补齐。</td></tr>
</tbody></table></div>
<div class="notice neutral"><p><strong>把四个“地址”分开：</strong>实际居住地决定日常生活与相应居住材料；户籍地关联具体招生类别；公司注册/经营地影响惠企事项；社保缴纳地影响某些资格。它们不能互相替代。具体教育和创业条件见下方对应文件。{refs('S04','S07','S08','S13')}</p></div></section>

<section id="districts"><div class="section-head"><span class="section-no">03</span><h2>区域方案：每一组都有明确的成立条件</h2></div>
<p>下面是<strong>居住考察方案，不是学校质量排名，也不是政策优劣评分</strong>。先拿到孩子的办理路径，再比较小区和办公室。</p>
<div class="routes">
<article class="route"><div><div class="route-label">方案 A · 城西工作生活候选</div><h3>余杭：五常 / 仓前 / 未来科技城</h3></div><div><p><strong>适用前提：</strong>实际合作对象或办公需求在城西，两个孩子均能按余杭当期规则接收，预算与接送距离合适。</p><p><strong>创业先问：</strong>园区给出海软件小团队提供什么具体服务？余杭出海服务站建设相关政策如何落到当前可用服务？{refs('S10','S11')}</p></div><p class="boundary"><strong>关键空白：</strong>本次未可靠取得余杭最新转学及高中招生细则，因此不能把它写成“孩子上学已解决”的推荐。先经12345转余杭教育、招生及企业服务部门确认。</p></article>
<article class="route"><div><div class="route-label">方案 B · 数字业务与条件型AI创业</div><h3>滨江：长河 / 西兴</h3></div><div><p><strong>适用前提：</strong>业务伙伴、岗位或办公室实际在滨江；孩子接收与高中报考类别已核实。</p><p><strong>创业先问：</strong>普通出海产品咨询数字贸易、软件服务与陪跑空间；确有AI产品的小团队，再核AI+OPC入库。{refs('S12','S13','S17','S18')}</p></div><p class="boundary"><strong>已核到：</strong>区级转学入口、教育咨询电话与工位政策解读。但有公开流程，不代表有空位，也不代表家庭已经满足条件。{refs('S06')}</p></article>
<article class="route"><div><div class="route-label">方案 C · 由学校或工作位置反推</div><h3>西湖：蒋村 / 三墩</h3></div><div><p><strong>适用前提：</strong>已经有明确的孩子接收路径，或母亲工作、父亲办公就在附近，且家庭能承受实际总成本。</p><p><strong>创业先问：</strong>具体企业地址是否位于相应园区或专项资金范围，不能把全区都当成同一扶持范围。{refs('S10')}</p></div><p class="boundary"><strong>不要预设：</strong>“租西湖、用余杭资源、直接享名校学位”不是可兑现的组合承诺。租房类别和学位仍按具体文件与实际审核处理。{refs('S04')}</p></article>
</div>
<div class="panel" style="margin-top:18px"><span class="label">我会怎么组织第一次实地看房</span><p>每组只选两套真正满足居住需求的房子，实测<strong>早晚接送两校 + 常用办公点</strong>的完整路线；不先花一天只看小区景观。地址附近的学校，只有获得接收确认后才算可用学校。</p><p>妻子工作未定时，不宜为了父亲每月几场活动让全家每天承担长通勤。若家庭住处和公司分属两区，分别核教育与创业规则，不假设两边条件可以拼接。</p><p class="subtle">本次没有核验具体房源、成交租金或实时通勤，因此不提供“某小区三房多少钱、几分钟直达”的虚假精度。</p></div></section>

<section id="education"><div class="section-head"><span class="section-no">04</span><h2>两个孩子，各自走完一条完整路径</h2></div>
<div class="flow-steps">
<div class="flow-step"><h3>先定“新生”还是“转学生”</h3><p>小学一年级新生 → P01；外地小学毕业升初一 → P02；小学或初中已经在读 → P03及目标区转学规则。不能互相替用。</p></div>
<div class="flow-step"><h3>再定“本家庭属于哪个资格类别”</h3><p>分别核孩子户籍、儿童居住证、家长人才居住证等可用路径；不要只问“租房能不能读”，要提交一个完整的家庭事实组合。{refs('S02','S03','S07')}</p></div>
<div class="flow-step"><h3>有初中孩子，就同步问高中报考</h3><p>把“是否可转入”“是否能按相应类别报考高中”“是否有名额分配资格”拆成三问；初二、初三尤其不应只拿小学招生问答判断。详细证据见P05。</p></div>
<div class="flow-step"><h3>最后核具体学校、学位、窗口和原校衔接</h3><p>接收资格不等于指定学校名额。以拟迁学期公告和真实学位审核为准，接收明确后再与原校依法衔接，不做挂靠或虚构就读经历。</p></div>
</div>
<div class="table-wrap" style="margin-top:20px"><table><thead><tr><th>孩子实际阶段</th><th>先拿到什么答复</th><th>更稳妥的家庭动作</th></tr></thead><tbody>
<tr><td>小学低中年级在读</td><td>目标区转学资格、该年级空位、材料与时间。</td><td>家长先考察，等接收路径清楚再转出。</td></tr>
<tr><td>小学六年级，准备初一</td><td>外地小学毕业生升初的报名类别；从初一起就读后的升学路径。</td><td>把搬迁时间与下一次正式新生招生对齐，而不是临时插班替代升初。</td></tr>
<tr><td>初一在读</td><td>已在西安就读部分如何影响目标招生范围的连续学籍要求。</td><td>不得假定“总共读满三年初中”就是“在规定范围连续三年”。</td></tr>
<tr><td>初二 / 初三</td><td>高中报考类别与可行路径的明确核验；名额分配条件另问。</td><td>暂不以全家立即迁居作为默认方案。教育路径不明确时，父亲先行测试更可逆。</td></tr>
</tbody></table></div>
<p class="subtle">上述是核验与搬迁建议，不是对任一孩子报考资格的个案裁定。升学规则依据拟毕业年度执行，2026年的规定只能作为当前风险识别依据。{refs('S05')}</p></section>

<section id="policies"><div class="section-head"><span class="section-no">05</span><h2>政策逐条划重点</h2></div>
<p>每张卡按<strong>原文关键词 → 条款要点 → 对本家庭的含义 → 办理前核验</strong>展开。黄色仅标记原文短语；其余是转述和判断，不把解读伪装成原文。</p>
<div class="filterbar no-print"><label class="sr-only" for="policySearch">搜索政策</label><input id="policySearch" type="search" placeholder="搜索：初中、租金、AI、居住证、余杭……"><label class="sr-only" for="categoryFilter">选择类别</label><select id="categoryFilter"><option value="全部">全部类别</option><option value="教育">教育</option><option value="户籍">户籍</option><option value="创业">创业</option></select><span class="filter-count" id="filterCount">14 / 14 条</span><button class="btn" id="expandBtn">展开办理提示</button></div>
<div class="policies">{''.join(cards)}</div><div id="empty" class="empty">没有匹配的解读卡，请换一个关键词。完整原文库仍在本页底部。</div>
</section>

<section id="platforms"><div class="section-head"><span class="section-no">06</span><h2>平台与联系人：先找到“能办事的人”</h2></div>
<p>这里优先提供官方平台和有官方活动记录的空间，不按招商宣传里的补助金额选园区。<strong>政府栏目列出过活动 ≠ 当前一定有空工位；陪跑空间 ≠ 自动属于AI+OPC创建社区。</strong>{refs('S08','S13','S18')}</p>
<div class="platform-grid">
<div class="platform-card"><span class="label">企业政策申报</span><h3><a href="https://qinqing.hangzhou.gov.cn/" target="_blank" rel="noopener noreferrer">亲清在线 ↗</a></h3><p>用实际杭州主体筛具体政策，核申报期、主管部门、注册经营和材料要求。入口已确认，但本次没有登录任何企业账户，也没有拿到他们的可申报列表。{refs('S21')}</p><p class="subtle">咨询时带：一页产品介绍、现有公司信息、实际业务及收入方式、员工和社保情况、拟经营地址。</p></div>
<div class="platform-card"><span class="label">入学、证件及综合办事</span><h3><a href="https://www.zjzwfw.gov.cn/" target="_blank" rel="noopener noreferrer">浙里办 / 浙江政务服务网 ↗</a></h3><p>招生文件指向“义务教育阶段学校学生入学一件事联办”等入口；另按真实事项查询居住登记、居住证和落户。选择正确区和学年后办理。{refs('S03','S24')}</p><span class="phone">12345 <small>无法定位主管单位时，请转目标区教育、公安或企业服务部门</small></span></div>
<div class="platform-card"><span class="label">滨江 · 学校与转学</span><h3><a href="https://www.hhtz.gov.cn/col/col1229565992/index.html" target="_blank" rel="noopener noreferrer">滨江教育服务栏目 ↗</a></h3><p>转学可从“滨江教育发布”菜单进入，或使用通知中的申请系统。先读申请须知，再查拟转年级学位，不把已关闭的2026年窗口当成当前开放。{refs('S06','S20')}</p><span class="phone"><a href="tel:057189520760">0571-89520760</a> / <a href="tel:057189520740">89520740</a></span><p class="subtle">官方转学通知公开的区教育局电话；电话沟通不等于已作出录取决定。</p></div>
<div class="platform-card"><span class="label">西湖 · 教育资格咨询</span><h3>先问所属类别，再问租哪套房</h3><p>西湖教育网学校方案公开了区级招生咨询电话。具体转学和目标校空位需要另核，不能用行知小学一年级方案包办所有情况。{refs('S04')}</p><span class="phone"><a href="tel:057189511751">0571-89511751</a> / <a href="tel:057189511752">89511752</a></span><p class="subtle">余杭本次未核得可靠的对应直线号码，使用12345转接并索取当期正式通知，避免提供未经验证的号码。</p></div>
<div class="platform-card"><span class="label">滨江 · 真实空间线索</span><h3>慧和创业陪跑空间</h3><p>2026年9月区人社活动表列有该空间的创业指导与企业培育服务，可询问后续咨询、工位、入驻和出海软件项目匹配情况。{refs('S18')}</p><div class="address">滨江区滨安路1180号1幢2号楼2层2102室（以活动表及当前运营方确认为准）</div><p class="subtle">活动记录是服务线索，不是入驻承诺；需要现行认定名单、合同、总费用和退出条款。</p></div>
<div class="platform-card"><span class="label">滨江 · 创业咨询线索</span><h3>创梦工场创业陪跑空间</h3><p>同一官方活动表列有创业融资和政策辅导。已列活动多数结束，可通过区就业创业栏目联系运营方询问新安排。{refs('S18','S19')}</p><div class="address">滨江区聚工路11号创伟科技园B座1楼</div><p class="subtle">女性创业、贷款或培训项目同样要先核条件；不要仅因妻子暂未就业就认定可领取。</p></div>
</div>
<div class="panel" style="margin-top:18px"><h3>滨江AI+OPC：按问题找对应部门</h3><div class="table-wrap"><table class="contact-table"><thead><tr><th>要解决的问题</th><th>公开联系人单位</th><th>电话</th></tr></thead><tbody>
<tr><td>社区、工位、培训</td><td>区科技局</td><td><a href="tel:057186691326">0571-86691326</a></td></tr>
<tr><td>Token、智能体、场景</td><td>区经信局</td><td><a href="tel:057189521408">0571-89521408</a></td></tr>
<tr><td>数据跨境服务</td><td>区商务局</td><td><a href="tel:057189520511">0571-89520511</a></td></tr>
<tr><td>人才公寓房租事项</td><td>区住建局</td><td><a href="tel:057189520926">0571-89520926</a></td></tr>
<tr><td>陪跑与政务服务</td><td>区审管办</td><td><a href="tel:057181187977">0571-81187977</a></td></tr>
<tr><td>云端产业园</td><td>高新科创集团</td><td><a href="tel:057186637726">0571-86637726</a></td></tr>
</tbody></table></div><p class="subtle">以上为2026年6月官方解读公开的业务电话，本次未实拨确认接听或个案结果。{refs('S13')}</p></div>
<div class="notice neutral"><p><strong>出海服务平台应该帮他们解决什么？</strong>不是只发一份补贴海报，而是能明确提供公司/财税对接、海外收款材料咨询、知识产权、数据与产品合规、客户或同行交流的哪些具体服务。请运营方给出服务清单、收费、顾问及已服务同类软件项目的可核实案例。</p><p>余杭出海服务站与滨江数字贸易信息可以作为咨询起点，但本次没有核验到所有服务的开放状态、价格和预约方式。{refs('S11','S17')}</p></div></section>

<section id="wife"><div class="section-head"><span class="section-no">07</span><h2>妻子的工作，不应等搬完家才考虑</h2></div>
<p>这部分是职业与家庭安排建议，不把她视作已经具备某项教师招聘、人才认定或创业补助资格。</p>
<div class="two-col"><div class="panel"><span class="label">路径一 · 继续任教</span><h3>用工作机会反推住房，不只跟着丈夫办公室走</h3><p>先做一页教师履历：学科、学段、教龄、学历、教师资格、职称、可授课程和到岗时间。直接核学校或教育部门招聘公告中的要求，再比较真实岗位。</p><p>面试时单独问清劳动合同、试用期、薪酬、社保、工作校区，以及是否有<strong>书面、适用于本人子女</strong>的安排。不能从“老师身份”推定孩子能入读任意学校。</p></div><div class="panel"><span class="label">路径二 · 教育相关产品或服务</span><h3>先小规模验证，不把夫妻同时创业当默认</h3><p>可把教研、课程运营、教育产品内容或客户支持列为候选方向；是否转型取决于能力、岗位和家庭现金流，不预设一定比任教收入高。</p><p>若参与丈夫业务，先写清具体职责、工时和报酬，避免一边承担全部接送，一边被默认“免费运营”。若计划经营教育培训，先向主管部门确认业务范围和所需资质。</p></div></div>
<p>招聘检索入口：<a href="https://www.hzrc.com/" target="_blank" rel="noopener noreferrer">杭州人才网 ↗</a>、<a href="https://www.hhrc.com.cn/" target="_blank" rel="noopener noreferrer">高新人才网 ↗</a>，再回到招聘单位正式公告核验。<strong>本次未核验具体学校在招职位、薪酬或子女优惠。</strong>{refs('S22','S23')}</p></section>

<section id="checklist"><div class="section-head"><span class="section-no">08</span><h2>签长租、转学和迁公司之前，逐项确认</h2></div>
<p>勾选仅表示材料或答复已确认，<strong>不是资格评分或录取审批</strong>。数据只尝试保存在当前浏览器；本页不向任何服务器上传。</p>
<div class="check-tools"><span class="check-progress" id="checkProgress">已确认 0 / 12 项</span><div><button class="btn no-print" id="exportChecks">导出确认记录</button> <button class="btn no-print" id="resetChecks">清空勾选</button></div></div><div class="check-list">{check_html}</div>
<div class="panel" style="margin-top:18px"><h3>看房时额外留意三件事</h3><p><strong>第一，证据能否办理。</strong>拿真实门牌向办理部门询问租赁备案、居住登记及入学材料，确认房东愿意配合。</p><p><strong>第二，失败时怎么退出。</strong>把可能的接收不成功、入学延后与租约如何处理交给双方协商，必要时由当地专业人士审阅，不靠口头“包上学”。</p><p><strong>第三，实际生活是否可持续。</strong>用可接收的两所学校实测通勤、接送与办公，而不是用最近的学校当路线终点。</p></div>
<label for="familyNotes" class="label" style="margin-top:22px">家庭记录（选填；不建议填写证件号码）</label><textarea class="notes-field" id="familyNotes" placeholder="例如：大孩初二，已向哪一区咨询；小孩四年级；主管部门答复日期、依据文件、尚缺材料……"></textarea></section>

<section id="timeline"><div class="section-head"><span class="section-no">09</span><h2>先后顺序，比“什么时候抢到便宜房子”更重要</h2></div>
<ol class="steps-list"><li><b>阶段1 · 远程核验</b>夫妻与孩子资料各一页；分别向候选区教育、户籍和企业服务部门提问。拿到缺件清单、适用类别、办理窗口及联系人。</li><li><b>阶段2 · 父亲实地试住和业务验证</b>考察实际接收学校周边住房、候选空间、合作伙伴；妻子同步面试。看一次活动不等于已有稳定创业资源。</li><li><b>阶段3 · 决定是否全家同步迁居</b>只有当学校与未来报考路径、住所材料、预算都能闭合，再确认长租和搬家；否则保留原安排，由成年人先行。</li><li><b>阶段4 · 正式入学、落户及企业衔接</b>按照各部门真实要求完成；保留合同、申请凭据、回执与费用凭证。公司迁入、新设或暂不迁各自核成本，不为重置年限而虚构经营事实。</li><li><b>阶段5 · 经营稳定后再申报</b>先形成真实研发、收入、社保及场地资料，再对照当期项目；把可能的补助当改善项，不当维持全家生活的必需收入。</li></ol>
<div class="table-wrap" style="margin-top:20px"><table><thead><tr><th>明确时间</th><th>截至2026-09-28的状态</th><th>这家人应如何使用</th></tr></thead><tbody>
<tr><td>2026年滨江暑假转学</td><td>申请7月1日—8月15日；已结束。{refs('S06')}</td><td>只参考流程；查下一学期通知，不能按旧入口开放推定还可正常补报。</td></tr>
<tr><td>2027年新生入学 / 转学</td><td>本次未取得正式日程。</td><td>先完成资格核验和真实证件准备，等待目标区发布，不填造日期。</td></tr>
<tr><td>AI+OPC政策</td><td>2026年7月25日起生效，有效期一年。{refs('S12')}</td><td>办理前再核政策是否延续、社区名录、入库和兑现窗口。</td></tr>
<tr><td>创新型中小企业当期申报</td><td>通知列2026年10月20日17:00截止。{refs('S16')}</td><td>仅已有材料且符合条件的企业核验；不建议为赶窗口仓促全家搬迁。</td></tr>
</tbody></table></div></section>

<section id="budget"><div class="section-head"><span class="section-no">10</span><h2>用自己的实际成本，做“零补贴”试算</h2></div>
<p>以下是算术工具，不是杭州市场报价，也不是消费建议。先填实际调查值；一次性成本不要和月度成本混在一起。<strong>补贴收入固定按0元处理。</strong></p>
<div class="budget-grid"><label>家庭住房 / 月（元）<input type="number" min="0" step="100" id="bRent" placeholder="填实际询价" inputmode="decimal"></label><label>教育与接送 / 月（元）<input type="number" min="0" step="100" id="bSchool" placeholder="学费摊月及接送" inputmode="decimal"></label><label>家庭生活 / 月（元）<input type="number" min="0" step="100" id="bLiving" placeholder="吃饭、水电等" inputmode="decimal"></label><label>办公及业务固定支出 / 月（元）<input type="number" min="0" step="100" id="bOffice" placeholder="工位、云服务等" inputmode="decimal"></label><label>社保及其他固定支出 / 月（元）<input type="number" min="0" step="100" id="bOther" placeholder="避免和上项重复" inputmode="decimal"></label><label>搬家及一次性支出（元）<input type="number" min="0" step="100" id="bMove" placeholder="搬运、往返、置办等" inputmode="decimal"></label><label>押金及暂时占用现金（元）<input type="number" min="0" step="100" id="bDeposit" placeholder="可退押金也占现金" inputmode="decimal"></label><label>测算覆盖月数<input type="number" min="1" max="36" step="1" id="bMonths" value="6" inputmode="numeric"></label></div>
<div class="budget-total" aria-live="polite"><div><small>每月固定支出</small><strong id="monthlyTotal">待填写</strong></div><div><small id="cashLabel">6个月无新增收入情景所需现金</small><strong id="cashTotal">待填写</strong></div><p>计算 = 月固定支出 × 月数 + 一次性支出 + 押金。未填项目在计算中暂按0；必须补齐后才能使用结果。</p></div>
<p class="subtle">“6个月”只是可修改的试算参数，不是该家庭必须持有的储备标准。可退押金属于现金占用，不计作永久成本；若学费按学期预缴，还需单独核对付款时点。</p></section>

<section id="questions"><div class="section-head"><span class="section-no">11</span><h2>把问题一次问完整</h2></div>
<p>以下可直接复制给主管部门或空间运营方。用实际情况替换方括号；重要结论尽量保留正式答复、回执或工单编号。</p>
<div class="copy-card"><div class="copy-head"><h3>发给区教育 / 招生部门</h3><button class="btn no-print" data-copy="qSchool">复制话术</button></div><div class="copy-text" id="qSchool">我们目前在西安生活，计划于[学年/学期]迁居杭州[区]并真实租住。夫妻户籍分别是[ ]；儿童户籍是[ ]；家长和孩子居住证情况为[ ]；杭州社保情况为[ ]。
小孩目前[小学几年级]，另一名孩子目前[初中几年级/小学六年级准备升初]，学籍均在[ ]。
请分别确认：
1. 属于新生招生还是转学？按哪个资格类别申请？需要哪些材料，何时办理？
2. 租赁备案、儿童居住证、落户完成时间各有什么要求？接收是否需要统筹？
3. 初中孩子将来报考当地高中适用哪一类资格？外地在读经历是否影响连续学籍条件？名额分配资格是否另有限定？
4. 若办理本区户籍，按何时的户籍状态认定？请不要仅按“能转学”回答高中报考问题。
5. 两个孩子能否协调接送片区？若目标学校该年级无空位，有什么正式安排？
烦请提供适用政策原文、办事入口、负责科室及可留存的答复。</div></div>
<div class="copy-card"><div class="copy-head"><h3>发给园区 / 创业服务部门</h3><button class="btn no-print" data-copy="qBusiness">复制话术</button></div><div class="copy-text" id="qBusiness">我们做[出海App/订阅SaaS/内容业务]，是否属于AI产品：[ ]。现有公司注册于[ ]，成立时间[ ]，人员[ ]，主营收入方式[ ]。计划[新设杭州主体/迁入现有主体/先不迁公司]。
请按真实情况确认：
1. 能匹配哪些具体政策？请提供文件编号和当前申报通知，不只提供宣传海报。
2. 受益对象是创业者、经营公司、采购企业，还是园区运营方？
3. 对身份、毕业时间、持股、社保、注册地址、实际经营、纳税和入驻期限有哪些限制？
4. 房租支持是工位、办公室还是指定人才住房？封顶多少？先付后补还是直接减免？兑现时点及同类补贴能否叠加？
5. 普通出海软件项目能使用哪些服务？若是AI+OPC，当前入库条件、社区名单及供应商名单是什么？
6. 给出总费用、合同、退租和迁出条款。若未获补助，合同下我方仍须承担哪些费用？</div></div>
<div class="copy-card"><div class="copy-head"><h3>发给房东 / 租赁服务方</h3><button class="btn no-print" data-copy="qRent">复制话术</button></div><div class="copy-text" id="qRent">我们是带小学和初中孩子的家庭，拟长期真实居住，不需要“包学位”承诺。
请提供准确门牌和房屋用途，并说明能否依法配合租赁备案、居住登记及教育部门要求的租赁证明材料。
请列明押金、付款周期、物业及其他费用、提前解约和续租规则。
孩子能否入学由主管部门审核；若接收延迟或未成功，双方可否在合同中事先协商明确的退出处理？我们需要先审阅完整合同，再决定签约。</div></div></section>

<section id="sources"><div class="section-head"><span class="section-no">12</span><h2>原文库与核验边界</h2></div>
<div class="notice neutral"><p><strong>收录口径：</strong>围绕这家人的迁居决策整理核心相关政策、解读和办事入口，不冒称覆盖全杭州所有政策。</p><p>已阅读的政策或解读与仅确认入口的平台分开标注。两份市级招生文件本次取得的是杭州网全文转引，已明确标记；未取得任何一家人的官方资格审核结果。</p></div>
<div class="panel"><h3>这几处仍要补上，不能靠推测填平</h3><ul class="gap-list"><li><strong>余杭：</strong>目标学期转学、新生招生及未来高中报考的本区最新细则和空位。本次检索/页面访问未可靠取得可用正文。</li><li><strong>西湖：</strong>目标片区、目标年级的区级转学细则与空位；已读的行知小学方案仅是特定学校一年级实例。</li><li><strong>落户：</strong>夫妻各自适用的当前办事指南、社保和落点条件；不把2023年基础文件当作2026年所有路径都未变化。</li><li><strong>企业：</strong>AI+OPC完整入库细则、当期社区名单和生态伙伴清单；普通出海App/SaaS可申请项目的细化口径；现有西安主体迁入是否影响企业年限或原有义务。</li><li><strong>服务与成本：</strong>具体学校岗位、租房挂牌和成交、实时通勤、园区剩余工位、电话实际接听和补贴到账情况均未实地或登录核验。</li></ul><p class="subtle">本手册保存的是阅读批注、官方链接及核验记录，不是所有原始PDF、附件或网页的完整离线镜像。完整原文以链接中的发布部门版本为准。</p></div>
<h3 style="margin-top:26px">24条来源与入口</h3><div class="source-list">{''.join(rows)}</div>
</section>
<footer class="footer"><div>家庭迁居与出海创业政策手册 · 核验截至2026-09-28<br>单文件HTML；无外部脚本、无分析统计、无账号登录。勾选与备注仅尝试存于本机浏览器。</div><div>法律/招生及申报事项以主管部门审核为准。<br>本页不构成录取、落户或补助承诺。</div></footer>
'''

JS=r'''
(()=>{'use strict';
const $=(s)=>document.querySelector(s), $$=(s)=>Array.from(document.querySelectorAll(s));
function toast(msg){const t=$('#toast');t.textContent=msg;t.style.display='block';setTimeout(()=>t.style.display='none',3000)}
const store={get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}},remove(k){try{localStorage.removeItem(k)}catch{}}};
const cards=$$('.policy');function filter(){const q=$('#policySearch').value.trim().toLowerCase(),cat=$('#categoryFilter').value;let n=0;cards.forEach(c=>{const show=(!q||c.textContent.toLowerCase().includes(q))&&(cat==='全部'||c.dataset.category===cat);c.style.display=show?'':'none';if(show)n++});$('#filterCount').textContent=`${n} / ${cards.length} 条`;$('#empty').style.display=n?'none':'block'}
$('#policySearch').addEventListener('input',filter);$('#categoryFilter').addEventListener('change',filter);
let allOpen=false;$('#expandBtn').addEventListener('click',()=>{allOpen=!allOpen;$$('.policy details').forEach(x=>x.open=allOpen);$('#expandBtn').textContent=allOpen?'收起办理提示':'展开办理提示'});
let beforePrintStates=[];window.addEventListener('beforeprint',()=>{beforePrintStates=$$('.policy details').map(x=>x.open);$$('.policy details').forEach(x=>x.open=true)});window.addEventListener('afterprint',()=>{$$('.policy details').forEach((x,i)=>x.open=beforePrintStates[i]||false)});$('#printBtn').addEventListener('click',()=>window.print());
const key='hz-family-policy-20260928-checks';let saved={};try{saved=JSON.parse(store.get(key)||'{}')}catch{};
const checks=$$('[data-check]');function updateChecks(){let n=0;const data={};checks.forEach(c=>{data[c.dataset.check]=c.checked;c.closest('label').classList.toggle('checked',c.checked);if(c.checked)n++});$('#checkProgress').textContent=`已确认 ${n} / ${checks.length} 项`;store.set(key,JSON.stringify(data))}
checks.forEach(c=>{c.checked=!!saved[c.dataset.check];c.addEventListener('change',updateChecks)});updateChecks();
$('#familyNotes').value=store.get(key+'-notes')||'';$('#familyNotes').addEventListener('input',e=>store.set(key+'-notes',e.target.value));
$('#resetChecks').addEventListener('click',()=>{if(!confirm('清空当前勾选？家庭备注不会删除。'))return;checks.forEach(c=>c.checked=false);updateChecks();toast('勾选已清空')});
function download(text,filename,type='text/plain;charset=utf-8'){const u=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=u;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)}
$('#exportChecks').addEventListener('click',()=>{const text=['杭州家庭迁居｜办理确认记录','政策核验截至：2026-09-28','记录导出时间：'+new Date().toLocaleString('zh-CN'),'勾选不是资格审批。','',...checks.map(c=>(c.checked?'[已确认] ':'[未确认] ')+c.parentElement.textContent.trim()),'','家庭备注：',$('#familyNotes').value].join('\n');download(text,'杭州迁居-确认记录.txt');toast('已导出文本记录')});
$$('[data-copy]').forEach(btn=>btn.addEventListener('click',async()=>{const text=document.getElementById(btn.dataset.copy).textContent.trim();try{await navigator.clipboard.writeText(text);toast('已复制，请用真实情况替换方括号')}catch{const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.left='-10000px';document.body.append(ta);ta.select();const ok=document.execCommand('copy');ta.remove();toast(ok?'已复制':'自动复制受浏览器限制，请选择文字复制')}}));
const bid=['bRent','bSchool','bLiving','bOffice','bOther','bMove','bDeposit','bMonths'];function num(id){const v=Number(document.getElementById(id).value);return Number.isFinite(v)?Math.max(0,v):0}function budget(){const filled=bid.slice(0,7).some(id=>document.getElementById(id).value!==''),m=Math.min(36,Math.max(1,Math.floor(num('bMonths')||6))),monthly=bid.slice(0,5).reduce((s,id)=>s+num(id),0),cash=monthly*m+num('bMove')+num('bDeposit'),money=n=>'¥ '+n.toLocaleString('zh-CN',{maximumFractionDigits:2});$('#monthlyTotal').textContent=filled?money(monthly):'待填写';$('#cashTotal').textContent=filled?money(cash):'待填写';$('#cashLabel').textContent=`${m}个月无新增收入情景所需现金`}
bid.forEach(id=>document.getElementById(id).addEventListener('input',budget));budget();
if('IntersectionObserver' in window){const obs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){$$('.sidebar nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+e.target.id))}})},{rootMargin:'-10% 0px -75% 0px'});$$('main section').forEach(s=>obs.observe(s))}
})();
'''

html_text=HEADER+BODY+'<div class="toast" id="toast" role="status" aria-live="polite"></div></main></div><script>'+JS+'</script></body></html>'
OUT.joinpath('hangzhou_family_policy_guide.html').write_text(html_text,encoding='utf-8')
# A readable companion package, without implying these are original government files.
md=['# 杭州家庭迁居：政策阅读批注','',f'核验截至：{AS_OF}','本文件是自写批注，不是政策原文或完整附件副本。原文请通过各条链接打开。','']
for p in POLICIES:
    clean=lambda t:re.sub('<[^>]+>','',t)
    md += [f"## {p['id']} {p['title']}",f"- 范围：{p['scope']}",f"- 时点：{p['date']}",f"- 状态：{p['status']}",f"- 原文关键词：{p['quote']}",'',f"条款要点：{clean(p['reading'])}",'',f"对这家人的含义：{clean(p['meaning'])}",'',f"办理前核验：{clean(p['action'])}",'']
    for i in p['sources']:
        md += [f"- {i} {SMAP[i]['title']}：{SMAP[i]['url']}"]
    md.append('')
OUT.joinpath('政策阅读批注.md').write_text('\n'.join(md),encoding='utf-8')
README='''# 杭州家庭迁居与出海创业政策手册

核验截至：2026年9月28日。
适用背景：目前在西安生活，父亲从事出海App、SaaS与自媒体，母亲有民办学校任教经历，孩子涉及小学与初中，拟全家租房迁居杭州。

## 打开方式
用 Chrome、Edge、Safari 或其他现代浏览器打开 `hangzhou_family_policy_guide.html`。不需要安装依赖或启动服务器。正文可离线阅读，原文链接与政务平台需要联网。

## 包内文件
- hangzhou_family_policy_guide.html：完整报告，包括居住方案、升学路径、14张政策解读卡、平台、确认清单、咨询话术及24条来源/入口。
- 政策阅读批注.md：便于复制、检索的逐条批注。
- sources.json：来源名称、机构、日期、链接、范围和核验状态。
- policy_annotations.json：政策卡结构化数据。
- build_report.py：生成此HTML的源代码；仅使用Python标准库。

## 功能
政策关键字搜索及分类、展开办理提示、本机勾选和备注、导出确认记录、复制咨询话术、零补贴成本试算、浏览器打印。

## 重要边界
这不是全杭州全量政策库；也不是所有原始PDF或附件的离线镜像。内容为阅读批注，原文以发布部门版本为准。
2026年新生招生和滨江暑假转学日期不应推定为2027年日程。
市区高中招生文件具有特定范围，不能直接套到余杭。
两份市级招生文件本次阅读来源为杭州网全文转引，已标注；仍应向主管部门核验个案。
家庭成员实际年级、户籍、资格、预算尚不齐全，不能据本文获得确定入学、落户或补贴承诺。
未实地考察、未实拨电话、未登录个人或企业政务账号办理；部分待核项已在报告列出。

## 本机数据
页面不含外部脚本和统计服务。清单和备注仅尝试写入当前浏览器的localStorage；部分本地文件模式可能不保存，请导出文本备份。为保护隐私，不建议填写完整证件号码。
'''
OUT.joinpath('README.md').write_text(README,encoding='utf-8')
print(json.dumps({'html_bytes':len(html_text.encode()),'policy_cards':len(POLICIES),'sources':len(SOURCES),'html_path':str(OUT/'hangzhou_family_policy_guide.html')},ensure_ascii=False))

# GitHub Pages presentation additions; the policy body remains the restored text.
page = html_text.replace('<title>', '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2212%22 fill=%22%23102e38%22/%3E%3Ctext x=%2211%22 y=%2244%22 font-size=%2232%22 fill=%22%23ffe19b%22%3EHZ%3C/text%3E%3C/svg%3E"><title>', 1)
page = page.replace('<button class="btn no-print" id="printBtn">打印 / 存为 PDF</button>', '<div class="no-print" style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn" href="downloads/hangzhou-family-policy-pack.zip" download>下载资料包</a><button class="btn" id="printBtn">打印 / 存为 PDF</button></div>', 1)
(OUT.parent / 'index.html').write_text(page, encoding='utf-8')
