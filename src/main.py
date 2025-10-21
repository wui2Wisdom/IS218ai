import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment (.env).")
        return

    client = OpenAI(api_key=api_key)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello World' in one short sentence."},
            ],
            temperature=0.2,
        )
        print(resp.choices[0].message.content)
    except Exception as e:
        print(f"OpenAI API error: {e}")

if __name__ == "__main__":
    main()
