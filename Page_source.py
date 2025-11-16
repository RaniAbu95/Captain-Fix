from openai import OpenAI
# ---- הגדרות OpenAI ----
Ai_agent = OpenAI(api_key="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")
from selenium import webdriver

def analyze_html_with_llm(html):
    prompt = f"""
    אני נותן לך קוד HTML של דף אינטרנט:
    {html}

    זהה את האלמנטים הפעילים (כפתורים, קישורים, טפסים) ותאר את הפעולות האפשריות שניתן לבצע עליהם.
    החזר את זה כרשימה ברורה, ממוינת לפי סוג האלמנט.
    """
    response = Ai_agent.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "אתה עוזר לאוטומציה עם Selenium."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
# אתחול סליניום
driver = webdriver.Chrome()
driver.get('file:///Users/raniaburaia/PycharmProjects/Captain-Fix/ActionChainsEx.Html')
driver.maximize_window()
# קבלת HTML ושליחה ל LLM
page_source = driver.page_source
llm_suggestions = analyze_html_with_llm(page_source)
driver.quit()
#הצגת הפעולות
print('ה LLM מציע את הפעולות הבאות\n')
print(llm_suggestions)

confirm = input("\n רוצה לבצע את הפעולות הבאות ? (y/n): ")
if confirm== "y":
    print("\n מבצע אוטומצייה על האלמנטים")
    # בקשה מ LLM לכתוב סקריפט מלא בסלניום לביצוע הפעולות
    response =Ai_agent.chat.completions.create(
    model ='gpt-4o-mini',
    messages=[
        {"role":"system", "content": "you are an experinced  qa engineer, required to write a test webpage with selenium"},
        {"role":"system","content":"the response should be a valid python script that will run in selenium,without any explanations or markdown formmating"},
        {"role":"system","content":"use this url:\"file:///C:/Users/ssssa/Desktop/QA%202024/Exercises/%D7%AA%D7%A8%D7%92%D7%99%D7%9C%20Action%20Chains/ActionChainsEx.Html"},
        {"role":"system","content":"the script should be able to handle the following actions:"+llm_suggestions},
        {"role": "system",
         "content": "example: for locating elements use this command <driver.find_element(By.ID, \"{value from source code}\")>"},
        {"role":"system","content":" for assertions look for the message box locator value in source code and print the message text "},
        {'role': 'user', 'content': f"please provide a valid python script,please maximize the size od driver window "}
        ],max_tokens=500
    )
    # הקוד שחזר מ LLM
    script_code = response.choices[0].message.content
    print("\n הקוד שנוצר הוא")
    print(script_code)
    #  הרצת הקוד
    exec(script_code)
else:
    print("\n ביצוע הפעולות בוטל")

