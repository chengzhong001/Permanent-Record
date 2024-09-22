# from pprint import pprint
from pypdf import PdfReader, PdfWriter
import re


# 输入和输出文件路径
input_pdf_path = "doc/永久档案原始.pdf"
output_pdf_path = "doc/永久档案（爱德华·斯诺登）.pdf"

# 打开并读取现有PDF文件
book_marks_dict = {}

with open(input_pdf_path, "rb") as input_file:
    reader = PdfReader(input_file)
    with open("book_marks.txt", "w") as book_marks:
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()  # 提取文本内容

            if "EDWARD Contents 目 录" in content:
                book_marks.write(f"{page_num}-目录\n")
                book_marks_dict["目录"] = {"page": page_num}
                print(f"目录页码: {page_num}")

            if "            前 言" in content:
                book_marks.write(f"{page_num}-前言\n")
                book_marks_dict["前言"] = {"page": page_num}
                print(f"前言页码: {page_num}")

            if page_num > 10:
                pattern = r"Part(?:One|Two|Three)\s+第[一二三四五六七八九十]+部"
                matches = re.findall(pattern, content)
                for match in matches:
                    book_marks.write(f"{page_num}-{match.split()[-1]}\n")
                    book_marks_dict[match.split()[-1]] = {
                        "page": page_num,
                        "children": [],
                    }
                    print(f"章节页码: {page_num}, 章节标题: {match.split()[-1]}")

            pattern = r"\s{15,}第[一二三四五六七八九十百千]+章\s+[\u4e00-\u9fff]+"

            # 查找所有匹配项
            matches = re.findall(pattern, content)

            # 输出匹配结果
            for match in matches:

                book_marks.write(f"  {page_num}-{match.strip()}\n")
                last_key = list(book_marks_dict.keys())[-1]
                book_marks_dict[last_key]["children"].append(
                    {match.strip(): {"page": page_num}}
                )
                print(f"  子章节页码: {page_num}, 子章节标题: {match.strip()}")

            if "           致 谢 " in content:
                book_marks.write(f"{page_num}-致 谢\n")
                book_marks_dict["致谢"] = {"page": page_num}
                print(f"致谢页码: {page_num}")

    writer = PdfWriter()

    # 将所有页面复制到新的PDF文件
    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    print("开始添加书签")
    for key, value in book_marks_dict.items():
        parent_outline_item = writer.add_outline_item(key, value["page"])

        if "children" in value:
            for child in value["children"]:
                for k, v in child.items():
                    writer.add_outline_item(k, v["page"], parent=parent_outline_item)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
print(f"书签已成功添加到 {output_pdf_path}")
