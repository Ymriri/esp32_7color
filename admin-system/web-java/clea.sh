#!/bin/bash

#lastUpdated
delete_files() {
    local dir="$1"

    # 迭代当前目录下的所有文件和文件夹
    for file in "$dir"/*; do
        if [[ -f "$file" && "$file" == *.lastUpdated ]]; then
            # 删除以 ".lastupdat" 结尾的文件
            rm "$file"
            echo "Deleted file: $file"
        elif [[ -d "$file" ]]; then
            # 递归调用 delete_files 函数处理子文件夹
            delete_files "$file"
        fi
    done
}

# 调用 delete_files 函数并传入当前目录
delete_files "."

echo "Deletion complete."
