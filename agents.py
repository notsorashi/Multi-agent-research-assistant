from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

# Load environment variables
load_dotenv()

# Verify API key
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY not found. Add it to your .env file."
    )
#model setup

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2,
)

#search agent setup
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )
    
#reader agent setup
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )
    
#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed report on the topic below.
     Topic: {topic}
     Research Gathered: {research}
     
     Structure the report as:
     - Introduction
     -Key Findings(minimum 3 well-explained points)
     - Conclusion
     -Sources (list all sources used in the research)
     
     Be detailed, factual and professional."""),
    ])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research critic. Critically evaluate the report below for accuracy, clarity, and depth."),
    ("human", """Critique the following report:
     Report: {report}
     
     Respond in this exact format :
     Score : X/10
     Strengths: 
     -....
     -....
     Areas for Improvement:
     -....
     
     One line verdict:
    ...
     
     Be constructive, factual and professional."""),
    ])

critic_chain = critic_prompt | llm | StrOutputParser()

#refiner chain
refiner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert editor."
    ),
    (
        "human",
        """
        Improve the report using the feedback.

        REPORT:
        {report}

        FEEDBACK:
        {feedback}

        Rewrite the entire report.
        Fix every issue mentioned.

        Keep:
        - Introduction
        - Key Findings
        - Conclusion
        - Sources
        """
    )
])

refiner_chain = refiner_prompt | llm | StrOutputParser()

