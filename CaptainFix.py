from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By

# ---- הגדרת OpenAI ----
Ai_agent = OpenAI(api_key="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")

def analyze_html_with_llm(html):
    prompt = f"""
    אני נותן לך קוד HTML של דף אינטרנט:
    {html}

    זהה את האלמנטים הפעילים (כפתורים, קישורים, טפסים)
    ותאר את הפעולות האפשריות שניתן לבצע עליהם.
    החזר רשימה מסודרת לפי סוג האלמנט.
    """

    response = Ai_agent.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "אתה עוזר לאוטומציה עם Selenium."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


# ---- Selenium ----
driver = webdriver.Chrome()
# the path of the file
driver.get("file:///Users/raniaburaia/PycharmProjects/Captain-Fix/ActionChainsEx.Html")
driver.maximize_window()

page_source = driver.page_source
llm_suggestions = analyze_html_with_llm(page_source)

driver.quit()

print("\nה-LLM מציע את הפעולות הבאות:\n")
print(llm_suggestions)

confirm = input("\nרוצה לבצע את הפעולות? (y/n): ")

if confirm.lower() == "y":
    print("\nמייצר קוד אוטומציה....\n")


    response = Ai_agent.chat.completions.create (
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an experienced QA engineer writing Selenium Python automation."},
            {"role": "system", "content": "Return ONLY raw Python code. No explanations. No markdown."},
            {"role": "system", "content": "the operation system is macOS."},
            {"role": "system", "content": "Use the URL: file:///Users/raniaburaia/PycharmProjects/Captain-Fix/ActionChainsEx.Html"},
            {"role": "system", "content": "Handle the following actions: " + llm_suggestions},
            {"role": "user", "content": "Produce a Python Selenium script and maximize the window."}
        ],
        max_tokens=500
    )

    script_code = response.choices[0].message.content

    print("\nהקוד שנוצר:\n")
    print(script_code)

    exec(script_code)

else:
    print("\nביצוע הפעולות בוטל.")