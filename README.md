# 🎓 学生成绩管理系统

一个基于 Flask 的学生成绩管理系统，提供简单直观的学生成绩管理功能。

## ✨ 主要功能

### 👥 用户管理
- 管理员和教师两种角色
- 基于角色的权限控制

### 📚 班级管理
- 班级信息的增删改查
- 班级学生数量统计

### 👨‍🎓 学生管理
- 学生信息的增删改查
- 按班级筛选学生列表

### 📊 成绩管理
- 成绩录入与统计
- 多维度成绩分析
- 平均分计算

## 🛠️ 技术栈

- 💻 Flask + MySQL
- 🎨 Bootstrap 5
- 🔧 SQLAlchemy

## 📦 快速开始

1. 配置环境
```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

2. 配置数据库
```ini
# 创建 .env 文件
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3307
MYSQL_DATABASE=student_management
SECRET_KEY=your-secret-key
```

3. 初始化数据库
```bash
python scripts/init_db.py
```

4. 运行应用
```bash
python run.py
```

## 👤 默认账户

- 管理员：admin / admin123
- 教师：teacher / teacher123

## 📁 项目结构

```
student_management/
├── app/
│   ├── models/     # 数据模型
│   ├── routes/     # 路由处理
│   ├── templates/  # 页面模板
│   └── utils/      # 工具函数
├── .env           # 环境配置
└── config.py      # 应用配置
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request

## 📝 联系方式

如果您有任何问题或建议，欢迎通过以下方式联系：

- 微信号：`ddouu3`（请注明来意）

## ☕ 支持项目

如果这个项目对您有帮助，欢迎打赏一杯咖啡：

<p align="center">
  <img src="docs/images/alipay.jpg" alt="支付宝" width="200" height="200" style="margin-right: 20px;"/>
  <img src="docs/images/wechat_pay.jpg" alt="微信支付" width="200" height="200"/>
</p>
<p align="center">
  <span style="margin-right: 120px;">支付宝</span>
  <span>微信支付</span>
</p>

## 📝 许可证

MIT License