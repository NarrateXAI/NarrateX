# NarrateXAI

<div align="center">
  <img src="./src/img/narratex_nobg.png" alt="NarrateXAI Banner" width="375" />
</div>

NarrateXAI is a **Text-to-Video AI Agent Storyline Framework**, built on top of the powerful [**PydanticAI**](https://ai.pydantic.dev/) framework. It brings your narratives to life by combining character-driven storytelling with cutting-edge AI technology.

---

## Overview

<div align="center">
  <img src="./src/img/workflow.svg" alt="NarrateXAI Workflow" width="100%" />
</div>

## Features

| **Feature**                        | **Description**                                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Character Lore**                 | Define rich, structured backstories and traits for your AI agents to enhance storytelling depth.                  |
| **Prompt Classification AI Agent** | Automatically classify user prompts into categories like "Chat" or "Vision" for tailored responses.               |
| **Character AI Agents**            | Generate responses based on the defined character lore, ensuring consistency in personality.                      |
| **Text-to-Video AI Agent**         | Convert narrative responses into videos using integrated text-to-video APIs like CogVideo, Sora, or Veo.\*        |
| **Text-to-Video Prompt Generator** | Create detailed prompts for external text-to-video services when visual storytelling is needed.                   |
| **API Integration**                | Seamlessly integrates with text-to-video AI providers (e.g., CogVideoX, Sora*, Veo*) to generate dynamic visuals. |

_\*API availability may vary based on provider support._

---

## Use Cases

- **Chatbots**: Create conversational agents with personality and visual appeal.
- **Social Media AI Agents**: Build engaging AI-driven content creators.
- **Creative Storytelling**: Develop immersive storylines and bring them to life with visuals.
- **Educational Tools**: Visualize lessons with AI-crafted characters.
- **Gaming Prototypes**: Define characters and scenes for RPGs or narrative-driven games.

---

## Quick Start Guide

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- [Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads)

---

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/NarrateXAI/NarrateX.git
   cd NarrateX
   ```

2. **Set Up a Virtual Environment (Optional)**:

   ```bash
   python -m venv myenv
   ```

   Activate the virtual environment:

   - On macOS or Linux:
     ```bash
     source myenv/bin/activate
     ```
   - On Windows:
     ```bash
     # CMD
     myenv\Scripts\activate.bat
     # PowerShell
     .\myenv\Scripts\Activate.ps1
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Environment**:  
   Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` to configure:

   - AI API Key
   - X account details (optional)
   - Chromedriver path

5. **Customize Your Agent**:  
   Open `/starter/char.py` to configure your own character using the **Character Lore Template**.

6. **Start the Agent**:  
   Run the starter script to interact with your AI agent:
   ```bash
   python -m starter.simple_chat.py
   ```

---

## Congratulations!

Your AI Agent is ready. Start interacting with a personalized agent powered by NarrateXAI!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For questions or issues, visit our [GitHub repository](https://github.com/NarrateXAI/NarrateX) or open an issue.
