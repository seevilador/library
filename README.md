# <span style="color: #2c3e50; font-size: 2em;">图书管理系统</span>

这是一个基于 Flask 框架开发的简单图书管理系统。系统提供了图书的增删改查功能，并支持图书封面图片的上传和管理。

## <span style="color: #3498db;">主要功能</span>

- 图书信息管理（增删改查）
- 图书封面图片上传和管理
- 简洁美观的用户界面
- 基于 SQLite 数据库的数据存储

## <span style="color: #3498db;">系统要求</span>

- Windows 10 或更高版本
- Python 3.x（用于运行源代码版本）
- 运行可执行文件版本无需额外要求

## <span style="color: #3498db;">快速开始指南</span>

### <span style="color: #e74c3c;">选项一：运行可执行文件（推荐普通用户使用）</span>

1. 下载最新发布包
2. 解压到目标位置
3. 运行 `图书管理系统.exe`
4. 打开浏览器访问 `http://localhost:5000`

### <span style="color: #e74c3c;">选项二：运行源代码（适合开发者）</span>

1. 确保系统已安装 Python 3.x
2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行应用程序：
   ```bash
   python app.py
   ```
4. 打开浏览器访问 `http://localhost:5000`

## <span style="color: #3498db;">核心功能</span>

### <span style="color: #2ecc71;">图书管理</span>
- 查看系统中的所有图书
- 添加新图书及详细信息
- 编辑现有图书信息
- 从系统中删除图书

### <span style="color: #2ecc71;">图片管理</span>
- 上传图书封面图片
- 查看图书封面
- 自动图片大小调整和优化

### <span style="color: #2ecc71;">用户界面</span>
- 响应式设计
- 直观的导航
- 实时搜索功能
- 分页支持

## <span style="color: #3498db;">文件结构</span>

- `app.py`: 主应用程序文件
- `database.py`: 数据库模型和配置
- `templates/`: HTML 模板文件
- `static/`: 静态资源（CSS、JavaScript 等）
- `uploads/`: 存储上传的图书封面目录
- `books.db`: SQLite 数据库文件

## <span style="color: #3498db;">重要说明</span>

1. <span style="color: #e67e22;">可执行文件版本：</span>
   - 应用程序会自动创建必要的文件和目录
   - 确保安装目录具有写入权限
   - 如遇权限问题，请以管理员身份运行

2. <span style="color: #e67e22;">源代码版本：</span>
   - 建议使用虚拟环境
   - 首次运行时会自动创建数据库
   - 确保 `uploads` 目录具有写入权限

## <span style="color: #3498db;">故障排除</span>

1. <span style="color: #e67e22;">如果应用程序无法启动：</span>
   - 检查 5000 端口是否可用
   - 确保所有必需文件都存在
   - 尝试以管理员身份运行

2. <span style="color: #e67e22;">如果数据库操作失败：</span>
   - 检查文件权限
   - 确保应用程序对目录具有写入权限

3. <span style="color: #e67e22;">如果图片上传失败：</span>
   - 确认 `uploads` 目录存在
   - 检查磁盘空间是否充足
   - 确保具有适当的文件权限

## <span style="color: #3498db;">技术支持</span>

如有任何问题或疑问，请联系开发团队或在代码仓库中创建问题。 