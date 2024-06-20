#!/bin/zsh

echo "切换jdk17..."

echo "准备打包...."
mvn package -DskipTests

echo "打包完成!"
