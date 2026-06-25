from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
    refiner_chain
)

import time


def run_research_pipeline(topic: str):

    state = {}

    # ==========================================
    # STEP 1 : SEARCH AGENT
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 1 : SEARCH AGENT")
    print("=" * 60)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Search the web for reliable and recent information about {topic}"
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print(state["search_results"])

    time.sleep(5)

    # ==========================================
    # STEP 2 : READER AGENT
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 2 : READER AGENT")
    print("=" * 60)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Choose the most relevant URL from these search results
and scrape it.

Search Results:

{state["search_results"][:1000]}
"""
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print(state["scraped_content"][:1000])

    time.sleep(5)

    # ==========================================
    # STEP 3 : WRITER
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 3 : WRITER")
    print("=" * 60)

    research_data = f"""
SEARCH RESULTS:
{state['search_results']}

SCRAPED CONTENT:
{state['scraped_content']}
"""

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_data
    })

    print("\nREPORT GENERATED")

    time.sleep(5)

    # ==========================================
    # STEP 4 : CRITIC
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 4 : CRITIC")
    print("=" * 60)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print(state["feedback"])

    time.sleep(5)

    # ==========================================
    # STEP 5 : REFINER
    # ==========================================

    print("\n" + "=" * 60)
    print("STEP 5 : REFINER")
    print("=" * 60)

    state["final_report"] = refiner_chain.invoke({
        "report": state["report"],
        "feedback": state["feedback"]
    })

    print(state["final_report"])

    return state


if __name__ == "__main__":

    topic = input("\nEnter Research Topic: ")

    run_research_pipeline(topic)