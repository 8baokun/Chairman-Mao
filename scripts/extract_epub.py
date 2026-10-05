#!/usr/bin/env python3
"""
提取EPUB文件内容并分类保存
"""

import os
import sys
import zipfile
import re
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import html2text

def extract_epub_content(epub_path, output_dir):
    """提取EPUB内容并保存为文本文件"""
    try:
        # 读取EPUB文件
        book = epub.read_epub(epub_path)
        
        print(f"正在处理: {epub_path}")
        print(f"书籍标题: {book.title}")
        print(f"作者: {book.get_metadata('DC', 'creator')}")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # HTML转文本转换器
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        
        # 提取所有章节
        all_content = ""
        chapter_contents = []
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # 解析HTML内容
                content = item.get_content().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(content, 'html.parser')
                
                # 获取文本
                text = h.handle(str(soup))
                
                # 简单的章节检测（基于常见标题模式）
                if len(text.strip()) > 500:  # 只保存较长的章节
                    chapter_contents.append(text)
                    all_content += text + "\n\n" + "="*80 + "\n\n"
        
        # 保存完整内容
        with open(os.path.join(output_dir, "毛泽东选集完整内容.txt"), "w", encoding="utf-8") as f:
            f.write(all_content)
        
        # 按章节保存
        for i, chapter in enumerate(chapter_contents[:50]):  # 最多保存50章
            with open(os.path.join(output_dir, f"章节_{i+1:03d}.txt"), "w", encoding="utf-8") as f:
                f.write(chapter)
        
        print(f"提取完成！保存到: {output_dir}")
        print(f"总章节数: {len(chapter_contents)}")
        print(f"总字符数: {len(all_content)}")
        
        return all_content, len(chapter_contents)
        
    except Exception as e:
        print(f"处理EPUB文件时出错: {e}")
        return None, 0

def extract_key_concepts(content, output_file):
    """从内容中提取关键概念和引用"""
    try:
        # 查找毛泽东的经典引用（带引号的内容）
        quotes = re.findall(r'["「](.+?)["」]', content)
        
        # 查找常见的心智模型相关词汇
        mental_models_keywords = [
            '矛盾', '实事求是', '群众路线', '统一战线', '独立自主',
            '持久战', '战略', '战术', '农村包围城市', '主要矛盾',
            '次要矛盾', '对立统一', '实践', '理论', '调查研究'
        ]
        
        # 统计关键词出现频率
        keyword_counts = {}
        for keyword in mental_models_keywords:
            count = len(re.findall(keyword, content))
            if count > 0:
                keyword_counts[keyword] = count
        
        # 保存提取结果
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 毛泽东选集关键概念提取\n\n")
            
            f.write("## 高频心智模型相关词汇\n")
            f.write("| 关键词 | 出现次数 |\n")
            f.write("|--------|----------|\n")
            for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {keyword} | {count} |\n")
            
            f.write("\n## 经典引用示例（前20条）\n")
            for i, quote in enumerate(quotes[:20]):
                if len(quote) > 10 and len(quote) < 500:  # 过滤太短或太长的
                    f.write(f"{i+1}. \"{quote}\"\n\n")
        
        print(f"关键概念提取完成！保存到: {output_file}")
        print(f"发现经典引用: {len(quotes)}条")
        print(f"高频关键词: {len(keyword_counts)}个")
        
        return keyword_counts, quotes
        
    except Exception as e:
        print(f"提取关键概念时出错: {e}")
        return {}, []

if __name__ == "__main__":
    epub_path = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/books/毛泽东选集(1-4卷).epub"
    output_dir = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/extracted"
    concepts_file = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/extracted/关键概念分析.md"
    
    # 提取内容
    content, chapter_count = extract_epub_content(epub_path, output_dir)
    
    if content:
        # 提取关键概念
        keyword_counts, quotes = extract_key_concepts(content, concepts_file)
        
        print(f"\n=== 提取结果总结 ===")
        print(f"EPUB文件: {os.path.basename(epub_path)}")
        print(f"章节数量: {chapter_count}")
        print(f"内容大小: {len(content):,} 字符")
        print(f"高频关键词数量: {len(keyword_counts)}")
        print(f"经典引用数量: {len(quotes)}")
        print(f"输出目录: {output_dir}")
    else:
        print("EPUB内容提取失败！")