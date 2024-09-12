#!/bin/bash
## 初始文件名
filename="$1"

# 用于存储已经处理过的文件，避免重复处理
declare -A processed_files

# 递归查找依赖模块的函数
find_dependencies() {
  # 查看$1是否在数组中
    if [ -n "${processed_files[$1]}" ]; then
        return
    fi
  
  # 添加文件到已处理列表
  processed_files[$1]=$1

  # 查找文件中的依赖模块
  while read -r module; do
    # 递归查找模块的依赖
    if [ -f "${module}.sv" ]; then
      find_dependencies "${module}.sv"
    elif [ -f "${module}.v" ]; then
      find_dependencies "${module}.v"
    fi
  done < <(grep -E '^\s*[a-zA-Z0-9_]+\s+[a-zA-Z0-9_]+\s* \(' "$1" | awk '{print $1}' | uniq)
}

# 开始查找依赖
find_dependencies "$filename"

# 输出所有查找到的文件
echo ${processed_files[@]}
