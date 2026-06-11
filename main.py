import re
import csv
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
# -------------------------------------------------
# Load Corpus Files
# -------------------------------------------------
lexicon = {}
with open("lexicon.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        lexicon[row["word"].lower()] = row["pos"]
with open("morph_rules.json", "r") as file:
    morph_rules = json.load(file)
with open("context_rules.json", "r") as file:
    context_rules = json.load(file)
# -------------------------------------------------
# NLP Functions
# -------------------------------------------------
def tokenize(text):
    return re.findall(r"\b\w+\b", text)
def initial_tagging(tokens):
    return [(word, lexicon.get(word.lower(), "UNK")) for word in tokens]
def apply_morphological_rules(tagged_tokens):
    updated = []
    for word, tag in tagged_tokens:
        if tag == "UNK":
            for suffix, new_tag in morph_rules.items():
                if word.lower().endswith(suffix):
                    tag = new_tag
                    break
        updated.append((word, tag))
    return updated
def apply_proper_noun_rule(tagged_tokens):
    updated = []
    for word, tag in tagged_tokens:
        if tag == "UNK" and word[0].isupper():
            updated.append((word, "NNP"))
        else:
            updated.append((word, tag))
    return updated
def apply_contextual_rules(tagged_tokens):
    updated = tagged_tokens.copy()
    for i, (word, tag) in enumerate(tagged_tokens):
        if tag != "UNK":
            continue
        for rule in context_rules:
            if "prev_tag" in rule and i > 0:
                if tagged_tokens[i - 1][1] == rule["prev_tag"]:
                    updated[i] = (word, rule["assign"])
                    break
            if "next_tag" in rule and i < len(tagged_tokens) - 1:
                if tagged_tokens[i + 1][1] == rule["next_tag"]:
                    updated[i] = (word, rule["assign"])
                    break
    return updated
def pos_tagger(sentence):
    tokens = tokenize(sentence)
    tagged = initial_tagging(tokens)
    tagged = apply_morphological_rules(tagged)
    tagged = apply_proper_noun_rule(tagged)
    tagged = apply_contextual_rules(tagged)
    return tagged
# -------------------------------------------------
# UI Logic
# -------------------------------------------------
def tag_sentence():
    sentence = input_text.get("1.0", tk.END).strip()
    if not sentence:
        messagebox.showwarning("Input Error", "Please enter a sentence")
        return
    result = pos_tagger(sentence)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"{'WORD':<20}{'POS TAG'}\n")
    output_text.insert(tk.END, "-" * 35 + "\n")
    for word, tag in result:
        output_text.insert(tk.END, f"{word:<20}{tag}\n")
def clear_output():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
# -------------------------------------------------
# Modern Tkinter UI
# -------------------------------------------------
root = tk.Tk()
root.title("Rule-Based POS Tagger")
root.state("zoomed")
root.configure(bg="#eef2f7")
# ---------------- Header ----------------
header = tk.Frame(root, bg="#3f51b5", height=100)
header.pack(side="top", fill="x")
tk.Label(
    header,
    text="Rule-Based Part of Speech Tagging System",
    font=("Segoe UI", 22, "bold"),
    bg="#3f51b5",
    fg="white"
).pack(pady=(15, 0))
tk.Label(
    header,
    text="An Academic Implementation of Rule-Based NLP Techniques",
    font=("Segoe UI", 11),
    bg="#3f51b5",
    fg="#e0e0e0"
).pack(pady=(5, 10))
# ---------------- Main Container ----------------
container = tk.Frame(root, bg="#eef2f7")
container.pack(side="top", padx=50, pady=10, fill="both", expand=True)
# ---------------- Input Card ----------------
input_card = tk.Frame(container, bg="white")
input_card.pack(fill="x", pady=10)
tk.Label(
    input_card,
    text="Input Sentence",
    font=("Segoe UI", 14, "bold"),
    bg="white",
    fg="#2c3e50"
).pack(anchor="w", padx=15, pady=10)
input_text = scrolledtext.ScrolledText(
    input_card,
    height=4,
    font=("Segoe UI", 12),
    wrap=tk.WORD,
    bd=1,
    relief="solid"
)
input_text.pack(padx=15, pady=10, fill="x")
# ---------------- Buttons ----------------
btn_frame = tk.Frame(container, bg="#eef2f7")
btn_frame.pack(pady=15)
tk.Button(
    btn_frame,
    text="Tag Sentence",
    font=("Segoe UI", 12, "bold"),
    bg="#3f51b5",
    fg="white",
    activebackground="#303f9f",
    padx=30,
    pady=10,
    bd=0,
    cursor="hand2",
    command=tag_sentence
).pack(side="left", padx=10)
tk.Button(
    btn_frame,
    text="Clear",
    font=("Segoe UI", 12),
    bg="#e0e0e0",
    fg="#2c3e50",
    padx=25,
    pady=10,
    bd=0,
    cursor="hand2",
    command=clear_output
).pack(side="left", padx=10)
# ---------------- Output Card ----------------
output_card = tk.Frame(container, bg="white")
output_card.pack(fill="both", expand=True, pady=10)
tk.Label(
    output_card,
    text="POS Tagging Output",
    font=("Segoe UI", 14, "bold"),
    bg="white",
    fg="#2c3e50"
).pack(anchor="w", padx=15, pady=10)
output_text = scrolledtext.ScrolledText(
    output_card,
    font=("Consolas", 11),
    wrap=tk.WORD,
    bd=1,
    relief="solid",
    height=15  # fixed height so footer remains visible
)
output_text.pack(padx=15, pady=10, fill="x", expand=False)
# ---------------- Footer ----------------
footer = tk.Frame(root, bg="#3f51b5", height=40)
footer.pack(side="bottom", fill="x")
tk.Label(
    footer,
    text="Manasa | Rule Based POS Tagger | B.Tech CSE",
    font=("Segoe UI", 10),
    bg="#3f51b5",
    fg="white"
).pack(pady=8)
root.mainloop()
