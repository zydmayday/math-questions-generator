"""
小学一年级数学题 PDF 生成器
生成10以内加减法练习题，A4纸打印格式
"""

import random
import argparse
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
import os
import sys


# ─── 字体注册 ───────────────────────────────────────────────────────────────

def register_chinese_font():
    """尝试注册中文字体，返回可用字体名"""
    # Windows 常见中文字体路径
    font_candidates = [
        ("SimSun",   r"C:\Windows\Fonts\simsun.ttc"),
        ("SimHei",   r"C:\Windows\Fonts\simhei.ttf"),
        ("Microsoft YaHei", r"C:\Windows\Fonts\msyh.ttc"),
        ("Arial",    r"C:\Windows\Fonts\arial.ttf"),
    ]
    for name, path in font_candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                return name
            except Exception:
                continue
    return "Helvetica"  # 回退到内置字体


# ─── 题目生成 ────────────────────────────────────────────────────────────────

def generate_problems(count: int = 20, max_num: int = 10) -> list[dict]:
    """
    生成加减法题目列表，结果在 0~max_num 之间。

    返回每题格式:
        {"a": int, "op": "+"/"-", "b": int, "answer": int}
    """
    problems = []
    seen = set()

    attempts = 0
    while len(problems) < count and attempts < count * 20:
        attempts += 1
        op = random.choice(["+", "-"])

        if op == "+":
            a = random.randint(0, max_num)
            b = random.randint(0, max_num - a)
            answer = a + b
        else:
            a = random.randint(0, max_num)
            b = random.randint(0, a)          # 保证结果 ≥ 0
            answer = a - b

        key = (a, op, b)
        if key not in seen:
            seen.add(key)
            problems.append({"a": a, "op": op, "b": b, "answer": answer})

    # 如果去重后不足，允许重复补齐
    while len(problems) < count:
        p = random.choice(problems)
        problems.append(p.copy())

    random.shuffle(problems)
    return problems[:count]


# ─── PDF 渲染 ────────────────────────────────────────────────────────────────

def draw_page(
    c: canvas.Canvas,
    problems: list[dict],
    page_num: int,
    total_pages: int,
    font_name: str,
    show_answers: bool = False,
    title: str = "10以内加减法练习",
    cols: int = 2,
):
    """在当前页面绘制题目"""
    page_w, page_h = A4

    # ── 标题 ──────────────────────────────────────────────────────────────────
    c.setFont(font_name, 18)
    c.setFillColor(colors.HexColor("#2c3e50"))
    c.drawCentredString(page_w / 2, page_h - 1.5 * cm, title)

    # ── 副标题：姓名 / 日期 / 得分 ─────────────────────────────────────────────
    c.setFont(font_name, 11)
    c.setFillColor(colors.HexColor("#555555"))
    info_y = page_h - 2.5 * cm
    c.drawString(1.8 * cm, info_y, "姓名：＿＿＿＿＿＿")
    c.drawCentredString(page_w / 2, info_y, f"日期：＿＿＿＿月＿＿＿＿日")
    c.drawRightString(page_w - 1.8 * cm, info_y, "得分：＿＿＿＿＿＿")

    # ── 分隔线 ────────────────────────────────────────────────────────────────
    c.setStrokeColor(colors.HexColor("#aaaaaa"))
    c.setLineWidth(0.5)
    c.line(1.5 * cm, info_y - 0.4 * cm, page_w - 1.5 * cm, info_y - 0.4 * cm)

    # ── 题目区域 ──────────────────────────────────────────────────────────────
    rows = (len(problems) + cols - 1) // cols

    margin_x = 1.8 * cm
    margin_top = info_y - 1.2 * cm
    margin_bottom = 1.8 * cm
    col_width = (page_w - 2 * margin_x) / cols
    row_height = (margin_top - margin_bottom) / rows

    c.setFillColor(colors.black)

    for idx, prob in enumerate(problems):
        col = idx % cols
        row = idx // cols

        cell_x = margin_x + col * col_width
        cell_y = margin_top - (row + 1) * row_height

        # 题号
        num_str = f"{idx + 1:02d}."
        c.setFont(font_name, 11)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(cell_x + 0.3 * cm, cell_y + row_height * 0.5, num_str)

        # 算式起始 x 坐标
        expr_x = cell_x + 1.2 * cm
        expr_y = cell_y + row_height * 0.5 - 0.2 * cm

        # 算式（不含空白答案位）
        expr = f"{prob['a']}  {prob['op']}  {prob['b']}  ="
        c.setFont(font_name, 20)
        c.setFillColor(colors.HexColor("#1a1a2e"))
        c.drawString(expr_x, expr_y, expr)

        # 算式实际宽度（用于定位答案）
        expr_width = stringWidth(expr, font_name, 20)
        ans_x = expr_x + expr_width + 0.2 * cm  # = 号之后留一点间隙

        # 答案（可选）
        if show_answers:
            ans_str = str(prob["answer"])
            c.setFont(font_name, 20)
            c.setFillColor(colors.HexColor("#c0392b"))
            c.drawString(ans_x, expr_y, ans_str)
        else:
            # 答案框：下划线，与算式基线对齐
            ans_y = expr_y - 0.05 * cm
            c.setStrokeColor(colors.HexColor("#333333"))
            c.setLineWidth(1)
            c.line(ans_x, ans_y, ans_x + 1.0 * cm, ans_y)

    # ── 页码 ──────────────────────────────────────────────────────────────────
    c.setFont(font_name, 9)
    c.setFillColor(colors.HexColor("#aaaaaa"))
    c.drawCentredString(
        page_w / 2,
        0.8 * cm,
        f"第 {page_num} 页 / 共 {total_pages} 页",
    )


# ─── 主函数 ──────────────────────────────────────────────────────────────────

def generate_pdf(
    output_path: str = "math_practice.pdf",
    pages: int = 1,
    problems_per_page: int = 20,
    cols: int = 2,
    max_num: int = 10,
    show_answers: bool = False,
    title: str = "10以内加减法练习",
):
    """
    生成数学练习题 PDF。

    Args:
        output_path:        输出文件路径
        pages:              总页数
        problems_per_page:  每页题目数
        cols:               每行列数
        max_num:            数字上限（默认10以内）
        show_answers:       是否显示答案
        title:              页面标题
    """
    font_name = register_chinese_font()

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(title)
    c.setAuthor("Math Questions Generator")
    c.setSubject(f"{max_num}以内加减法练习题")

    for page_num in range(1, pages + 1):
        problems = generate_problems(problems_per_page, max_num)
        draw_page(
            c,
            problems,
            page_num=page_num,
            total_pages=pages,
            font_name=font_name,
            show_answers=show_answers,
            title=title,
            cols=cols,
        )
        if page_num < pages:
            c.showPage()

    c.save()
    print(f"[OK] PDF generated: {output_path}  ({pages} pages, {problems_per_page} problems/page)")


# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="生成小学加减法练习题 PDF（A4 可打印）",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-o", "--output",
        default=f"math_practice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        help="输出 PDF 文件路径（默认：math_practice_时间戳.pdf）",
    )
    parser.add_argument(
        "-p", "--pages",
        type=int, default=1,
        help="生成页数（默认：1）",
    )
    parser.add_argument(
        "-n", "--problems",
        type=int, default=20,
        help="每页题目数量（默认：20）",
    )
    parser.add_argument(
        "-c", "--cols",
        type=int, default=2,
        help="每行列数（默认：2）",
    )
    parser.add_argument(
        "--max",
        type=int, default=10,
        help="数字上限，如 10 表示 10以内（默认：10）",
    )
    parser.add_argument(
        "--answers",
        action="store_true",
        help="在 PDF 中显示答案（用于生成答案卷）",
    )
    parser.add_argument(
        "--title",
        default="10以内加减法练习",
        help="PDF 页面标题（默认：10以内加减法练习）",
    )

    args = parser.parse_args()

    generate_pdf(
        output_path=args.output,
        pages=args.pages,
        problems_per_page=args.problems,
        cols=args.cols,
        max_num=args.max,
        show_answers=args.answers,
        title=args.title,
    )


if __name__ == "__main__":
    main()
