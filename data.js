// 赶集会 前九期数据 — 从会议纪要原文逐条提取，跳跳审核
const siteData = {
  "stats": {
    "totalSessions": 9,
    "totalPeople": 41,
    "totalMotions": 31,
    "passedMotions": 27,
    "pendingMotions": 4,
    "totalAttendance": 147
  },
  "sessions": [
    {
      "label": "第1期",
      "date": "2026-03-22",
      "presentCount": 19,
      "totalMembers": 45,
      "topics": ["赶集会制度建立", "将进酒推广销售", "DAO治理结构", "集体生活约定"],
      "motions": [
        {"proposer": "青峰明月", "content": "成立将进酒推广销售小组，制定销售草案", "result": "被终止（不合规）", "type": "活动"},
        {"proposer": "智能主持人", "content": "3月30日前请高玲姐准备南塘将进酒生产资料、生产过程记录及制作工法", "result": "通过（5票）", "type": "活动"},
        {"proposer": "富章", "content": "3月30号前提供两小时，燕冷号召共创营，确认方案可行性", "result": "通过（4票）", "type": "活动"},
        {"proposer": "富章", "content": "25、26号前安排与淑慧、验人的响应安排，与袁老师直接对话", "result": "通过（3票）", "type": "活动"},
        {"proposer": "富章", "content": "25或26号晚安排1-1.5小时线上会议，召集家乐及在地伙伴，讨论云彪老师的创业项目", "result": "通过（3票）", "type": "活动"},
        {"proposer": "富章", "content": "创业学社研究AI如何支持创业项目，提出可行方案后在公众会议讨论", "result": "获默认一致同意", "type": "制度"},
        {"proposer": "砚仁", "content": "明天上午召开调研小组会议，感兴趣的成员可私下加入，3月30日宣告调研活动开始", "result": "通过（4票）", "type": "活动"},
        {"proposer": "跳跳", "content": "30号举行聚会，收集大家意见，制定不超过100字的集体吃饭约定规则", "result": "通过（6票）", "type": "制度"}
      ]
    },
    {
      "label": "第2期",
      "date": "2026-03-30",
      "presentCount": 13,
      "totalMembers": 45,
      "topics": ["加密钱包到账确认", "宣传文案招募", "共创营筹备"],
      "motions": [
        {"proposer": "富章", "content": "4月10号推出宣传文案招募机制，达到宣传活动目标；张玲负责将进酒文案预热", "result": "通过（3票）", "type": "活动"},
        {"proposer": "富章", "content": "了解第二期活动收尾，统计差额数据，燕南通报信息不对称问题", "result": "未获附议", "type": "活动"},
        {"proposer": "富章", "content": "确认合作社加密钱包到账情况，自行参酌是否对抗法律风险", "result": "通过（4票）", "type": "制度"},
        {"proposer": "富章", "content": "林彪老师进行口述史，讲述庙的历史，共创营根据需要发起", "result": "获默认一致同意", "type": "活动"},
        {"proposer": "跳跳", "content": "下次赶集会前，收集集体生活反馈，制定一起吃饭的约定文本", "result": "获默认一致同意", "type": "制度"},
        {"proposer": "富章", "content": "4月10号前若曦负责测算收入支出并制作简要测算表，跳跳等协助", "result": "通过（3票）", "type": "活动"}
      ]
    },
    {
      "label": "第3期",
      "date": "2026-04-10",
      "presentCount": 16,
      "totalMembers": 45,
      "topics": ["静心营活动", "赶集会参与机制", "共创会议"],
      "motions": [
        {"proposer": "富章", "content": "若曦发起静心营，地点南塘，8-12人，8-15天，预计4月20日或5月初开始", "result": "通过（4票）", "type": "活动"},
        {"proposer": "富章", "content": "15号前组织'好好吃饭好好生活'共创会议，邀请老师及社区成员分享经验", "result": "通过（2票）", "type": "活动"},
        {"proposer": "富章", "content": "与野生蓝莓沟通，了解需求和期待，根据结果决定是否再次发起动议", "result": "未获附议", "type": "活动"},
        {"proposer": "富章", "content": "蓝莓下周二前与张帆对话，了解情况并探索合作可能，采取最小激活策略", "result": "获默认一致同意", "type": "活动"}
      ]
    },
    {
      "label": "第4期",
      "date": "2026-04-20",
      "presentCount": 12,
      "totalMembers": 45,
      "topics": ["英语共学策划", "会议时间调整"],
      "motions": [
        {"proposer": "YTZ", "content": "发起英语共学共同策划，征集参与者意愿和想法，建立沟通群组", "result": "获默认一致同意", "type": "活动"},
        {"proposer": "KIKO", "content": "将赶集会时间调整为每月10号、20号、30号晚上10点（如过晚可提前至9点）", "result": "获默认一致同意", "type": "制度"}
      ]
    },
    {
      "label": "第5期",
      "date": "2026-04-30",
      "presentCount": 18,
      "totalMembers": 45,
      "topics": ["周末营地活动", "夏令营策划"],
      "motions": [
        {"proposer": "富章", "content": "在宿舍区域开展周末活动，6月端午假期组织3天活动，7月后开办为期1周收费夏令营，与钱老师合作课程策划和招生", "result": "获默认一致同意", "type": "活动"}
      ]
    },
    {
      "label": "第6期",
      "date": "2026-05-10",
      "presentCount": 11,
      "totalMembers": 45,
      "topics": ["iMeeting功能讨论", "数据知识库集成", "社区操作系统", "AI BOT统一入口", "会议管理与AI功能"],
      "motions": []
    },
    {
      "label": "第7期",
      "date": "2026-05-20",
      "presentCount": 18,
      "totalMembers": 45,
      "topics": ["场地利用与盈利策略", "直播行动", "辩论赛筹备", "代币经济与IVT工具", "电子合同与智能合约"],
      "motions": [
        {"proposer": "富章", "content": "在南塘合作社宿舍场地基础上提供食宿服务，进行市场竞争和招商，收取场地租赁、住宿和餐饮费用", "result": "通过", "type": "活动"},
        {"proposer": "砚仁", "content": "成立直播行动小组：刘宇摄像、家乐场控、明浩摄像、机器主持，采访前两期参与者", "result": "通过", "type": "活动"},
        {"proposer": "富章", "content": "修正案：富章离开前支持一场论坛，确保时间杠杆比率不要太小", "result": "获默认一致同意", "type": "修正案"},
        {"proposer": "奇迹行者", "content": "发起辩论赛筹备：在赶集会募集筹备组，设定南塘道治理或未来愿景议题，创新辩论形式结合iMeeting规则", "result": "通过", "type": "活动"},
        {"proposer": "富章", "content": "开发IVT工具，今年上半年完成钱包支付接通；推动代币经济、有价加密货币，形成电子合同发展到智能合约", "result": "通过", "type": "制度"},
        {"proposer": "富章", "content": "修正案：安排1-3场对话/研讨（分散10天内），推进iMeeting功能与代币经济结合", "result": "获默认一致同意", "type": "修正案"}
      ]
    },
    {
      "label": "第8期",
      "date": "2026-05-30",
      "presentCount": 22,
      "totalMembers": 45,
      "topics": ["合作社成员孤独感", "观察营招募与宣传", "自媒体发展策略", "南塘道住宿与NT流通", "提案发起与利益协调", "合作社角色与演变"],
      "motions": []
    },
    {
      "label": "第9期",
      "date": "2026-06-10",
      "presentCount": 18,
      "totalMembers": 43,
      "topics": ["南塘艺术共创营", "NT价值与劳动认证", "收入与盈利路径", "搭便车问题", "组织目标澄清"],
      "motions": [
        {"proposer": "KIKO", "content": "下次赶集会前确定可邀请人员名单，控制会议正式程度，围绕议题讨论并设提问环节", "result": "获默认一致同意", "type": "制度"},
        {"proposer": "奇迹行者", "content": "设立一期'葡萄酒会'：端午节后周六启动，工作人员培训（开瓶/倒酒/礼仪），先确认人数与预算再确定酒品，场地安排与执行方案", "result": "通过（3票）", "type": "活动"},
        {"proposer": "奇迹行者", "content": "（第二项主动议，内容缺失）", "result": "尚未解决", "type": "主动议"},
        {"proposer": "富章", "content": "修正案：删除议程第二项'葡萄酒从青岛运回后加征12%-15%费用'的讨论", "result": "获默认一致同意", "type": "修正案"}
      ]
    }
  ],
  "people": [
    {"name": "富章", "attendedCount": 9, "speechCount": 0},
    {"name": "xiaobai", "attendedCount": 9, "speechCount": 0},
    {"name": "砚仁", "attendedCount": 9, "speechCount": 0},
    {"name": "KIKO", "attendedCount": 9, "speechCount": 0},
    {"name": "跳跳", "attendedCount": 9, "speechCount": 0},
    {"name": "奇迹行者", "attendedCount": 8, "speechCount": 0},
    {"name": "木木曦", "attendedCount": 8, "speechCount": 0},
    {"name": "YTZ", "attendedCount": 8, "speechCount": 0},
    {"name": "若曦", "attendedCount": 8, "speechCount": 0},
    {"name": "蚊子", "attendedCount": 7, "speechCount": 0},
    {"name": "淅淅", "attendedCount": 7, "speechCount": 0},
    {"name": "周周", "attendedCount": 6, "speechCount": 0},
    {"name": "南塘汉子", "attendedCount": 5, "speechCount": 0},
    {"name": "和光同尘", "attendedCount": 5, "speechCount": 0},
    {"name": "青峰明月", "attendedCount": 5, "speechCount": 0},
    {"name": "谠泰", "attendedCount": 5, "speechCount": 0},
    {"name": "野生蓝莓", "attendedCount": 5, "speechCount": 0},
    {"name": "洪水", "attendedCount": 4, "speechCount": 0},
    {"name": "Daniel（出席者）", "attendedCount": 4, "speechCount": 0},
    {"name": "大卷", "attendedCount": 4, "speechCount": 0},
    {"name": "Hello 章先森", "attendedCount": 3, "speechCount": 0},
    {"name": "漫山漫野", "attendedCount": 3, "speechCount": 0},
    {"name": "家乐", "attendedCount": 3, "speechCount": 0},
    {"name": "Janus", "attendedCount": 3, "speechCount": 0},
    {"name": "菱形", "attendedCount": 3, "speechCount": 0},
    {"name": "焕炘", "attendedCount": 2, "speechCount": 0},
    {"name": "南塘之子", "attendedCount": 2, "speechCount": 0},
    {"name": "阿山", "attendedCount": 2, "speechCount": 0},
    {"name": "大杜", "attendedCount": 2, "speechCount": 0},
    {"name": "世佳", "attendedCount": 1, "speechCount": 0},
    {"name": "麦田", "attendedCount": 1, "speechCount": 0},
    {"name": "云展", "attendedCount": 1, "speechCount": 0},
    {"name": "方熊", "attendedCount": 1, "speechCount": 0},
    {"name": "余星", "attendedCount": 1, "speechCount": 0},
    {"name": "Connie", "attendedCount": 1, "speechCount": 0},
    {"name": "紫螟", "attendedCount": 1, "speechCount": 0},
    {"name": "麦客", "attendedCount": 1, "speechCount": 0},
    {"name": "Gloria", "attendedCount": 1, "speechCount": 0},
    {"name": "茵籽", "attendedCount": 1, "speechCount": 0},
    {"name": "言礼", "attendedCount": 1, "speechCount": 0},
    {"name": "aa", "attendedCount": 1, "speechCount": 0}
  ],
  "motions": []
};

// Auto-compute stats
(function() {
  const d = siteData;
  d.stats.totalSessions = d.sessions.length;
  d.stats.totalPeople = d.people.length;
  let totalMotions = 0, passed = 0;
  d.sessions.forEach(s => {
    s.motions.forEach(m => { totalMotions++; if (m.result.includes('通过') || m.result.includes('一致同意')) passed++; });
  });
  d.stats.totalMotions = totalMotions;
  d.stats.passedMotions = passed;
  d.stats.pendingMotions = totalMotions - passed;
  d.stats.totalAttendance = d.sessions.reduce((sum, s) => sum + s.presentCount, 0);
})();
