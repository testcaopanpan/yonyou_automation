import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
import pdfplumber
from diff_match_patch import diff_match_patch
import os
from pdf2docx import Converter
import openpyxl
from openpyxl import Workbook
import pandas as pd

class PDFTool:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Processing Tool")
        self.root.geometry("800x600")

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Tab 1: PDF Comparison
        self.compare_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compare_frame, text='PDF 对比')
        self.setup_compare_tab()

        # Tab 2: PDF Editing
        self.edit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.edit_frame, text='PDF 修改')
        self.setup_edit_tab()

        # Tab 3: PDF Conversion
        self.convert_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.convert_frame, text='PDF 转化')
        self.setup_convert_tab()

    def setup_compare_tab(self):
        # File selection
        ttk.Label(self.compare_frame, text="选择第一个PDF:").grid(row=0, column=0, padx=10, pady=10)
        self.pdf1_path = tk.StringVar()
        ttk.Entry(self.compare_frame, textvariable=self.pdf1_path, width=50).grid(row=0, column=1)
        ttk.Button(self.compare_frame, text="浏览", command=lambda: self.select_file(self.pdf1_path)).grid(row=0, column=2)

        ttk.Label(self.compare_frame, text="选择第二个PDF:").grid(row=1, column=0, padx=10, pady=10)
        self.pdf2_path = tk.StringVar()
        ttk.Entry(self.compare_frame, textvariable=self.pdf2_path, width=50).grid(row=1, column=1)
        ttk.Button(self.compare_frame, text="浏览", command=lambda: self.select_file(self.pdf2_path)).grid(row=1, column=2)

        # Compare button
        ttk.Button(self.compare_frame, text="对比", command=self.compare_pdfs).grid(row=2, column=1, pady=20)

        # Result display
        self.compare_result = tk.Text(self.compare_frame, height=20, width=80)
        self.compare_result.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def setup_edit_tab(self):
        # File selection
        ttk.Label(self.edit_frame, text="选择PDF文件:").grid(row=0, column=0, padx=10, pady=10)
        self.edit_pdf_path = tk.StringVar()
        ttk.Entry(self.edit_frame, textvariable=self.edit_pdf_path, width=50).grid(row=0, column=1)
        ttk.Button(self.edit_frame, text="浏览", command=lambda: self.select_file(self.edit_pdf_path)).grid(row=0, column=2)

        # Text selection and replacement
        ttk.Label(self.edit_frame, text="原内容:").grid(row=1, column=0, padx=10, pady=10)
        self.original_text = tk.Text(self.edit_frame, height=5, width=50)
        self.original_text.grid(row=1, column=1, columnspan=2)

        ttk.Label(self.edit_frame, text="替换内容:").grid(row=2, column=0, padx=10, pady=10)
        self.replacement_text = tk.Text(self.edit_frame, height=5, width=50)
        self.replacement_text.grid(row=2, column=1, columnspan=2)

        # Replace button
        ttk.Button(self.edit_frame, text="替换", command=self.replace_text).grid(row=3, column=1, pady=10)

        # Export button
        ttk.Button(self.edit_frame, text="导出", command=self.export_pdf).grid(row=4, column=1, pady=10)

    def setup_convert_tab(self):
        # File selection
        ttk.Label(self.convert_frame, text="选择PDF文件:").grid(row=0, column=0, padx=10, pady=10)
        self.convert_pdf_path = tk.StringVar()
        ttk.Entry(self.convert_frame, textvariable=self.convert_pdf_path, width=50).grid(row=0, column=1)
        ttk.Button(self.convert_frame, text="浏览", command=lambda: self.select_file(self.convert_pdf_path)).grid(row=0, column=2)

        # Format selection
        ttk.Label(self.convert_frame, text="选择格式:").grid(row=1, column=0, padx=10, pady=10)
        self.format_var = tk.StringVar()
        formats = ['Excel', 'Word', 'OFD']
        self.format_combo = ttk.Combobox(self.convert_frame, textvariable=self.format_var, values=formats)
        self.format_combo.grid(row=1, column=1)
        self.format_combo.current(0)

        # Convert button
        ttk.Button(self.convert_frame, text="转化", command=self.convert_pdf).grid(row=2, column=1, pady=20)

    def select_file(self, path_var):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            path_var.set(filename)

    def compare_pdfs(self):
        pdf1 = self.pdf1_path.get()
        pdf2 = self.pdf2_path.get()
        if not pdf1 or not pdf2:
            messagebox.showerror("错误", "请选择两个PDF文件")
            return

        try:
            text1 = self.extract_text(pdf1)
            text2 = self.extract_text(pdf2)

            dmp = diff_match_patch()
            diffs = dmp.diff_main(text1, text2)
            dmp.diff_cleanupSemantic(diffs)

            result = ""
            for op, data in diffs:
                if op == -1:
                    result += f"删除: {data}\n"
                elif op == 1:
                    result += f"添加: {data}\n"
                else:
                    result += f"相同: {data}\n"

            self.compare_result.delete(1.0, tk.END)
            self.compare_result.insert(tk.END, result)

            if any(op != 0 for op, _ in diffs):
                messagebox.showinfo("结果", "PDF文件不一致")
            else:
                messagebox.showinfo("结果", "PDF文件一致")

        except Exception as e:
            messagebox.showerror("错误", f"对比失败: {str(e)}")

    def extract_text(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def replace_text(self):
        # This is a simplified version. Full text replacement in PDF is complex.
        # For demonstration, we'll just show a message.
        messagebox.showinfo("替换", "文本替换功能需要更复杂的实现。")

    def export_pdf(self):
        # Placeholder
        messagebox.showinfo("导出", "导出功能待实现。")

    def convert_pdf(self):
        pdf_path = self.convert_pdf_path.get()
        format_type = self.format_var.get()
        if not pdf_path:
            messagebox.showerror("错误", "请选择PDF文件")
            return

        try:
            if format_type == 'Word':
                self.convert_to_word(pdf_path)
            elif format_type == 'Excel':
                self.convert_to_excel(pdf_path)
            elif format_type == 'OFD':
                self.convert_to_ofd(pdf_path)
            messagebox.showinfo("成功", f"已转换为{format_type}")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")

    def convert_to_word(self, pdf_path):
        docx_file = pdf_path.replace('.pdf', '.docx')
        cv = Converter(pdf_path)
        cv.convert(docx_file, start=0, end=None)
        cv.close()

    def convert_to_excel(self, pdf_path):
        # Extract tables using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            wb = Workbook()
            ws = wb.active
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        ws.append(row)
            excel_file = pdf_path.replace('.pdf', '.xlsx')
            wb.save(excel_file)

    def convert_to_ofd(self, pdf_path):
        # Placeholder for OFD conversion
        messagebox.showinfo("OFD", "OFD转换功能待实现。")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFTool(root)
    root.mainloop()</content>
<parameter name="filePath">d:\python_workspace\yonyou_automation\pdf_tool.py