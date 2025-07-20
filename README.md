import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Harsha's Portfolio")
root.geometry("600x600")
root.configure(bg="#f4f4f9")

title = tk.Label(root, text="👋 Hi, I’m Harsha", font=("Arial", 20), bg="#f4f4f9")
title.pack(pady=(10, 5))

subtitle = tk.Label(root, text="AI & Data Engineering | B.Tech", font=("Arial", 12), bg="#f4f4f9")
subtitle.pack()

link = tk.Label(root, text="LinkedIn", font=("Arial", 12), fg="#0077b5", bg="#f4f4f9", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: root.clipboard_append("https://www.linkedin.com/in/harshavardhan-reddy-n-268176285/"))

email = tk.Label(root, text="harshavardhan414212@gmail.com", font=("Arial", 12), bg="#f4f4f9")
email.pack()

projects_label = tk.Label(root, text="🔥 Projects", font=("Arial", 16), fg="#d35400", bg="#f4f4f9")
projects_label.pack(pady=(20, 5))

projects = [
    ("LaughBot", "Witty, learning chatbot"),
    ("Smart Recommender", "ML-powered suggestions"),
    ("DataViz Stories", "Visual, interactive data"),
    ("Generative Playground", "Creative AI experiments")
]

for name, desc in projects:
    proj = tk.Label(root, text=f"{name} – {desc}", font=("Arial", 12), bg="#f4f4f9", anchor="w")
    proj.pack(fill='x', padx=20)

toolbox_label = tk.Label(root, text="🛠️ Toolbox", font=("Arial", 16), fg="#d35400", bg="#f4f4f9")
toolbox_label.pack(pady=(20, 5))

tools1 = tk.Label(root, text="Python · Java · HTML5 · CSS3", font=("Arial", 12), bg="#f4f4f9")
tools1.pack()
tools2 = tk.Label(root, text="Scikit-learn · OpenAI · MySQL · Power BI · Hadoop · Linux · Git", font=("Arial", 12), bg="#f4f4f9")
tools2.pack()

join_label = tk.Label(root, text="🌟 Join In!", font=("Arial", 16), fg="#d35400", bg="#f4f4f9")
join_label.pack(pady=(20, 5))

join_list = ["⭐ Star projects", "💬 Collaborate or suggest", "Let’s make ideas happen!"]
for item in join_list:
    line = tk.Label(root, text=item, font=("Arial", 12), bg="#f4f4f9", anchor="w")
    line.pack(fill='x', padx=20)

root.mainloop()
