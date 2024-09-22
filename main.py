from pypdf import PdfReader, PdfWriter
import re

def extract_and_write_bookmark(content, page_num, keyword, label, bookmarks, bookmarks_dict):
    if keyword in content:
        bookmarks.write(f"{page_num}-{label}\n")
        bookmarks_dict[label] = {"page": page_num}
        print(f"{label}页码: {page_num}")

def extract_and_write_chapter(content, page_num, pattern, label_prefix, bookmarks, bookmarks_dict):
    matches = re.findall(pattern, content)
    for match in matches:
        bookmarks.write(f"{page_num}-{match.split()[-1]}\n")
        bookmarks_dict[match.split()[-1]] = {"page": page_num, "children": []}
        print(f"章节页码: {page_num}, 章节标题: {match.split()[-1]}")

def extract_and_write_subchapter(content, page_num, pattern, bookmarks, bookmarks_dict):
    matches = re.findall(pattern, content)
    for match in matches:
        bookmarks.write(f"  {page_num}-{match.strip()}\n")
        last_key = list(bookmarks_dict.keys())[-1]
        bookmarks_dict[last_key]["children"].append({match.strip(): {"page": page_num}})
        print(f"  子章节页码: {page_num}, 子章节标题: {match.strip()}")

input_pdf_path = "doc/永久档案原始.pdf"
output_pdf_path = "doc/永久档案（爱德华·斯诺登）.pdf"

bookmarks_dict = {}

with open(input_pdf_path, "rb") as input_file:
    reader = PdfReader(input_file)
    with open("bookmarks.txt", "w") as bookmarks:
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content = page.extract_text()

            extract_and_write_bookmark(content, page_num, "EDWARD Contents 目 录", "目录", bookmarks, bookmarks_dict)
            extract_and_write_bookmark(content, page_num, "            前 言", "前言", bookmarks, bookmarks_dict)
            extract_and_write_bookmark(content, page_num, "           致 谢 ", "致谢", bookmarks, bookmarks_dict)

            if page_num > 10:
                chapter_pattern = r"Part(?:One|Two|Three)\s+第[一二三四五六七八九十]+部"
                extract_and_write_chapter(content, page_num, chapter_pattern, "章节", bookmarks, bookmarks_dict)

            subchapter_pattern = r"\s{15,}第[一二三四五六七八九十百千]+章\s+[\u4e00-\u9fff]+"
            extract_and_write_subchapter(content, page_num, subchapter_pattern, bookmarks, bookmarks_dict)

    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    print("开始添加书签")
    for key, value in bookmarks_dict.items():
        parent_outline_item = writer.add_outline_item(key, value["page"])
        if "children" in value:
            for child in value["children"]:
                for k, v in child.items():
                    writer.add_outline_item(k, v["page"], parent=parent_outline_item)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
print(f"书签已成功添加到 {output_pdf_path}")