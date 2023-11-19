import openai
import textwrap

# Initialize the OpenAI client - it will automatically use the OPENAI_API_KEY environment variable
client = openai.Client()

# Step 1: Create an Assistant
# This assistant is configured to build other agents based on user specifications
# Specifically, a web scraping agent according to SOB guidelines
web_scraping_agent = client.beta.assistants.create(
    name="SOB Web Scraping Agent",
    instructions=textwrap.dedent("""\
        You are an agent specialized in web scraping. Your task is to extract data from websites
        in a structured format while following the legal and ethical guidelines outlined by the
        Supreme Oversight Board (SOB). Ensure that you respect the robots.txt file of the websites,
        handle user data with confidentiality, and do not overload the website servers with requests.
    """),
    tools=[
        {"type": "code_interpreter"},
        {"type": "retrieval"},
    ],
    model="gpt-4-1106-preview"
)

# Step 2: Create a Thread
# This thread represents a conversation where agent building will be handled
thread = client.beta.threads.create()

# Assuming 'user_request' contains the details for a new agent
user_request = "Please create a web scraping agent that can extract product details from e-commerce sites."

# Step 3: Add a Message to a Thread
# This message tells the Assistant what kind of agent to build
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_request
)

# Step 4: Run the Assistant
# The Assistant processes the message and builds the agent
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=web_scraping_agent.id
)

# Step 5: Display the Assistant's Response
# After the run is complete, the built agent's details are retrieved
run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

# Retrieve messages added by the Assistant to the Thread
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# Display the Assistant's response
for msg in messages.data:
    if msg.role == "assistant":
        print(f"Assistant's response: {msg.content.text.value}")