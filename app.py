from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from database import db, Book
from datetime import datetime, timedelta
import os
import logging
from werkzeug.utils import secure_filename
import shutil
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, make_response
# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COVER_FOLDER'] = 'static/covers'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COVER_FOLDER'], exist_ok=True)

# 创建默认封面图片
default_cover_path = os.path.join(app.config['COVER_FOLDER'], 'default.jpg')
if not os.path.exists(default_cover_path):
    # 创建一个简单的默认封面图片
    img = Image.new('RGB', (300, 400), color=(240, 240, 240))
    d = ImageDraw.Draw(img)
    d.text((150, 200), "无封面", fill=(100, 100, 100), anchor="mm")
    img.save(default_cover_path)
    logger.info("已创建默认封面图片")

db.init_app(app)

# 确保数据库表存在
def init_db():
    """
    初始化数据库，创建所有必要的表
    
    如果创建过程中出现错误，会记录错误并抛出异常
    """
    with app.app_context():
        try:
            logger.info("正在创建数据库表...")
            db.create_all()
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"创建数据库表时出错: {str(e)}")
            raise

@app.route('/')
def index():
    """
    首页路由
    
    返回:
        template: 渲染后的首页模板，包含所有图书列表
    """
    try:
        logger.debug("正在获取所有图书...")
        query = request.args.get('query', '')
        search_type = request.args.get('search_type', 'title')
        
        if query:
            if search_type == 'title':
                books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
            elif search_type == 'author':
                books = Book.query.filter(Book.author.ilike(f'%{query}%')).all()
            elif search_type == 'isbn':
                books = Book.query.filter(Book.isbn.ilike(f'%{query}%')).all()
            elif search_type == 'category':
                books = Book.query.filter(Book.category.ilike(f'%{query}%')).all()
        else:
            books = Book.query.all()
        
        logger.debug(f"成功获取到 {len(books)} 本图书")
        return render_template('index.html', books=books, query=query, search_type=search_type)
    except Exception as e:
        logger.error(f"获取图书列表时出错: {str(e)}")
        flash('获取图书列表时出错，请查看日志')
        return render_template('index.html', books=[])

@app.route('/add', methods=['POST'])
def add_book():
    """
    添加新图书的路由
    
    处理POST请求，接收表单数据，保存图书信息和文件
    
    返回:
        redirect: 成功添加后重定向到首页
    """
    try:
        logger.debug("开始处理添加图书请求...")
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        publish_date_str = request.form.get('publish_date')
        category = request.form.get('category')
        description = request.form.get('description')
        
        logger.debug(f"表单数据: title={title}, author={author}, isbn={isbn}")
        
        # 处理图书文件
        file_path = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                logger.debug(f"保存图书文件到: {file_path}")
                file.save(file_path)
        
        # 处理封面图片
        cover_path = None
        if 'cover' in request.files:
            cover = request.files['cover']
            if cover.filename != '' and allowed_image(cover.filename):
                cover_filename = secure_filename(cover.filename)
                # 确保文件名是唯一的
                base, ext = os.path.splitext(cover_filename)
                counter = 1
                while os.path.exists(os.path.join(app.config['COVER_FOLDER'], cover_filename)):
                    cover_filename = f"{base}_{counter}{ext}"
                    counter += 1
                
                # 使用正斜杠而不是反斜杠
                cover_path = f"covers/{cover_filename}"
                full_cover_path = os.path.join(app.config['COVER_FOLDER'], cover_filename)
                logger.debug(f"保存封面图片到: {full_cover_path}")
                cover.save(full_cover_path)
        
        if title and author:
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                publish_date=datetime.strptime(publish_date_str, '%Y-%m-%d').date() if publish_date_str else None,
                category=category,
                description=description,
                file_path=file_path,
                cover_path=cover_path
            )
            db.session.add(book)
            db.session.commit()
            logger.info(f"成功添加图书: {title}")
            flash('图书添加成功！')
        else:
            logger.warning("添加图书失败：标题和作者是必填项")
            flash('标题和作者是必填项！')
    except Exception as e:
        logger.error(f"添加图书时出错: {str(e)}")
        flash('添加图书时出错，请查看日志')
    
    return redirect(url_for('index'))

@app.route('/edit_book/<int:id>', methods=['POST'])
def edit_book(id):
    """
    编辑图书信息的路由
    
    参数:
        id (int): 要编辑的图书ID
    
    返回:
        redirect: 成功编辑后重定向到首页
    """
    try:
        book = Book.query.get_or_404(id)
        
        # 更新基本信息
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.category = request.form.get('category')
        book.description = request.form.get('description')
        
        # 处理出版日期
        publish_date = request.form.get('publish_date')
        if publish_date:
            book.publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        
        # 处理借出状态
        book.is_borrowed = 'is_borrowed' in request.form
        
        # 处理封面图片
        if 'cover' in request.files:
            cover = request.files['cover']
            if cover and cover.filename:
                filename = secure_filename(cover.filename)
                # 确保文件名是唯一的
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(app.config['COVER_FOLDER'], filename)):
                    filename = f"{base}_{counter}{ext}"
                    counter += 1
                
                cover_path = os.path.join(app.config['COVER_FOLDER'], filename)
                cover.save(cover_path)
                # 使用正斜杠而不是反斜杠
                book.cover_path = f"covers/{filename}"
        
        # 处理图书文件
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                book.file_path = os.path.join('uploads', filename)
        
        db.session.commit()
        flash('图书信息已更新', 'success')
    except Exception as e:
        logger.error(f"编辑图书时出错: {str(e)}")
        flash('更新失败，请重试！', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_book/<int:id>')
def delete_book(id):
    """
    删除图书的路由
    
    参数:
        id (int): 要删除的图书ID
    
    返回:
        redirect: 删除后重定向到首页
    """
    try:
        logger.debug(f"正在删除图书 ID: {id}")
        book = Book.query.get_or_404(id)
        
        # 检查图书是否已借出
        if book.is_borrowed:
            logger.warning(f"尝试删除已借出的图书: {book.title}")
            flash('该图书已被借出，无法删除！请先归还图书。')
            return redirect(url_for('index'))
        
        # 删除相关文件
        if book.file_path and os.path.exists(book.file_path):
            os.remove(book.file_path)
            logger.debug(f"已删除图书文件: {book.file_path}")
        
        if book.cover_path:
            cover_path = os.path.join(app.config['COVER_FOLDER'], os.path.basename(book.cover_path))
            if os.path.exists(cover_path):
                os.remove(cover_path)
                logger.debug(f"已删除封面图片: {cover_path}")
        
        db.session.delete(book)
        db.session.commit()
        logger.info(f"成功删除图书: {book.title}")
        flash(f'成功删除图书: {book.title}')
    except Exception as e:
        logger.error(f"删除图书时出错: {str(e)}")
        flash('删除图书时出错，请查看日志')
    
    return redirect(url_for('index'))

@app.route('/borrow_book/<int:id>')
def borrow_book(id):
    """
    借阅图书的路由
    
    参数:
        id (int): 要借阅的图书ID
    
    返回:
        redirect: 借阅后重定向到首页
    """
    try:
        logger.debug(f"正在借阅图书 ID: {id}")
        book = Book.query.get_or_404(id)
        
        if book.is_borrowed:
            logger.warning(f"尝试借阅已借出的图书: {book.title}")
            flash('该图书已被借出！')
            return redirect(url_for('index'))
        
        # 设置借阅状态
        book.is_borrowed = True
        book.borrower = request.args.get('borrower', '未知')
        book.borrow_date = datetime.now()
        book.return_date = None
        
        db.session.commit()
        logger.info(f"成功借阅图书: {book.title}")
        flash(f'成功借阅图书: {book.title}')
    except Exception as e:
        logger.error(f"借阅图书时出错: {str(e)}")
        flash('借阅图书时出错，请查看日志')
    
    return redirect(url_for('index'))

@app.route('/return_book/<int:id>')
def return_book(id):
    """
    归还图书的路由
    
    参数:
        id (int): 要归还的图书ID
    
    返回:
        redirect: 归还后重定向到首页
    """
    try:
        logger.debug(f"正在归还图书 ID: {id}")
        book = Book.query.get_or_404(id)
        
        if not book.is_borrowed:
            logger.warning(f"尝试归还未借出的图书: {book.title}")
            flash('该图书未被借出！')
            return redirect(url_for('index'))
        
        # 设置归还状态
        book.is_borrowed = False
        book.return_date = datetime.now()
        
        db.session.commit()
        logger.info(f"成功归还图书: {book.title}")
        flash(f'成功归还图书: {book.title}')
    except Exception as e:
        logger.error(f"归还图书时出错: {str(e)}")
        flash('归还图书时出错，请查看日志')
    
    return redirect(url_for('index'))

@app.route('/download/<int:id>')
def download_book(id):
    """
    下载图书文件的路由
    
    参数:
        id (int): 要下载的图书ID
    
    返回:
        file: 图书文件或错误消息
    """
    try:
        logger.debug(f"正在下载图书 ID: {id}")
        book = Book.query.get_or_404(id)
        
        # 检查图书是否已借出
        if not book.is_borrowed:
            logger.warning(f"尝试下载未借出的图书: {book.title}")
            flash('该图书未被借出，无法下载！')
            return redirect(url_for('index'))
            
        if book.file_path and os.path.exists(book.file_path):
            logger.info(f"开始下载图书: {book.title}")
            # 获取文件扩展名
            file_ext = os.path.splitext(book.file_path)[1]
            # 使用图书标题作为下载文件名
            download_name = f"{book.title}{file_ext}"
            response = make_response(send_from_directory(
        os.path.dirname(book.file_path),
        os.path.basename(book.file_path),
        as_attachment=True
    ))
            response.headers['Content-Disposition'] = f'attachment; filename="{download_name}"'
            return response
        logger.warning(f"图书文件不存在: {book.file_path}")
        flash('文件不存在！')
    except Exception as e:
        logger.error(f"下载图书时出错: {str(e)}")
        flash('下载图书时出错，请查看日志')
    
    return redirect(url_for('index'))

def allowed_file(filename):
    """
    检查文件扩展名是否允许
    
    参数:
        filename (str): 文件名
    
    返回:
        bool: 是否允许该文件类型
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt', 'epub', 'mobi'}

def allowed_image(filename):
    """
    检查图片文件扩展名是否允许
    
    参数:
        filename (str): 文件名
    
    返回:
        bool: 是否允许该图片类型
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@app.errorhandler(404)
def not_found_error(error):
    """
    404错误处理
    
    参数:
        error: 错误对象
    
    返回:
        template: 404错误页面
    """
    logger.error(f"页面未找到: {request.url}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    500错误处理
    
    参数:
        error: 错误对象
    
    返回:
        template: 500错误页面
    """
    logger.error(f"服务器错误: {str(error)}")
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()  # 确保数据库表存在
    app.run(debug=True) 