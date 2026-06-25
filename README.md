# MASP — Multi-Agent Research Assistant

A sophisticated AI-powered research assistant that leverages multiple specialized agents to conduct web research, synthesize information, and provide constructive feedback on generated reports. Built with LangChain and Google Gemini, MASP demonstrates an advanced feedback loop where AI agents collaborate to improve research quality.

## 🎯 Overview

MASP implements a 5-step research pipeline where different AI agents work together to:
1. **Search** for information across the web
2. **Read** and extract relevant content from sources
3. **Write** structured, detailed research reports
4. **Critique** reports for accuracy and depth
5. **Refine** reports based on critical feedback

The system creates a feedback loop where initial reports are improved iteratively based on AI-generated criticism, ensuring higher quality outputs.

## 🏗️ Architecture

### Core Components

#### **Agents** (`agents.py`)
- **Search Agent**: Uses web search tools to find reliable, recent information
- **Reader Agent**: Scrapes URLs to extract detailed content
- **Writer Chain**: Generates well-structured research reports
- **Critic Chain**: Evaluates reports for accuracy, clarity, and depth
- **Refiner Chain**: Improves reports based on critical feedback

#### **Tools** (`tools.py`)
- **`web_search(query)`**: Searches using Tavily API for top 5 results with titles, URLs, and snippets
- **`scrape_url(url)`**: Extracts and cleans text content from URLs using BeautifulSoup

#### **Pipeline** (`pipeline.py`)
Orchestrates the 5-step process with state management and timing controls:
```
Search → Read → Write → Critique → Refine
```

#### **Frontend** (`app.py`)
Streamlit-based web interface with custom styling using Space Grotesk and Space Mono fonts.

## 🚀 Features

- **Multi-Agent Collaboration**: Specialized agents handle different research aspects
- **Iterative Improvement**: Built-in feedback and refinement loop
- **Web Integration**: Real-time web search and content scraping
- **Structured Output**: Reports include Introduction, Key Findings, Conclusion, and Sources
- **Professional UI**: Clean, modern Streamlit interface with custom styling
- **Quality Assurance**: Automatic critique and scoring (X/10) of generated content

## 📋 Requirements

The project uses the following key dependencies:

- **LangChain**: Core framework for agent orchestration
- **Google Gemini 2.5 Flash**: Primary language model
- **Tavily API**: Web search functionality
- **BeautifulSoup4**: Web scraping
- **Streamlit**: Web interface
- **Python Dotenv**: Environment variable management

See `requirements.txt` for complete dependency list.

## 🔧 Setup & Installation

### Prerequisites
- Python 3.8+
- API Keys for:
  - Google Gemini (`GEMINI_API_KEY`)
  - Tavily Search (`TAVILY_API_KEY`)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd masproj
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

### Web Interface
1. Open the Streamlit app (typically `http://localhost:8501`)
2. Enter your research topic
3. The system automatically runs through all 5 stages:
   - Stage 1: Searches for relevant information
   - Stage 2: Reads and extracts detailed content
   - Stage 3: Writes a comprehensive report
   - Stage 4: Critiques the report (generates score and feedback)
   - Stage 5: Refines the report based on criticism

### Command Line
```bash
python pipeline.py
# Then enter your research topic when prompted
```

## 🔄 Research Pipeline Details

### Step 1: Search Agent
- Queries the web for recent, reliable information
- Returns top 5 results with titles, URLs, and content snippets
- 5-second delay before proceeding to Step 2

### Step 2: Reader Agent
- Analyzes search results
- Selects the most relevant URL
- Scrapes and extracts clean text content (up to 3000 characters)
- 5-second delay before proceeding to Step 3

### Step 3: Writer
- Combines search results and scraped content
- Generates structured report with:
  - Introduction
  - Key Findings (minimum 3 points)
  - Conclusion
  - Sources
- Professional, detailed, and factual tone
- 5-second delay before proceeding to Step 4

### Step 4: Critic
- Evaluates the generated report
- Provides structured feedback:
  - **Score**: X/10 rating
  - **Strengths**: Key positive aspects
  - **Areas for Improvement**: Constructive suggestions
  - **Verdict**: One-line summary
- 5-second delay before proceeding to Step 5

### Step 5: Refiner
- Rewrites the report incorporating all critical feedback
- Maintains original structure (Intro, Key Findings, Conclusion, Sources)
- Addresses every identified issue
- Produces final polished output

## 🛠️ Project Structure

```
masproj/
├── app.py              # Streamlit web interface
├── agents.py           # Agent definitions & chains
├── pipeline.py         # Research orchestration pipeline
├── tools.py            # Web search & scraping tools
├── requirements.txt    # Python dependencies
├── .env               # API keys (not in repo)
└── README.md          # This file
```

## 🔑 Key Technologies

| Component | Technology |
|-----------|-----------|
| **LLM** | Google Gemini 2.5 Flash |
| **Framework** | LangChain + LangChain Community |
| **Web Search** | Tavily API |
| **Web Scraping** | BeautifulSoup4 |
| **UI** | Streamlit |
| **Config** | Python Dotenv |
| **Text Processing** | Requests, LXML |

## 💡 How Feedback Loop Works

```
User Input (Topic)
        ↓
    [Search Agent]
        ↓
    [Reader Agent]
        ↓
    [Writer] → Generate Report
        ↓
    [Critic] → Evaluate & Score
        ↓
    [Refiner] → Improve Based on Feedback
        ↓
    Final Polished Report
```

This architecture ensures that reports are:
- Well-researched (multi-source information)
- Thoroughly reviewed (AI criticism)
- Iteratively improved (feedback integration)
- High-quality outputs

## 📊 Output Structure

Each research report includes:

```
[INTRODUCTION]
Overview of the topic

[KEY FINDINGS]
• Finding 1: Detailed explanation
• Finding 2: Detailed explanation
• Finding 3+ : Additional insights

[CONCLUSION]
Summary and implications

[SOURCES]
- Title 1 (URL)
- Title 2 (URL)
- Title 3+ (URLs)

[QUALITY METRICS]
Score: X/10
Strengths: [Listed]
Improvements Made: [Listed]
```

## ⚙️ Configuration

### Model Settings
- **Model**: Google Gemini 2.5 Flash
- **Temperature**: 0.7 (balanced creativity & consistency)
- **Max Retries**: 2
- **Search Results**: Top 5 per query
- **Content Limit**: 3000 characters per scraped page

### Timing
- 5-second delay between pipeline stages (prevents rate limiting)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not found` | Add key to `.env` file |
| `TAVILY_API_KEY not found` | Add key to `.env` file |
| Web scraping timeouts | Check URL accessibility |
| Empty search results | Try different search terms |
| Streamlit errors | Ensure all dependencies installed |

## 🎨 Styling

The Streamlit interface features:
- Dark theme with purple gradient background (#3D1534)
- Space Grotesk font for body text
- Space Mono font for code/technical elements
- Clean, professional layout
- Hidden Streamlit chrome (menu, footer)

## 📝 Example Workflow

```bash
$ python pipeline.py
Enter Research Topic: Artificial Intelligence in Healthcare

STEP 1: SEARCH AGENT
[Searching for AI in Healthcare...]
[Found 5 relevant sources]

STEP 2: READER AGENT
[Scraping most relevant URL...]
[Extracted 2,847 characters]

STEP 3: WRITER
[Generating comprehensive report...]
[Report generated with 3 key findings]

STEP 4: CRITIC
[Evaluating report quality...]
Score: 7.5/10
Strengths: Well-structured, comprehensive research
Areas for Improvement: Add more recent statistics, expand on implementation challenges

STEP 5: REFINER
[Improving report based on feedback...]
[Final report ready with all improvements applied]
```

## 🚀 Future Enhancements

Potential improvements:
- Multi-source comparison analysis
- Sentiment analysis of findings
- Automatic citation formatting (APA, MLA, Chicago)
- Report export to PDF/Word formats
- Custom report templates
- Caching for repeated queries
- Parallel agent execution
- Advanced filtering and sorting of sources

## 👤 Author

[Rashi Kaushik]

---

**MASP** demonstrates advanced AI orchestration with feedback loops, creating a framework for intelligent, iterative research that combines multiple specialized agents for superior output quality.
