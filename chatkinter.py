import tkinter as tk
from tkinter import Text
import arabic_reshaper
from bidi.algorithm import get_display
import difflib
from tkinter import font

# دیتابیس سؤالات و پاسخ‌ها
knowledge_base = {
    "ارزش غذایی زیتون": "زیتون حاوی چربی‌های سالم، ویتامین E، آهن و آنتی‌اکسیدان‌ها است.",
    "کالری زیتون": "هر 100 گرم زیتون بین 115 تا 145 کالری دارد.",
    "چربی زیتون": "زیتون 10 تا 15 درصد چربی دارد که بیشتر آن اسیداولئیک است.",
    "پروتئین زیتون": "میزان پروتئین زیتون کمتر از 1 درصد است.",
    "فیبر زیتون": "زیتون حدود 4 درصد فیبر دارد که به گوارش کمک می‌کند.",
    "پتاسیم زیتون": "زیتون دارای پتاسیم است که برای سلامت قلب مفید می‌باشد.",
    "آهن زیتون": "زیتون حاوی آهن است که برای تولید هموگلوبین ضروری است.",
    "ویتامین‌های زیتون": "زیتون دارای ویتامین‌های A، E و K است که به سلامت پوست، بینایی و انعقاد خون کمک می‌کنند.",
    "آنتی‌اکسیدان‌های زیتون": "زیتون حاوی آنتی‌اکسیدان‌هایی مانند اولئوروپین است که به کاهش التهاب و محافظت از سلول‌ها کمک می‌کند.",
    "خواص ضدالتهابی زیتون": "زیتون می‌تواند به کاهش التهاب و محافظت در برابر بیماری‌های مزمن کمک کند.",
    "زیتون و سلامت قلب": "چربی‌های غیراشباع زیتون می‌توانند به کاهش کلسترول بد (LDL) و افزایش کلسترول خوب (HDL) کمک کنند.",
    "مضرات زیتون": "زیتون‌های فرآوری‌شده معمولاً حاوی نمک زیادی هستند که ممکن است برای افراد با فشار خون بالا مضر باشد.",
    
    "ارزش غذایی خرما": "خرما منبع غنی از کربوهیدرات، فیبر و آنتی‌اکسیدان‌ها است.",
    "کالری خرما": "هر 100 گرم خرما تقریباً 277 کالری دارد.",
    "چربی خرما": "خرما تقریباً بدون چربی است و کمتر از 0.2 درصد چربی دارد.",
    "پروتئین خرما": "هر 100 گرم خرما حدود 2 درصد پروتئین دارد.",
    "فیبر خرما": "خرما دارای 7 گرم فیبر در هر 100 گرم است که برای سلامت روده مفید است.",
    "قند خرما": "خرما حاوی قندهای طبیعی مانند گلوکز و فروکتوز است که انرژی فوری فراهم می‌کنند.",
    "پتاسیم خرما": "خرما دارای پتاسیم بالایی است که به سلامت قلب و کاهش فشار خون کمک می‌کند.",
    "ویتامین‌های خرما": "خرما دارای ویتامین‌های K، B6 و C است که برای سلامت استخوان‌ها و عملکرد سیستم ایمنی مفید هستند.",
    "مواد معدنی خرما": "خرما حاوی مواد معدنی مانند منیزیم، مس و سلنیوم است که برای سلامت عمومی بدن ضروری هستند.",
    "فواید خرما برای دستگاه گوارش": "خرما با داشتن فیبر زیاد به تنظیم عملکرد روده و جلوگیری از یبوست کمک می‌کند.",
    "خرما و انرژی‌زایی": "به دلیل داشتن قندهای طبیعی، خرما منبعی عالی برای تأمین انرژی سریع است.",
    "خرما و سلامت مغز": "خرما دارای ترکیباتی است که ممکن است به بهبود عملکرد مغز و کاهش خطر بیماری‌های عصبی کمک کند.",
    "خرما و سلامت استخوان‌ها": "خرما به دلیل داشتن مواد معدنی مانند منیزیم و کلسیم به تقویت استخوان‌ها کمک می‌کند.",
    "خرما و تقویت سیستم ایمنی": "آنتی‌اکسیدان‌های موجود در خرما به تقویت سیستم ایمنی بدن کمک می‌کنند.",
    "مضرات خرما": "مصرف بیش از حد خرما ممکن است باعث افزایش قند خون شود و برای افراد دیابتی باید با احتیاط مصرف شود.",
    "آهن خرما":"خرما دارای آهن است که به تولید گلبول‌های قرمز کمک می‌کند."
}

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("چت‌بات")
        self.root.geometry("500x600")
        
        # بارگذاری فونت Arial
        self.font = font.Font(family="Arial", size=12)
        
        # نمایش تاریخچه چت
        self.chat_history = Text(root, wrap=tk.WORD, font=self.font, state='disabled', height=20)
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # تنظیم راست‌چین بودن متن
        self.chat_history.tag_configure("right", justify="right")
        
        # ورودی کاربر
        self.user_input = tk.Entry(root, font=self.font, justify='right')
        self.user_input.pack(padx=10, pady=5, fill=tk.X)
        
        # دکمه ارسال
        self.send_button = tk.Button(root, text="ارسال", command=self.send_message, font=self.font)
        self.send_button.pack(pady=5)
        
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # نمایش پیام خوشامدگویی اولیه
        self.display_message("چت‌بات: سلام! در مورد ارزش غذایی خرما و زیتون بپرس.", is_bot=True)

    def find_best_match(self, user_text):
        user_text = user_text.strip()
        matches = difflib.get_close_matches(user_text, knowledge_base.keys(), n=1, cutoff=0.6)
        return knowledge_base.get(matches[0], "متاسفم! اطلاعاتی در این مورد ندارم.") if matches else "متاسفم! اطلاعاتی در این مورد ندارم."
    
    def send_message(self):
        user_text = self.user_input.get().strip()
        if user_text:
            self.display_message(user_text, is_bot=False)
            bot_response = self.find_best_match(user_text)
            self.display_message(bot_response, is_bot=True)
            self.user_input.delete(0, tk.END)

    def display_message(self, text, is_bot):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{bidi_text}\n", "right")  # اعمال راست‌چین بودن
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
