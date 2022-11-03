# PDF OCR Searching

## 介绍

某些 PDF 扫描版书记无法使用基于文字的搜索

## 使用

安装依赖

```bash
pip3 install pillow pytesseract PyMuPDF
sudo apt-get install tesseract-ocr
```

或按照 [ref](https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/) 说明安装 tesseract-ocr 的 windos 版本

还需要通过 [tessdata-fast](https://github.com/tesseract-ocr/tessdata_fast) 或 [tessdata](https://github.com/tesseract-ocr/tessdata) 下载中文识别模型

可通过 tesseract 官网 查找中文模型名称

目前, 只能在 `pdf-ocrsearch.py` 中标明 要查找的 PDF 文件绝对路径, 和要查找的关键词

```python
SEARCHING_TARGET = "软件"
PDF_file = Path(r"test.pdf")
```

## 效果

在使用多线程优化之后, 可以达到 平均 2s 检测一页. 是不使用优化的一半.

OCR 搜索时长是最大的瓶颈, 只可能使用搜索中间结果缓存, 不过如此意义不大

## 后续

- 提升搜索速度, 目标达到每秒搜索 100 页
- 命令行给出搜索结果附近的语境
- 支持中英文混合文本, 比如 CS 专业书籍
