import re
import subprocess
import customtkinter as ctk

PIP_SOURCES = {
    "官方 PyPI": "https://pypi.org/simple/",
    "阿里云": "https://mirrors.aliyun.com/pypi/simple/",
    "豆瓣": "https://pypi.douban.com/simple/",
    "清华大学": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "中国科技大学": "https://mirrors.ustc.edu.cn/pypi/web/simple/",
    "华为云": "https://repo.huaweicloud.com/repository/pypi/simple",
}


def get_source_name(source_url):
    for source_name, url in PIP_SOURCES.items():
        if source_url.lower().strip("/") == url.lower().strip("/"):
            return source_name
    return source_url


def get_current_pip_source():
    output = subprocess.run(
        ["pip", "config", "list"], capture_output=True, text=True
    ).stdout

    pattern = r"index-url\s*=\s*(.*)$"
    match = re.findall(pattern, output, flags=re.M)

    if match:
        return match[0].strip().strip("'").strip('"')
    else:
        return None


def set_pip_source(source_name):
    source_url = PIP_SOURCES.get(source_name)
    if not source_url:
        result_label.configure(text="无效的选项！", text_color="red")
        return

    try:
        process = subprocess.Popen(
            ["pip", "config", "set", "global.index-url", source_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = process.communicate()
        if process.returncode == 0:
            result_label.configure(text=f"PIP 源已设置为：{source_name}", text_color="green")
        else:
            result_label.configure(text=f"设置PIP源时出现错误：{error.decode()}", text_color="red")
    except Exception as e:
        result_label.configure(text=f"设置PIP源时出现错误：{str(e)}", text_color="red")


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - 100
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
window = ctk.CTk()
window.title("PIP 源切换工具")
window.geometry("480x310")
window.resizable(False, False)
window.withdraw()

main_frame = ctk.CTkFrame(window, corner_radius=10)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

for i, source_name in enumerate(PIP_SOURCES.keys()):
    row = i // 2
    col = i % 2
    button = ctk.CTkButton(
        main_frame,
        text=source_name,
        width=200,
        height=50,
        command=lambda source_name=source_name: set_pip_source(source_name),
        fg_color="#2196f3",
        hover_color="#1e88e5",
        text_color="white",
        corner_radius=8,
    )
    button.grid(row=row, column=col, padx=10, pady=10)

current_pip_source = get_current_pip_source()
if current_pip_source:
    current_source_name = get_source_name(current_pip_source)
else:
    current_source_name = "未知pip源"
result_label = ctk.CTkLabel(
    main_frame,
    text=f"当前源：{current_source_name}",
    text_color="green",
)
result_label.grid(row=len(PIP_SOURCES) // 2 + 1, columnspan=2, padx=10, pady=10)

center_window(window)
window.update()
window.deiconify()
window.mainloop()
