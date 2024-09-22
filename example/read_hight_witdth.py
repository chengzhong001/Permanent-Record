
import pypdf

# 打开 PDF 文件
with open('/Users/chengzhong/Downloads/永久档案.pdf', 'rb') as file:
    pdf_reader = pypdf.PdfReader(file)

    # 获取第一页的页面尺寸
    page = pdf_reader.pages[0]
    media_box = page.mediabox
    width = media_box.width
    height = media_box.height

    print(f"PDF 页面尺寸: 宽度 {width} 点，高度 {height} 点")