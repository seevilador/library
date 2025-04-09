from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    """
    图书模型类，定义了图书的所有属性和关系
    
    属性:
        id (int): 主键，图书的唯一标识符
        title (str): 图书标题，必填项
        author (str): 作者姓名，必填项
        isbn (str): 国际标准书号，唯一
        publish_date (date): 出版日期
        category (str): 图书分类
        description (text): 图书描述
        file_path (str): 电子书文件路径
        cover_path (str): 封面图片路径
        is_borrowed (bool): 是否被借出
        borrower (str): 借阅者姓名
        borrow_date (datetime): 借阅日期
        return_date (datetime): 归还日期
        created_at (datetime): 创建时间
        updated_at (datetime): 最后更新时间
    """
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 基本信息
    title = db.Column(db.String(100), nullable=False)  # 图书标题，必填
    author = db.Column(db.String(100), nullable=False)  # 作者，必填
    isbn = db.Column(db.String(13), unique=True)  # ISBN号，唯一
    publish_date = db.Column(db.Date)  # 出版日期
    category = db.Column(db.String(50))  # 分类
    description = db.Column(db.Text)  # 描述
    
    # 文件路径
    file_path = db.Column(db.String(255))  # 电子书文件路径
    cover_path = db.Column(db.String(255))  # 封面图片路径
    
    # 借阅信息
    is_borrowed = db.Column(db.Boolean, default=False)  # 是否被借出
    borrower = db.Column(db.String(100))  # 借阅者
    borrow_date = db.Column(db.DateTime)  # 借阅日期
    return_date = db.Column(db.DateTime)  # 归还日期
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    def __repr__(self):
        """
        返回图书对象的字符串表示
        
        返回:
            str: 图书标题的字符串表示
        """
        return f'<Book {self.title}>' 