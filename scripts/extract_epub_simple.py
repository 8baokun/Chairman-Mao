#!/usr/bin/env python3
"""
简单的EPUB内容提取
"""

import zipfile
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_text_from_epub(epub_path, output_dir):
    """从EPUB文件中提取文本内容"""
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 打开EPUB文件（EPUB是zip格式）
        with zipfile.ZipFile(epub_path, 'r') as epub:
            # 列出所有文件
            file_list = epub.namelist()
            print(f"EPUB中包含 {len(file_list)} 个文件")
            
            # 查找内容文件（通常是HTML/XML格式）
            content_files = []
            for file in file_list:
                if file.endswith(('.html', '.xhtml', '.htm', '.xml')):
                    content_files.append(file)
            
            print(f"找到 {len(content_files)} 个内容文件")
            
            all_text = ""
            
            # 提取每个内容文件
            for i, content_file in enumerate(content_files[:20]):  # 限制前20个文件
                try:
                    # 读取文件内容
                    content = epub.read(content_file)
                    
                    # 尝试解码
                    try:
                        text = content.decode('utf-8')
                    except:
                        try:
                            text = content.decode('gbk')
                        except:
                            text = content.decode('utf-8', errors='ignore')
                    
                    # 提取文本（简单的HTML标签去除）
                    text = re.sub(r'<[^>]+>', ' ', text)
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()
                    
                    if len(text) > 100:  # 只保存有内容的文件
                        # 保存单个文件
                        file_path = os.path.join(output_dir, f"content_{i+1:03d}.txt")
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(text[:5000])  # 只保存前5000字符
                        
                        all_text += text + "\n\n"
                        
                except Exception as e:
                    print(f"处理文件 {content_file} 时出错: {e}")
            
            # 保存完整文本
            if all_text:
                full_path = os.path.join(output_dir, "毛泽东选集_完整提取.txt")
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(all_text)
                
                print(f"完整文本已保存到: {full_path}")
                print(f"总字符数: {len(all_text):,}")
                
                return all_text
            else:
                print("未能提取到文本内容")
                return None
                
    except Exception as e:
        print(f"打开EPUB文件时出错: {e}")
        return None

def analyze_key_concepts(text, output_file):
    """分析文本中的关键概念"""
    
    if not text:
        return
    
    # 关键概念列表
    concepts = [
        "矛盾", "实事求是", "群众路线", "统一战线", "独立自主",
        "持久战", "战略", "战术", "农村包围城市", "主要矛盾",
        "次要矛盾", "对立统一", "实践", "理论", "调查研究",
        "人民", "革命", "战争", "政治", "经济", "文化",
        "帝国主义", "封建主义", "官僚资本主义", "社会主义",
        "共产主义", "马克思主义", "列宁主义", "毛泽东思想"
    ]
    
    # 分析每个概念的出现频率
    concept_counts = {}
    for concept in concepts:
        count = len(re.findall(concept, text))
        if count > 0:
            concept_counts[concept] = count
    
    # 查找经典引用（带引号的内容）
    quotes = re.findall(r'["「](.+?)["」]', text)
    
    # 保存分析结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 毛泽东选集关键概念分析\n\n")
        
        f.write("## 统计信息\n")
        f.write(f"- 分析时间: {os.path.basename(output_file)}\n")
        f.write(f"- 文本大小: {len(text):,} 字符\n")
        f.write(f"- 关键概念数量: {len(concept_counts)}\n")
        f.write(f"- 经典引用数量: {len(quotes)}\n\n")
        
        f.write("## 关键概念频率排名\n")
        f.write("| 概念 | 出现次数 | 重要性 |\n")
        f.write("|------|----------|--------|\n")
        
        # 按频率排序
        sorted_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)
        
        for concept, count in sorted_concepts:
            if count > 100:
                importance = "★★★★★"
            elif count > 50:
                importance = "★★★★"
            elif count > 20:
                importance = "★★★"
            elif count > 10:
                importance = "★★"
            else:
                importance = "★"
            
            f.write(f"| {concept} | {count} | {importance} |\n")
        
        f.write("\n## 高频概念分析\n")
        
        # 分析前5个高频概念
        top_concepts = sorted_concepts[:5]
        for concept, count in top_concepts:
            f.write(f"\n### {concept} (出现{count}次)\n")
            
            # 查找包含该概念的句子
            sentences = []
            for sentence in re.split(r'[。！？]', text):
                if concept in sentence and len(sentence) > 10:
                    sentences.append(sentence.strip())
                    if len(sentences) >= 3:
                        break
            
            if sentences:
                f.write("**相关论述:**\n")
                for i, sentence in enumerate(sentences[:3], 1):
                    f.write(f"{i}. {sentence}。\n")
        
        f.write("\n## 经典引用示例（前15条）\n")
        for i, quote in enumerate(quotes[:15], 1):
            if 20 < len(quote) < 200:  # 过滤太短或太长的
                f.write(f"{i}. \"{quote}\"\n\n")
        
        f.write("\n## 文本样本\n")
        f.write("```\n")
        # 取文本的前1000字符作为样本
        sample = text[:1000] + "..." if len(text) > 1000 else text
        f.write(sample)
        f.write("\n```\n")
    
    print(f"概念分析已保存到: {output_file}")
    print(f"最高频概念: {sorted_concepts[0][0]} (出现{sorted_concepts[0][1]}次)")
    
    return concept_counts, quotes

def main():
    epub_path = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/books/毛泽东选集(1-4卷).epub"
    output_dir = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/extracted"
    analysis_file = os.path.join(output_dir, "关键概念分析.md")
    
    print("开始提取EPUB内容...")
    text = extract_text_from_epub(epub_path, output_dir)
    
    if text:
        print("\n开始分析关键概念...")
        concept_counts, quotes = analyze_key_concepts(text, analysis_file)
        
        print("\n=== 分析完成 ===")
        print(f"输出目录: {output_dir}")
        print(f"分析文件: {analysis_file}")
        print(f"提取字符数: {len(text):,}")
        print(f"发现概念数: {len(concept_counts)}")
        print(f"发现引用数: {len(quotes)}")
    else:
        print("EPUB内容提取失败！")

if __name__ == "__main__":
    main()