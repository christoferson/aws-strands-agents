# aws-strands-agents

# 🤖 AWS Strands Agents

AWS Bedrock integration with Strands AI agents framework for building intelligent conversational agents.

## 🚀 Installation

### 1. Clone the Repository
git clone https://github.com/christoferson/aws-strands-agents.git
cd aws-strands-agents

### 2. Install Package Manager (UV - Ultra-fast Python package installer)
py -3.12 -m pip install uv

### 3. Install Core Dependencies

py -3.12 -m pip install --upgrade pip

py -3.12 -m pip install --upgrade boto3

py -3.12 -m pip install --upgrade strands-agents

py -3.12 -m pip install --upgrade strands-agents-tools

py -3.12 -m pip install --upgrade requests 

py -3.12 -m pip install --upgrade beautifulsoup4

py -3.12 -m pip install --upgrade wikipedia



### 4. Verify Installation

#### Check Strands agents installation details

py -3.12 -m pip show strands-agents

#### List all installed packages

py -3.12 -m pip list

## ⚙️ Configuration

### Set AWS profile (replace 'xxxx' with your actual profile name)
set AWS_PROFILE=your-aws-profile-name

## Basic Demo

py -3.12 demo_strands_basic.py

py -3.12 demo_strands_config.py

py -3.12 demo_strands_logging.py

py -3.12 demo_strands_conversation_history.py

py -3.12 demo_strands_agent_state.py

py -3.12 demo_strands_request_state.py

py -3.12 demo_strands_bedrock.py

py -3.12 demo_strands_callback.py

py -3.12 demo_strands_callback_event_loop.py

py -3.12 demo_strands_async_iterator.py

py -3.12 demo_strands_tool_builtin.py

py -3.12 demo_strands_tool_custom.py

py -3.12 demo_strands_tool_mcp.py

###

py -3.12 demo_tool_read_web_content.py

py -3.12 demo_tool_wikipedia.py

## Resources

https://strandsagents.com/latest/documentation/docs/

https://docs.aws.amazon.com/bedrock/

https://strandsagents.com/

https://github.com/strands-agents/sdk-python