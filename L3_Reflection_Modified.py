from utils import get_openai_api_key
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"model": "gpt-3.5-turbo"} 

# Legal chatbot task - reviewing documents for legal compliance
task = '''
Please review the following document for legal compliance and provide feedback:
"Company X requires all employees to sign non-compete agreements that prevent them from working in the same industry for 5 years after termination. The company also reserves the right to monitor all employee communications without notice."
'''

import autogen

# Legal Document Reviewer Agent
legal_reviewer = autogen.AssistantAgent(
    name="Legal_Reviewer",
    system_message="You are an experienced legal attorney specializing in employment law and compliance. "
        "Your role is to review documents for legal compliance, identify potential legal issues, "
        "and provide actionable recommendations. Focus on: "
        "- Employment law compliance (non-compete agreements, monitoring policies) "
        "- Data privacy regulations "
        "- Contract validity and enforceability "
        "- Potential liability risks "
        "Provide clear, concise legal analysis with specific recommendations. "
        "Cite relevant legal principles when appropriate.",
    llm_config=llm_config,
)

# Legal Research Assistant
legal_researcher = autogen.AssistantAgent(
    name="Legal_Researcher",
    system_message="You are a legal research assistant. Your role is to: "
        "- Research relevant laws and regulations "
        "- Provide case law references when applicable "
        "- Identify jurisdictional variations "
        "- Offer best practices in legal drafting "
        "Keep responses factual and reference reliable legal sources.",
    llm_config=llm_config,
)

# Compliance Checker
compliance_checker = autogen.AssiantAgent(
    name="Compliance_Checker",
    system_message="You specialize in regulatory compliance across different jurisdictions. "
        "Your focus areas include: "
        "- GDPR and data protection compliance "
        "- Employment standards compliance "
        "- Industry-specific regulations "
        "- International compliance requirements "
        "Provide specific compliance recommendations and risk assessments.",
    llm_config=llm_config,
)

# Client Communication Specialist
client_communicator = autogen.AssistantAgent(
    name="Client_Communicator",
    system_message="You translate complex legal concepts into clear, understandable language for clients. "
        "Your role is to ensure legal advice is: "
        "- Accessible to non-lawyers "
        "- Actionable and practical "
        "- Prioritized by risk level "
        "- Followed by clear next steps "
        "Always maintain a professional but approachable tone.",
    llm_config=llm_config,
)

# Legal Chatbot Orchestrator
legal_bot = autogen.AssistantAgent(
    name="Legal_Chatbot",
    system_message="You are a comprehensive legal assistance chatbot. "
        "Coordinate between specialized legal agents to provide complete legal review services. "
        "Ensure all legal aspects are covered: compliance, research, risk assessment, and client communication. "
        "Present final recommendations in a structured, comprehensive manner.",
    llm_config=llm_config,
)

# Define the review workflow
def legal_review_workflow(recipient, messages, sender, config):
    return f'''Please conduct a comprehensive legal review of the following document:
    
    DOCUMENT FOR REVIEW:
    {recipient.chat_messages_for_summary(sender)[-1]['content']}
    
    Please analyze for:
    1. Legal compliance issues
    2. Potential liability risks
    3. Regulatory requirements
    4. Recommended modifications
    5. Risk mitigation strategies'''

# Set up the nested chat structure
review_chats = [
    {
        "recipient": legal_reviewer,
        "message": legal_review_workflow,
        "max_turns": 2,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Provide a concise legal analysis focusing on main issues and recommendations."
        }
    },
    {
        "recipient": legal_researcher,
        "message": "Research relevant laws and regulations applicable to this document. Focus on employment law, non-compete agreements, and privacy regulations.",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Summarize key legal research findings with relevant statutes or case law references."
        }
    },
    {
        "recipient": compliance_checker,
        "message": "Conduct a compliance check focusing on data privacy, employment standards, and regulatory requirements.",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "List compliance issues and recommended fixes in bullet points."
        }
    },
    {
        "recipient": client_communicator,
        "message": "Translate the legal findings into clear, actionable advice for a business client.",
        "max_turns": 1,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Provide client-friendly recommendations with priority levels and next steps."
        }
    }
]

# Register the nested chats with the legal bot
legal_bot.register_nested_chats(
    review_chats,
    trigger=legal_reviewer,
)

# Initiate the legal review process
print("=== LEGAL CHATBOT - DOCUMENT REVIEW ===")
print(f"Reviewing document: {task}")
print("\n" + "="*50 + "\n")

result = legal_bot.initiate_chat(
    recipient=legal_reviewer,
    message=task,
    max_turns=3,
    summary_method="last_msg"
)

print("\n" + "="*50)
print("FINAL LEGAL REVIEW SUMMARY:")
print("="*50)
print(result.summary)

# Additional functionality for ongoing legal queries
def ask_legal_question(question):
    """Function to ask follow-up legal questions"""
    response = legal_bot.generate_reply(
        messages=[{"content": f"Additional legal question: {question}", "role": "user"}]
    )
    return response

# Example of asking a follow-up question
follow_up = "What would be a reasonable non-compete duration in California?"
print(f"\nFollow-up question: {follow_up}")
follow_up_response = ask_legal_question(follow_up)
print(f"Legal advice: {follow_up_response}")

# Save the legal review to a file
def save_legal_review(review_content, filename="legal_review_report.txt"):
    with open(filename, 'w') as f:
        f.write("LEGAL REVIEW REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(review_content)
    print(f"\nLegal review saved to {filename}")

save_legal_review(result.summary)