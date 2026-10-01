# 小学数学练习题 PDF 生成器

为小学一年级生成 **10以内加减法** 练习题，输出可打印的 A4 PDF 文件。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
# 生成 1 页（默认20题）练习题
python math_generator.py

# 生成 3 页练习题，指定文件名
python math_generator.py -o homework.pdf -p 3

# 同时生成答案卷
python math_generator.py -o answers.pdf -p 2 --answers
```

## 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--output` | `-o` | `math_practice_时间戳.pdf` | 输出文件路径 |
| `--pages` | `-p` | `1` | 生成页数 |
| `--problems` | `-n` | `20` | 每页题目数量 |
| `--cols` | `-c` | `2` | 每行列数 |
| `--max` | | `10` | 数字上限（默认10以内） |
| `--answers` | | 不显示 | 在PDF中显示答案 |
| `--title` | | `10以内加减法练习` | 页面标题 |

## 使用示例

```bash
# 生成 5 页、每页 20 道题的练习册
python math_generator.py -o workbook.pdf -p 5

# 生成对应答案卷
python math_generator.py -o workbook_answers.pdf -p 5 --answers

# 20以内加减法（进阶版）
python math_generator.py --max 20 --title "20以内加减法练习" -p 2

# 每页 4 列密集版
python math_generator.py -c 4 -n 40 -o dense.pdf
```

## 项目结构

```
math-questions-generator/
├── math_generator.py   # 主程序
├── requirements.txt    # 依赖
└── README.md
```
