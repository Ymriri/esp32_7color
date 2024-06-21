#!/bin/bash

# 遍历当前目录下所有带空格的文件
for file in *\ *; do
    # 检查文件是否存在，防止没有带空格的文件时出错
    if [ -e "$file" ]; then
        # 将文件名中的空格替换为下划线或删除空格
        # 使用 ${file// /_} 将空格替换成下划线
        # 使用 ${file// /} 则是直接删除空格
        new_file="${file// /}"
        
        # 重命名文件
        mv "$file" "$new_file"
        echo "Renamed '$file' to '$new_file'"
    fi
done
