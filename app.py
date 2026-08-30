import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from pathlib import Path


# =========================
# COLORS
# =========================

WE_PURPLE = "#5C2D91"
WE_PURPLE_LIGHT = "#7B4BC0"
WE_ORANGE = "#F59E0B"
BG = "#F7F5FB"
WHITE = "#FFFFFF"
BLACK = "#222222"
GRAY = "#666666"


# =========================
# LOAD DATA
# =========================

PLANS_FILE = Path(__file__).parent / "plans.json"


def load_plans():
    if not PLANS_FILE.exists():
        return []

    with open(PLANS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):
        plans = data.get("plans", [])
    else:
        plans = data

    for plan in plans:
        plan.setdefault("name_en", "WE Plan")
        plan.setdefault("price", 0)
        plan.setdefault("data_gb", 0)
        plan.setdefault("minutes", 0)
        plan.setdefault("sms", 0)
        plan.setdefault("best_for_en", "")

    plans.sort(key=lambda p: p["price"])

    return plans


plans = load_plans()


# =========================
# LOGIC
# =========================

def find_best_plan(gb, minutes, sms):
    suitable = []

    for plan in plans:
        if (
            plan["data_gb"] >= gb
            and plan["minutes"] >= minutes
            and plan["sms"] >= sms
        ):
            suitable.append(plan)

    if not suitable:
        return None

    return min(suitable, key=lambda p: p["price"])


def calculate_match(plan, gb, minutes, sms):
    if not plan:
        return 0

    data_score = min(gb / max(plan["data_gb"], 1), 1)
    minute_score = min(minutes / max(plan["minutes"], 1), 1)

    if sms > 0:
        sms_score = min(sms / max(plan["sms"], 1), 1)
    else:
        sms_score = 1

    result = (
        data_score * 0.45
        + minute_score * 0.40
        + sms_score * 0.15
    )

    return round(result * 100)


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("WE Plan Calculator")
root.geometry("1250x760")
root.configure(bg=BG)

root.minsize(1050, 650)


# =========================
# STYLE
# =========================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TNotebook",
    background=BG,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background="#EEE8F5",
    foreground=WE_PURPLE,
    padding=[22, 12],
    font=("Segoe UI", 11, "bold")
)

style.map(
    "TNotebook.Tab",
    background=[
        ("selected", WE_PURPLE)
    ],
    foreground=[
        ("selected", WHITE)
    ]
)

style.configure(
    "Treeview",
    background=WHITE,
    foreground=BLACK,
    fieldbackground=WHITE,
    rowheight=30,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=WE_PURPLE,
    foreground=WHITE,
    font=("Segoe UI", 10, "bold")
)


# =========================
# HEADER
# =========================

header = tk.Frame(
    root,
    bg=WHITE,
    height=90,
    highlightbackground="#E6DDF0",
    highlightthickness=1
)

header.pack(
    fill="x",
    padx=25,
    pady=(20, 10)
)

header.pack_propagate(False)


logo = tk.Label(
    header,
    text="WE",
    bg=WE_PURPLE,
    fg=WHITE,
    font=("Segoe UI", 18, "bold"),
    width=4,
    height=2
)

logo.pack(
    side="left",
    padx=(20, 15),
    pady=15
)


title_frame = tk.Frame(
    header,
    bg=WHITE
)

title_frame.pack(
    side="left",
    pady=15
)


tk.Label(
    title_frame,
    text="WE Plan Calculator",
    bg=WHITE,
    fg=WE_PURPLE,
    font=("Segoe UI", 22, "bold")
).pack(anchor="w")


tk.Label(
    title_frame,
    text="Smart plan recommendation & cost optimization",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 10)
).pack(anchor="w")


tk.Label(
    header,
    text="Smart Recommendation Engine",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 10)
).pack(
    side="right",
    padx=25
)


# =========================
# NOTEBOOK
# =========================

notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


plan_tab = tk.Frame(
    notebook,
    bg=BG
)

bill_tab = tk.Frame(
    notebook,
    bg=BG
)

chat_tab = tk.Frame(
    notebook,
    bg=BG
)


notebook.add(
    plan_tab,
    text="📊 Plan Calculator"
)

notebook.add(
    bill_tab,
    text="📄 Bill Analysis"
)

notebook.add(
    chat_tab,
    text="🤖 Smart Assistant"
)


# =====================================================
# PLAN CALCULATOR
# =====================================================

left_panel = tk.Frame(
    plan_tab,
    bg=WHITE,
    highlightbackground="#E6DDF0",
    highlightthickness=1
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(10, 5),
    pady=15
)


right_panel = tk.Frame(
    plan_tab,
    bg="#F4ECFB",
    highlightbackground="#D6C4EA",
    highlightthickness=1,
    width=380
)

right_panel.pack(
    side="right",
    fill="y",
    padx=(5, 10),
    pady=15
)

right_panel.pack_propagate(False)


tk.Label(
    left_panel,
    text="Tell us your usage",
    bg=WHITE,
    fg=BLACK,
    font=("Segoe UI", 18, "bold")
).pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


tk.Label(
    left_panel,
    text="Adjust your monthly usage and we will recommend the best plan.",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    padx=25,
    pady=(0, 20)
)


# DATA

gb_var = tk.IntVar(value=45)

tk.Label(
    left_panel,
    text="🌐 Internet Usage (GB)",
    bg=WHITE,
    fg=WE_PURPLE,
    font=("Segoe UI", 11, "bold")
).pack(
    anchor="w",
    padx=25
)


gb_scale = tk.Scale(
    left_panel,
    from_=0,
    to=200,
    orient="horizontal",
    variable=gb_var,
    bg=WHITE,
    fg=WE_PURPLE,
    highlightthickness=0,
    troughcolor="#DDD3E8",
    activebackground=WE_PURPLE,
    length=600
)

gb_scale.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


# MINUTES

minutes_var = tk.IntVar(value=600)

tk.Label(
    left_panel,
    text="📞 Call Minutes",
    bg=WHITE,
    fg=WE_PURPLE,
    font=("Segoe UI", 11, "bold")
).pack(
    anchor="w",
    padx=25
)


minutes_scale = tk.Scale(
    left_panel,
    from_=0,
    to=6000,
    resolution=50,
    orient="horizontal",
    variable=minutes_var,
    bg=WHITE,
    fg=WE_PURPLE,
    highlightthickness=0,
    troughcolor="#DDD3E8",
    activebackground=WE_PURPLE
)

minutes_scale.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


# SMS

sms_var = tk.IntVar(value=100)

tk.Label(
    left_panel,
    text="💬 SMS",
    bg=WHITE,
    fg=WE_PURPLE,
    font=("Segoe UI", 11, "bold")
).pack(
    anchor="w",
    padx=25
)


sms_scale = tk.Scale(
    left_panel,
    from_=0,
    to=2000,
    resolution=25,
    orient="horizontal",
    variable=sms_var,
    bg=WHITE,
    fg=WE_PURPLE,
    highlightthickness=0,
    troughcolor="#DDD3E8",
    activebackground=WE_PURPLE
)

sms_scale.pack(
    fill="x",
    padx=25,
    pady=(0, 20)
)


# =========================
# BEST PLAN CARD
# =========================

tk.Label(
    right_panel,
    text="✦ BEST MATCH",
    bg=WE_PURPLE,
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    padx=12,
    pady=6
).pack(
    anchor="w",
    padx=25,
    pady=(30, 20)
)


recommended_name = tk.Label(
    right_panel,
    text="Select your usage",
    bg="#F4ECFB",
    fg=WE_PURPLE,
    font=("Segoe UI", 22, "bold")
)

recommended_name.pack(
    anchor="w",
    padx=25
)


recommended_price = tk.Label(
    right_panel,
    text="",
    bg="#F4ECFB",
    fg=WE_PURPLE,
    font=("Segoe UI", 28, "bold")
)

recommended_price.pack(
    anchor="w",
    padx=25,
    pady=(15, 10)
)


recommended_details = tk.Label(
    right_panel,
    text="",
    bg="#F4ECFB",
    fg=BLACK,
    font=("Segoe UI", 11),
    justify="left"
)

recommended_details.pack(
    anchor="w",
    padx=25,
    pady=10
)


recommended_reason = tk.Label(
    right_panel,
    text="",
    bg="#F4ECFB",
    fg=GRAY,
    font=("Segoe UI", 10),
    justify="left",
    wraplength=320
)

recommended_reason.pack(
    anchor="w",
    padx=25,
    pady=15
)


def update_plan():
    gb = gb_var.get()
    minutes = minutes_var.get()
    sms = sms_var.get()

    plan = find_best_plan(
        gb,
        minutes,
        sms
    )

    if plan:
        recommended_name.config(
            text=plan["name_en"]
        )

        recommended_price.config(
            text=f'{plan["price"]} EGP'
        )

        match = calculate_match(
            plan,
            gb,
            minutes,
            sms
        )

        recommended_details.config(
            text=
            f'🌐 {plan["data_gb"]} GB\n\n'
            f'📞 {plan["minutes"]} Minutes\n\n'
            f'💬 {plan["sms"]} SMS\n\n'
            f'🎯 Match: {match}%'
        )

        reason = plan.get(
            "best_for_en",
            ""
        )

        if not reason:
            reason = "This plan covers your expected monthly usage."

        recommended_reason.config(
            text=f"Why this plan?\n{reason}"
        )

    else:
        recommended_name.config(
            text="No matching plan"
        )

        recommended_price.config(
            text=""
        )

        recommended_details.config(
            text=""
        )

        recommended_reason.config(
            text="Your usage is higher than the available plans."
        )


tk.Button(
    left_panel,
    text="Find My Best Plan",
    bg=WE_PURPLE,
    fg=WHITE,
    activebackground=WE_PURPLE_LIGHT,
    activeforeground=WHITE,
    borderwidth=0,
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=12,
    command=update_plan
).pack(
    fill="x",
    padx=25,
    pady=15
)


# =====================================================
# ALL PLANS TABLE
# =====================================================

table_frame = tk.Frame(
    left_panel,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(5, 20)
)


columns = (
    "Plan",
    "Price",
    "Data",
    "Minutes",
    "SMS"
)


plan_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=7
)


for column in columns:
    plan_table.heading(
        column,
        text=column
    )

    plan_table.column(
        column,
        width=120,
        anchor="center"
    )


plan_table.pack(
    fill="both",
    expand=True
)


for plan in plans:
    plan_table.insert(
        "",
        "end",
        values=(
            plan["name_en"],
            f'{plan["price"]} EGP',
            f'{plan["data_gb"]} GB',
            plan["minutes"],
            plan["sms"]
        )
    )


# =====================================================
# BILL ANALYSIS
# =====================================================

bill_card = tk.Frame(
    bill_tab,
    bg=WHITE,
    highlightbackground="#E6DDF0",
    highlightthickness=1
)

bill_card.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=20
)


tk.Label(
    bill_card,
    text="Bill Cost Optimizer",
    bg=WHITE,
    fg=BLACK,
    font=("Segoe UI", 20, "bold")
).pack(
    anchor="w",
    padx=30,
    pady=(30, 5)
)


tk.Label(
    bill_card,
    text="Enter your current spending and usage to identify a better alternative.",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    padx=30,
    pady=(0, 25)
)


inputs = tk.Frame(
    bill_card,
    bg=WHITE
)

inputs.pack(
    fill="x",
    padx=30
)


bill_var = tk.StringVar(value="250")
bill_gb_var = tk.StringVar(value="13")
bill_minutes_var = tk.StringVar(value="900")
bill_sms_var = tk.StringVar(value="30")


def create_input(parent, text, variable):
    frame = tk.Frame(
        parent,
        bg=WHITE
    )

    frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    tk.Label(
        frame,
        text=text,
        bg=WHITE,
        fg=BLACK,
        font=("Segoe UI", 10, "bold")
    ).pack(
        anchor="w"
    )

    entry = tk.Entry(
        frame,
        textvariable=variable,
        bg="#201C25",
        fg=WHITE,
        insertbackground=WHITE,
        font=("Segoe UI", 12, "bold"),
        relief="flat"
    )

    entry.pack(
        fill="x",
        ipady=12,
        pady=5
    )


create_input(
    inputs,
    "Current Bill (EGP)",
    bill_var
)

create_input(
    inputs,
    "Data Used (GB)",
    bill_gb_var
)

create_input(
    inputs,
    "Minutes Used",
    bill_minutes_var
)

create_input(
    inputs,
    "SMS Used",
    bill_sms_var
)


bill_result = tk.Label(
    bill_card,
    text="",
    bg=WHITE,
    fg=BLACK,
    font=("Segoe UI", 12),
    justify="left"
)

bill_result.pack(
    anchor="w",
    padx=30,
    pady=25
)


def analyze_bill():
    try:
        current_bill = float(
            bill_var.get()
        )

        used_gb = float(
            bill_gb_var.get()
        )

        used_minutes = int(
            bill_minutes_var.get()
        )

        used_sms = int(
            bill_sms_var.get()
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers."
        )

        return

    fits = []

    for plan in plans:
        if (
            plan["data_gb"] >= used_gb
            and plan["minutes"] >= used_minutes
            and plan["sms"] >= used_sms
        ):
            fits.append(plan)

    if not fits:
        bill_result.config(
            text="No available plan fully covers your current usage."
        )

        return

    eligible = [
        plan for plan in fits
        if plan["price"] <= current_bill
    ]

    if eligible:
        best = max(
            eligible,
            key=lambda plan: (
                plan["data_gb"] * 2
                + plan["minutes"] / 50
                + plan["sms"] / 100
            )
        )
    else:
        best = min(
            fits,
            key=lambda plan: plan["price"]
        )

    difference = current_bill - best["price"]

    result = (
        f'Recommended Plan: {best["name_en"]}\n\n'
        f'Recommended Cost: {best["price"]} EGP\n\n'
        f'Data: {used_gb:g} GB used → {best["data_gb"]} GB included\n'
        f'Calls: {used_minutes} used → {best["minutes"]} included\n'
        f'SMS: {used_sms} used → {best["sms"]} included\n\n'
    )

    if difference > 0:
        result += (
            f'Estimated Saving: {difference:g} EGP/month\n'
            f'Annual Saving: {difference * 12:g} EGP'
        )

    elif difference < 0:
        result += (
            f'This plan costs {abs(difference):g} EGP more '
            f'than your current bill.'
        )

    else:
        result += (
            "The recommended plan has the same monthly cost."
        )

    bill_result.config(
        text=result
    )


tk.Button(
    bill_card,
    text="⚡ Analyze My Bill",
    bg=WE_PURPLE,
    fg=WHITE,
    activebackground=WE_PURPLE_LIGHT,
    activeforeground=WHITE,
    borderwidth=0,
    font=("Segoe UI", 11, "bold"),
    pady=13,
    command=analyze_bill
).pack(
    fill="x",
    padx=30,
    pady=20
)


# =====================================================
# SMART ASSISTANT
# =====================================================

chat_card = tk.Frame(
    chat_tab,
    bg=WHITE,
    highlightbackground="#E6DDF0",
    highlightthickness=1
)

chat_card.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=20
)


tk.Label(
    chat_card,
    text="🤖 WE Smart Assistant",
    bg=WHITE,
    fg=WE_PURPLE,
    font=("Segoe UI", 20, "bold")
).pack(
    anchor="w",
    padx=25,
    pady=(25, 5)
)


tk.Label(
    chat_card,
    text="Ask about plans, usage, prices, comparisons or budget.",
    bg=WHITE,
    fg=GRAY,
    font=("Segoe UI", 10)
).pack(
    anchor="w",
    padx=25,
    pady=(0, 15)
)


chat_box = tk.Text(
    chat_card,
    bg="#FAF8FC",
    fg=BLACK,
    font=("Segoe UI", 11),
    wrap="word",
    relief="flat"
)

chat_box.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


chat_box.insert(
    "end",
    "WE Assistant: Hi 👋 I'm WE Smart Assistant.\n"
    "Ask me about plans, prices, usage or your budget.\n\n"
)


chat_entry = tk.Entry(
    chat_card,
    bg=WHITE,
    fg=WE_PURPLE,
    insertbackground=WE_PURPLE,
    font=("Segoe UI", 11),
    relief="solid",
    bd=1
)

chat_entry.pack(
    fill="x",
    padx=25,
    ipady=12,
    pady=(5, 10)
)


def chatbot_answer(text):
    message = text.lower()

    if not plans:
        return "No plan data is currently available."

    if "cheapest" in message:
        plan = min(
            plans,
            key=lambda p: p["price"]
        )

        return (
            f'The cheapest plan is {plan["name_en"]} '
            f'at {plan["price"]} EGP/month. '
            f'It includes {plan["data_gb"]} GB, '
            f'{plan["minutes"]} minutes and '
            f'{plan["sms"]} SMS.'
        )

    if "compare" in message:
        first = sorted(
            plans,
            key=lambda p: p["price"]
        )[:3]

        result = "Here are three options:\n"

        for plan in first:
            result += (
                f'\n• {plan["name_en"]}: '
                f'{plan["price"]} EGP, '
                f'{plan["data_gb"]} GB, '
                f'{plan["minutes"]} minutes'
            )

        return result

    if "budget" in message or "under" in message:
        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            message
        )

        if not numbers:
            return "Tell me your budget, for example: My budget is 250 EGP."

        budget = float(
            numbers[0]
        )

        affordable = [
            p for p in plans
            if p["price"] <= budget
        ]

        if not affordable:
            return "I could not find a plan within this budget."

        plan = max(
            affordable,
            key=lambda p: (
                p["data_gb"]
                + p["minutes"] / 100
            )
        )

        return (
            f'For a budget of {budget:g} EGP, '
            f'I recommend {plan["name_en"]} at '
            f'{plan["price"]} EGP/month.'
        )

    if "gb" in message or "minute" in message:
        gb_match = re.search(
            r"(\d+(?:\.\d+)?)\s*gb",
            message
        )

        minute_match = re.search(
            r"(\d+)\s*(?:min|mins|minute|minutes)",
            message
        )

        gb = (
            float(gb_match.group(1))
            if gb_match else 0
        )

        minutes = (
            int(minute_match.group(1))
            if minute_match else 0
        )

        matches = [
            plan for plan in plans
            if plan["data_gb"] >= gb
            and plan["minutes"] >= minutes
        ]

        if not matches:
            return "I couldn't find a plan that fully covers this usage."

        plan = min(
            matches,
            key=lambda p: p["price"]
        )

        return (
            f'I recommend {plan["name_en"]}. '
            f'It costs {plan["price"]} EGP/month '
            f'and includes {plan["data_gb"]} GB '
            f'and {plan["minutes"]} minutes.'
        )

    if (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):
        return (
            "Hi 👋 I can recommend plans, compare prices, "
            "work with your budget and analyze your usage."
        )

    return (
        "I can help with WE plans. "
        "Try asking: 'What is the cheapest plan?', "
        "'My budget is 300 EGP', "
        "or 'I need 30 GB and 600 minutes'."
    )


def send_message(event=None):
    message = chat_entry.get().strip()

    if not message:
        return

    chat_box.insert(
        "end",
        f"You: {message}\n"
    )

    answer = chatbot_answer(
        message
    )

    chat_box.insert(
        "end",
        f"WE Assistant: {answer}\n\n"
    )

    chat_box.see("end")

    chat_entry.delete(
        0,
        "end"
    )


tk.Button(
    chat_card,
    text="Send",
    bg=WE_PURPLE,
    fg=WHITE,
    activebackground=WE_PURPLE_LIGHT,
    activeforeground=WHITE,
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    command=send_message
).pack(
    padx=25,
    pady=(0, 20),
    anchor="e"
)


chat_entry.bind(
    "<Return>",
    send_message
)


# =========================
# START
# =========================

update_plan()

root.mainloop()
