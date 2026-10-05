#!/usr/bin/env python3
"""
处理《毛泽东传》EPUB文件，提取关键信息
"""

import os
import zipfile
import re
import json

def extract_biography_content(biography_path, output_dir):
    """提取传记内容"""
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 打开EPUB文件
        with zipfile.ZipFile(biography_path, 'r') as epub:
            # 列出所有文件
            file_list = epub.namelist()
            
            # 查找内容文件
            content_files = []
            for file in file_list:
                if file.endswith(('.html', '.xhtml', '.htm', '.xml', '.txt')):
                    content_files.append(file)
            
            print(f"找到 {len(content_files)} 个内容文件")
            
            all_text = ""
            
            # 提取内容（限制前30个文件）
            for i, content_file in enumerate(content_files[:30]):
                try:
                    content = epub.read(content_file)
                    try:
                        text = content.decode('utf-8')
                    except:
                        try:
                            text = content.decode('gbk')
                        except:
                            text = content.decode('utf-8', errors='ignore')
                    
                    # 简单的HTML标签去除
                    text = re.sub(r'<[^>]+>', ' ', text)
                    text = re.sub(r'\s+', ' ', text)
                    text = text.strip()
                    
                    if len(text) > 200:
                        all_text += text + "\n\n"
                        
                except Exception as e:
                    continue
            
            # 保存内容
            output_file = os.path.join(output_dir, "毛泽东传_完整内容.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(all_text)
            
            print(f"传记内容已保存到: {output_file}")
            print(f"总字符数: {len(all_text):,}")
            
            return all_text
            
    except Exception as e:
        print(f"处理传记文件时出错: {e}")
        return None

def analyze_biography_key_points(text, output_file):
    """分析传记中的关键点"""
    
    if not text:
        return
    
    # 查找关键章节
    chapters = re.findall(r'第[一二三四五六七八九十]+章[：:]\s*[^。]+', text)
    
    # 查找重要事件
    important_events = re.findall(r'(一九[零一二三四五六七八九十]+年[^。]{10,80})', text)
    
    # 查找评价性语言
    evaluations = re.findall(r'(毛泽东[^。]{10,80}(思想|理论|贡献|错误|失误)[^。]{5,50})', text)
    
    # 查找转折点
    turning_points = re.findall(r'(转折点|关键时期|重大决策|历史关头)[^。]{20,100}', text)
    
    # 保存分析结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 《毛泽东传》关键点分析\n\n")
        
        f.write("## 章节概览\n")
        for i, chapter in enumerate(chapters[:15], 1):
            f.write(f"{i}. {chapter}\n")
        
        f.write("\n## 重要事件（前20个）\n")
        for i, event in enumerate(important_events[:20], 1):
            f.write(f"{i}. {event}。\n")
        
        f.write("\n## 关键评价\n")
        for i, evaluation in enumerate(evaluations[:10], 1):
            f.write(f"{i}. {evaluation}。\n")
        
        f.write("\n## 历史转折点\n")
        for i, point in enumerate(turning_points[:10], 1):
            f.write(f"{i}. {point}。\n")
        
        f.write("\n## 文本样本\n")
        f.write("```\n")
        sample = text[:1500] + "..." if len(text) > 1500 else text
        f.write(sample)
        f.write("\n```\n")
    
    print(f"传记分析已保存到: {output_file}")
    print(f"发现章节: {len(chapters)}个")
    print(f"重要事件: {len(important_events)}个")
    print(f"关键评价: {len(evaluations)}个")
    print(f"转折点: {len(turning_points)}个")

def extract_timeline_from_biography(text, timeline_file):
    """从传记中提取时间线"""
    
    # 查找年份模式
    year_pattern = r'(一九[零一二三四五六七八九十]+年)([^。]{20,100})'
    matches = re.findall(year_pattern, text)
    
    # 转换为数字年份
    year_map = {
        '一九二': '192', '一九三': '193', '一九四': '194', '一九五': '195',
        '一九六': '196', '一九七': '197', '一九八': '198', '一九九': '199',
        '一九〇': '190', '一九一': '191'
    }
    
    timeline = []
    for year_str, event in matches:
        for key, value in year_map.items():
            if year_str.startswith(key):
                year = value + year_str[-1]
                timeline.append((year, event.strip()))
                break
    
    # 去重并排序
    unique_timeline = []
    seen = set()
    for year, event in timeline:
        key = f"{year}_{event[:50]}"
        if key not in seen:
            seen.add(key)
            unique_timeline.append((year, event))
    
    # 按年份排序
    unique_timeline.sort(key=lambda x: int(x[0]))
    
    # 保存时间线
    with open(timeline_file, 'w', encoding='utf-8') as f:
        f.write("# 毛泽东生平时间线（从传记中提取）\n\n")
        
        current_decade = None
        for year, event in unique_timeline[:50]:  # 只取前50个
            decade = year[:3] + "0年代"
            if decade != current_decade:
                f.write(f"\n## {decade}\n")
                current_decade = decade
            
            f.write(f"- **{year}年**：{event}。\n")
    
    print(f"时间线已保存到: {timeline_file}")
    print(f"提取时间点: {len(unique_timeline)}个")

def main():
    biography_path = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/books/毛泽东传(逢先知_金冲及).epub"
    output_dir = "/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/biography_extracted"
    
    print("开始提取《毛泽东传》内容...")
    text = extract_biography_content(biography_path, output_dir)
    
    if text:
        print("\n开始分析传记关键点...")
        analysis_file = os.path.join(output_dir, "传记关键点分析.md")
        analyze_biography_key_points(text, analysis_file)
        
        print("\n开始提取时间线...")
        timeline_file = os.path.join(output_dir, "毛泽东时间线.md")
        extract_timeline_from_biography(text, timeline_file)
        
        print("\n=== 传记处理完成 ===")
        print(f"输出目录: {output_dir}")
        print(f"分析文件: {analysis_file}")
        print(f"时间线文件: {timeline_file}")
    else:
        print("传记内容提取失败！")

if __name__ == "__main__":
    main()