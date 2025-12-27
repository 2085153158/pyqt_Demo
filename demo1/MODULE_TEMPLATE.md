# 📦 模块添加指南

## 项目结构

```
demo1/
├── core/                           # 核心业务逻辑层
│   ├── base.py                    # 基类
│   ├── modules/                   # 模块文件夹
│   │   ├── __init__.py
│   │   ├── text_processor.py     # 文本处理器(示例)
│   │   ├── data_processor.py     # 数据处理器
│   │   └── module_template.py    # 核心处理器模板
│   └── __init__.py
│
├── vievs/                          # 视图UI层(仅存放子功能UI)
│   ├── base_view.py               # 视图基类
│   ├── modules/                   # 功能模块文件夹
│   │   ├── __init__.py
│   │   ├── text_module/          # 文本模块(示例)
│   │   │   ├── __init__.py
│   │   │   └── text_module_ui.py
│   │   └── image_module/         # 图像模块(示例)
│   │       ├── __init__.py
│   │       └── image_module_ui.py
│   ├── templates/                 # 模板文件夹
│   │   ├── __init__.py
│   │   └── ui_module_template.py # UI模板
│   └── __init__.py
│
├── qtmodern/                       # 现代化主题
│   └── resources/
│       └── style.qss              # 样式文件
│
└── main.py                         # 程序入口(包含主界面UI创建)
```

---

## 🚀 添加新模块的步骤

### 步骤 1：创建核心处理器（在 core/modules/ 目录）

创建文件：`core/modules/your_processor.py`

```python
"""
您的功能处理器
"""
from ..base import BaseCore  # 注意：使用 ..base 相对导入

class YourProcessor(BaseCore):
    """您的处理器类"""
    
    def __init__(self):
        super().__init__()
        self.result = ""
    
    def initialize(self):
        """初始化"""
        print("✅ YourProcessor 已初始化")
        return True
    
    def process(self, data=None, options=None):
        """
        处理数据
        
        Args:
            data: 输入数据
            options: 处理选项
            
        Returns:
            bool: 处理是否成功
        """
        try:
            # 在这里实现您的业务逻辑
            self.result = f"处理结果: {data}"
            return True
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            return False
    
    def get_result(self):
        """获取处理结果"""
        return self.result
    
    def cleanup(self):
        """清理资源"""
        print("🧹 YourProcessor 已清理")
```

**更新 `core/modules/__init__.py`：**

```python
"""
核心处理器模块
"""
from .text_processor import TextProcessor
from .data_processor import DataProcessor
from .your_processor import YourProcessor  # 添加这行

__all__ = ['TextProcessor', 'DataProcessor', 'YourProcessor']  # 添加导出
```

**更新 `core/__init__.py`：**

```python
from .base import BaseCore
from .modules import DataProcessor, TextProcessor, YourProcessor  # 添加 YourProcessor

__all__ = ['BaseCore', 'DataProcessor', 'TextProcessor', 'YourProcessor']
```

---

### 步骤 2：创建 UI模块文件夹和UI界面（在 vievs/modules/ 目录）

#### 2.1 创建模块文件夹

```bash
mkdir vievs\modules\your_module
```

#### 2.2 创建 UI文件

创建文件：`vievs/modules/your_module/your_module_ui.py`

```python
"""
您的功能UI模块
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTextEdit, QGroupBox)
from PySide6.QtCore import Qt

class YourModuleUI(QWidget):
    """您的模块UI"""
    
    def __init__(self, parent=None, processor=None):
        super().__init__(parent)
        self.parent_window = parent
        self.processor = processor  # YourProcessor 实例
        
        # 初始化处理器
        if self.processor:
            self.processor.initialize()
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        # 标题
        title = QLabel("🎯 您的功能模块")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # 输入区域
        input_group = QGroupBox("📝 输入")
        input_layout = QVBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("在这里输入...")
        self.input_text.setMaximumHeight(150)
        input_layout.addWidget(self.input_text)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.btn_process = QPushButton("🚀 开始处理")
        self.btn_process.setMinimumHeight(35)
        self.btn_clear = QPushButton("🧹 清空")
        self.btn_clear.setMinimumHeight(35)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_process)
        button_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(button_layout)
        
        # 输出区域
        output_group = QGroupBox("✅ 结果")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("结果将显示在这里...")
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # 添加伸缩
        main_layout.addStretch()
    
    def connect_signals(self):
        """连接信号槽"""
        self.btn_process.clicked.connect(self.on_process_clicked)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
    
    def on_process_clicked(self):
        """处理按钮点击"""
        input_data = self.input_text.toPlainText().strip()
        
        if not input_data:
            self.output_text.append("⚠️ 请先输入内容！")
            return
        
        # 调用核心处理器
        if self.processor:
            success = self.processor.process(input_data)
            
            if success:
                result = self.processor.get_result()
                self.output_text.setPlainText(result)
                self.output_text.append("✨ 处理完成！")
            else:
                self.output_text.append("❌ 处理失败")
    
    def on_clear_clicked(self):
        """清空"""
        self.output_text.clear()
    
    def cleanup(self):
        """清理资源"""
        if self.processor:
            self.processor.cleanup()
```

#### 2.3 创建模块包文件

创建文件：`vievs/modules/your_module/__init__.py`

```python
"""
您的功能模块
"""
from .your_module_ui import YourModuleUI

__all__ = ['YourModuleUI']
```

**更新 `vievs/modules/__init__.py`：**

```python
"""
视图模块包
"""
from .text_module import TextModuleUI
from .image_module import ImageModuleUI
from .your_module import YourModuleUI  # 添加这行

__all__ = ['TextModuleUI', 'ImageModuleUI', 'YourModuleUI']  # 添加导出
```

**更新 `vievs/__init__.py`:**

```python
from .base_view import BaseView
from .modules.text_module import TextModuleUI
from .modules.image_module import ImageModuleUI
from .modules.your_module import YourModuleUI  # 添加这行

__all__ = [
    'BaseView',
    'TextModuleUI',
    'ImageModuleUI',
    'YourModuleUI'  # 添加这行
]
```

---

### 步骤 3：在主窗口中注册模块

编辑 `vievs/main_window.py`，在 `load_modules()` 方法中添加：

```python
def load_modules(self):
    """加载模块 - 双层结构"""
    from vievs.modules.text_module import TextModuleUI
    from vievs.modules.image_module import ImageModuleUI
    from vievs.modules.your_module import YourModuleUI  # 导入您的模块
    from core import TextProcessor, YourProcessor  # 导入处理器
    
    # ========== 1. 图像处理分类 ==========
    self.add_category('图像处理', 0)
    
    # ... 已有模块 ...
    
    # ========== 新增您的分类 ==========
    self.add_category('您的分类', 6)  # 添加新分类（或添加到现有分类）
    
    # 添加您的模块
    your_processor = YourProcessor()
    your_ui = YourModuleUI(self, your_processor)
    self.add_module('您的分类', '您的模块名', your_ui)
```

**或者添加到现有分类：**

```python
# 添加到文本处理分类
self.add_category('文本处理', 2)

# 文本处理模块
text_processor = TextProcessor()
text_ui = TextModuleUI(self, text_processor)
self.add_module('文本处理', '文本处理', text_ui)

# 您的模块（添加到同一分类）
your_processor = YourProcessor()
your_ui = YourModuleUI(self, your_processor)
self.add_module('文本处理', '您的模块', your_ui)
```

---

## 📋 快速添加模块检查清单

- [ ] 1. 在 `core/modules/` 创建处理器类（继承 BaseCore）
- [ ] 2. 更新 `core/modules/__init__.py` 导出新处理器
- [ ] 3. 更新 `core/__init__.py` 导出新处理器
- [ ] 4. 在 `vievs/modules/` 创建模块文件夹
- [ ] 5. 在模块文件夹中创建 UI类（继承 QWidget）
- [ ] 6. 创建模块的 `__init__.py` 并导出UI类
- [ ] 7. 更新 `vievs/modules/__init__.py` 导出UI类
- [ ] 8. 更新 `vievs/__init__.py` 导出UI类
- [ ] 9. 在 `main.py` 的 `MainWindow.load_modules()` 中注册模块
- [ ] 10. 测试运行

---

## 🎯 当前项目已有模块

### 完整功能模块：
1. **文本处理模块** - 完整功能
   - 处理器：`core/modules/text_processor.py`
   - UI：`vievs/modules/text_module/text_module_ui.py`

2. **图像处理模块** - 完整功能
   - UI：`vievs/modules/image_module/image_module_ui.py`

### 占位模块（可替换）：
- 单帧图处理
- 双重编码编码
- 块是处理
- 除工具条
- ImageSteganography
- BruteForceImage
- FrequencyColor
- GIF
- Misc

---

## 👡 推荐的模块结构

为了保持项目的清晰和模块化，建议按以下结构组织模块：

```
vievs/modules/
├── text_module/              # 文本处理模块
│   ├── __init__.py
│   └── text_module_ui.py
│
├── image_module/             # 图像处理模块
│   ├── __init__.py
│   └── image_module_ui.py
│
└── your_module/              # 您的模块
    ├── __init__.py
    └── your_module_ui.py
```

每个模块文件夹应该包含：
- `__init__.py` - 模块包文件，导出UI类
- `*_ui.py` - UI类文件
- （可选）其他辅助文件，如配置文件、资源文件等

---

## 💡 提示

1. **核心处理器**（core）负责业务逻辑，不涉及UI
2. **视图UI**（vievs）负责界面展示，调用核心处理器
3. **分层清晰**，便于测试和维护
4. **样式统一**，使用 qtmodern 主题
5. **模块独立**，互不影响

---

## 🔧 调试技巧

运行程序时，控制台会显示模块加载信息：
```
✅ 分类 'XXX' 添加成功
  ✅ 模块 'XXX' 添加到分类 'XXX'
```

如果有错误，会显示具体信息，方便排查。
