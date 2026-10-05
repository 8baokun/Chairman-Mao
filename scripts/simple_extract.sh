#!/bin/bash
# 简单的EPUB内容提取脚本

EPUB_PATH="/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/books/毛泽东选集(1-4卷).epub"
OUTPUT_DIR="/root/.openclaw/workspace/skills/mao-zedong-perspective/references/sources/extracted"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 使用unzip提取EPUB内容（EPUB本质上是zip文件）
echo "正在提取EPUB文件内容..."
unzip -q "$EPUB_PATH" -d "$OUTPUT_DIR/temp_epub" 2>/dev/null

# 查找并提取文本内容
echo "正在处理文本内容..."
find "$OUTPUT_DIR/temp_epub" -name "*.html" -o -name "*.xhtml" -o -name "*.htm" | while read file; do
    # 使用lynx提取纯文本
    if command -v lynx >/dev/null 2>&1; then
        lynx -dump -nolist "$file" >> "$OUTPUT_DIR/raw_text.txt" 2>/dev/null
    else
        # 使用简单的文本提取
        grep -o '<p>[^<]*</p>' "$file" 2>/dev/null | sed 's/<[^>]*>//g' >> "$OUTPUT_DIR/raw_text.txt"
    fi
done

# 清理临时文件
rm -rf "$OUTPUT_DIR/temp_epub"

# 统计和整理
if [ -f "$OUTPUT_DIR/raw_text.txt" ]; then
    # 计算文件大小
    CHAR_COUNT=$(wc -m < "$OUTPUT_DIR/raw_text.txt")
    LINE_COUNT=$(wc -l < "$OUTPUT_DIR/raw_text.txt")
    
    # 提取关键概念
    echo "正在分析关键概念..."
    
    # 定义关键概念列表
    CONCEPTS=("矛盾" "实事求是" "群众路线" "统一战线" "独立自主" "持久战" "战略" "战术" "农村包围城市" "主要矛盾" "次要矛盾" "对立统一" "实践" "理论" "调查研究")
    
    # 创建分析文件
    ANALYSIS_FILE="$OUTPUT_DIR/概念分析.md"
    echo "# 毛泽东选集概念分析" > "$ANALYSIS_FILE"
    echo "" >> "$ANALYSIS_FILE"
    echo "## 文件信息" >> "$ANALYSIS_FILE"
    echo "- 源文件: 毛泽东选集(1-4卷).epub" >> "$ANALYSIS_FILE"
    echo "- 提取时间: $(date)" >> "$ANALYSIS_FILE"
    echo "- 总字符数: $CHAR_COUNT" >> "$ANALYSIS_FILE"
    echo "- 总行数: $LINE_COUNT" >> "$ANALYSIS_FILE"
    echo "" >> "$ANALYSIS_FILE"
    
    echo "## 关键概念出现频率" >> "$ANALYSIS_FILE"
    echo "| 概念 | 出现次数 | 示例 |" >> "$ANALYSIS_FILE"
    echo "|------|----------|------|" >> "$ANALYSIS_FILE"
    
    for concept in "${CONCEPTS[@]}"; do
        COUNT=$(grep -o "$concept" "$OUTPUT_DIR/raw_text.txt" | wc -l)
        if [ $COUNT -gt 0 ]; then
            # 查找一个示例
            EXAMPLE=$(grep -m1 "$concept" "$OUTPUT_DIR/raw_text.txt" | head -c 100)
            echo "| $concept | $COUNT | $EXAMPLE... |" >> "$ANALYSIS_FILE"
        fi
    done
    
    echo "" >> "$ANALYSIS_FILE"
    echo "## 经典引用示例" >> "$ANALYSIS_FILE"
    
    # 提取可能的引用（带引号的内容）
    grep -o '["「][^"」]*["」]' "$OUTPUT_DIR/raw_text.txt" | head -20 | while read -r quote; do
        echo "- $quote" >> "$ANALYSIS_FILE"
    done
    
    echo "" >> "$ANALYSIS_FILE"
    echo "## 内容样本" >> "$ANALYSIS_FILE"
    echo "\`\`\`" >> "$ANALYSIS_FILE"
    head -100 "$OUTPUT_DIR/raw_text.txt" >> "$ANALYSIS_FILE"
    echo "\`\`\`" >> "$ANALYSIS_FILE"
    
    echo "=== 提取完成 ==="
    echo "输出目录: $OUTPUT_DIR"
    echo "总字符数: $CHAR_COUNT"
    echo "分析文件: $ANALYSIS_FILE"
else
    echo "错误: 未能提取文本内容"
    exit 1
fi