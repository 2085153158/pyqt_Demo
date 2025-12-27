"""
Core模块模板 - 业务逻辑层

使用方法：
1. 复制这个文件，重命名为你的模块名，如 my_processor.py
2. 修改 YourProcessor 为你的处理器类名
3. 实现 initialize(), process(), cleanup() 方法
4. 添加你的业务逻辑方法

示例：
    from core.my_processor import MyProcessor
    
    processor = MyProcessor()
    processor.initialize()
    result = processor.process(data)
"""

from ..base import BaseCore


class YourProcessor(BaseCore):
    """
    你的业务逻辑处理器
    
    这个类负责纯粹的业务逻辑，不包含UI代码
    """
    
    def __init__(self):
        super().__init__()
        # 初始化你的数据成员
        self.data = None
        self.result = None
        self.config = {}
    
    def initialize(self):
        """
        初始化处理器
        
        在这里进行：
        - 加载配置
        - 初始化资源
        - 建立连接
        """
        self._initialized = True
        print(f"{self.__class__.__name__} 已初始化")
        
        # 你的初始化代码
        # self.config = self.load_config()
        # self.connection = self.setup_connection()
    
    def process(self, *args, **kwargs):
        """
        主处理逻辑
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数，如 options, mode 等
        
        Returns:
            bool: 处理是否成功
        
        示例:
            processor.process(data, options={'mode': 'fast'})
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # 获取参数
            data = args[0] if args else None
            options = kwargs.get('options', {})
            
            print(f"处理数据: {data}")
            print(f"选项: {options}")
            
            # ==================== 你的业务逻辑 ====================
            # 1. 数据验证
            if not self.validate_data(data):
                print("数据验证失败")
                return False
            
            # 2. 数据处理
            self.result = self.process_data(data, options)
            
            # 3. 结果验证
            if not self.validate_result(self.result):
                print("结果验证失败")
                return False
            
            print("处理成功")
            return True
            
        except Exception as e:
            print(f"处理失败: {e}")
            return False
    
    def cleanup(self):
        """
        清理资源
        
        在这里进行：
        - 关闭连接
        - 释放资源
        - 保存状态
        """
        self.data = None
        self.result = None
        self._initialized = False
        print(f"{self.__class__.__name__} 已清理")
    
    # ==================== 业务逻辑方法 ====================
    
    def validate_data(self, data):
        """验证输入数据"""
        if data is None:
            return False
        # 添加你的验证逻辑
        return True
    
    def process_data(self, data, options):
        """处理数据 - 核心业务逻辑"""
        # 这里实现你的核心算法
        result = f"处理结果: {data}"
        return result
    
    def validate_result(self, result):
        """验证处理结果"""
        if result is None:
            return False
        # 添加你的验证逻辑
        return True
    
    def get_result(self):
        """获取处理结果"""
        return self.result
    
    def set_config(self, key, value):
        """设置配置项"""
        self.config[key] = value
    
    def get_config(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)


# ==================== 使用示例 ====================
"""
在 core/__init__.py 中导出：
    from .your_processor import YourProcessor
    __all__ = ['BaseCore', 'DataProcessor', 'YourProcessor']

在代码中使用：
    from core import YourProcessor
    
    processor = YourProcessor()
    processor.initialize()
    success = processor.process(data, options={'mode': 'fast'})
    if success:
        result = processor.get_result()
        print(result)
    processor.cleanup()
"""
