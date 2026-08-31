import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

RESUME_SUMMARY = """
Adarsh Sahay - Full-stack software engineering student (BITS Pilani / RMIT Melbourne).
Skills: JavaScript, Dart (Flutter), Python, Java, C, Node.js, Express, FastAPI, REST APIs,
JWT auth, SQLAlchemy, Prisma ORM, MySQL, AI/LLM integration, Firebase, Socket.io/WebSockets.
Projects: AI-powered skincare tracking app (Flutter + Node.js + Groq AI), Premier League
management system with AI predictions (Flask + Gemini), campus e-commerce platform
(Node.js + real-time tracking), and this job application tracker automation (FastAPI + Make.com).
Open to: software engineering internships/roles, and also casual/part-time work of any kind
(retail, hospitality, kitchen) as flexible income while studying.
"""


def score_job(title: str, company: str, location: str) -> tuple[int, str]:
    """Returns (score 0-100, short reason). Falls back to a neutral score on any failure."""
    prompt = f"""You are helping a university student evaluate job postings.

Candidate background:
{RESUME_SUMMARY}

Job posting:
Title: {title}
Company: {company}
Location: {location}

Rate how good a fit this job is for the candidate on a scale of 0-100, considering both
career-relevant tech roles AND casual/part-time work (both are welcome).
Respond in EXACTLY this format, nothing else:
SCORE: <number>
REASON: <one short sentence, max 15 words>
"""

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )

        message = response.choices[0].message
        text = message.content

        if not text:
            return 50, f"AI returned empty response (finish_reason: {response.choices[0].finish_reason})"

        text = text.strip()

        score = 50
        reason = "Could not parse AI response"
        for line in text.splitlines():
            if line.upper().startswith("SCORE:"):
                score = int("".join(filter(str.isdigit, line)))
            elif line.upper().startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()

        return score, reason
    except Exception as e:
        return 50, f"AI scoring unavailable ({str(e)[:100]})"