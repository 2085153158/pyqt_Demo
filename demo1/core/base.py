"""
核心业务逻辑基类
"""
from abc import ABC, abstractmethod


class BaseCore(ABC):
    """业务逻辑基类"""
    
    def __init__(self):
        self._initialized = False
    
    @abstractmethod
    def initialize(self):
        """初始化"""
        pass
    
    @abstractmethod
    def process(self, *args, **kwargs):
        """处理逻辑"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass
