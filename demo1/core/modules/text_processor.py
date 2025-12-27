"""
文本处理器 - 示例业务逻辑模块

这个处理器展示如何在 core 层实现纯业务逻辑
"""

from ..base import BaseCore


class TextProcessor(BaseCore):
    """
    文本处理器
    
    功能：
    - 文本转换（大写、小写、首字母大写）
    - 文本统计（字符数、单词数、行数）
    - 文本分析
    """
    
    def __init__(self):
        super().__init__()
        self.input_text = None
        self.result = None
        self.statistics = {}
    
    def initialize(self):
        """初始化处理器"""
        self._initialized = True
        print("✅ TextProcessor 已初始化")
    
    def process(self, *args, **kwargs):
        """
        处理文本
        
        Args:
            args[0] (str): 输入文本
            kwargs['options']: 处理选项
                - mode: 'upper', 'lower', 'title', 'analyze'
        
        Returns:
            bool: 处理是否成功
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # 获取参数
            self.input_text = args[0] if args else ""
            options = kwargs.get('options', {})
            mode = options.get('mode', 'upper')
            
            print(f"📝 处理文本: {len(self.input_text)} 字符")
            print(f"🔧 模式: {mode}")
            
            # 根据模式处理
            if mode == 'upper':
                self.result = self.to_upper()
            elif mode == 'lower':
                self.result = self.to_lower()
            elif mode == 'title':
                self.result = self.to_title()
            elif mode == 'analyze':
                self.result = self.analyze_text()
            else:
                self.result = self.input_text
            
            # 计算统计信息
            self.calculate_statistics()
            
            print("✨ 处理完成")
            return True
        
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            return False
    
    def cleanup(self):
        """清理资源"""
        self.input_text = None
        self.result = None
        self.statistics = {}
        self._initialized = False
        print("🧹 TextProcessor 已清理")
    
    # ==================== 业务逻辑方法 ====================
    
    def to_upper(self):
        """转大写"""
        return self.input_text.upper()
    
    def to_lower(self):
        """转小写"""
        return self.input_text.lower()
    
    def to_title(self):
        """首字母大写"""
        return self.input_text.title()
    
    def analyze_text(self):
        """分析文本"""
        analysis = []
        analysis.append(f"原文: {self.input_text}")
        analysis.append(f"大写: {self.input_text.upper()}")
        analysis.append(f"小写: {self.input_text.lower()}")
        analysis.append(f"首字母大写: {self.input_text.title()}")
        return "\n".join(analysis)
    
    def calculate_statistics(self):
        """计算统计信息"""
        if self.input_text:
            self.statistics = {
                'char_count': len(self.input_text),
                'word_count': len(self.input_text.split()),
                'line_count': self.input_text.count('\n') + 1,
                'space_count': self.input_text.count(' '),
            }
        else:
            self.statistics = {}
    
    def get_result(self):
        """获取处理结果"""
        return self.result
    
    def get_statistics(self):
        """获取统计信息"""
        return self.statistics
