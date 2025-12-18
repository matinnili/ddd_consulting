from openai import OpenAI




client=OpenAI()


def generate_questions(prompt: str, max_questions: int = 5,**kwargs) -> list[str]:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates interview questions."},
            {"role": "user", "content": f"Generate {max_questions} interview questions based on the following prompt: {prompt}"}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    questions_text = response.choices[0].message.content
    questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
    return questions