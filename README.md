# **ComfyPlus**

*The New Application Layer for Enhanced Comfy*

---

Empowering AI Application Anywhere  
No Installation or GPU Required, Multi \- Modal Support and Seamless Workflow Execution 

---

[![ComfyPlus][website-shield]][website-url]
[![Discord][discord-shield]][discord-url]
<br>
[![][github-release-shield]][github-release-link]
[![][github-release-date-shield]][github-release-link]
[![][github-downloads-shield]][github-downloads-link]
[![][github-downloads-latest-shield]][github-downloads-link]

[matrix-shield]: https://img.shields.io/badge/Matrix-000000?style=flat&logo=matrix&logoColor=white
[matrix-url]: https://app.element.io/#/room/%23comfyui_space%3Amatrix.org
[website-shield]: https://img.shields.io/badge/ComfyPlus-blue?style=flat
[website-url]: https://comfyplus.run

[discord-shield]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fdiscord.com%2Fapi%2Finvites%2Fcomfyorg%3Fwith_counts%3Dtrue&query=%24.approximate_member_count&logo=discord&logoColor=white&label=Discord&color=green&suffix=%20total
[discord-url]: https://discord.com/invite/GhXU7sfXvE

[github-release-shield]: https://img.shields.io/github/v/release/ComfyPlus/ComfyPlus_Anywhere?style=flat&sort=semver
[github-release-link]: https://github.com/ComfyPlus/ComfyPlus_Anywhere/releases
[github-release-date-shield]: https://img.shields.io/github/release-date/ComfyPlus/ComfyPlus_Anywhere?style=flat
[github-downloads-shield]: https://img.shields.io/github/downloads/ComfyPlus/ComfyPlus_Anywhere/total?style=flat
[github-downloads-latest-shield]: https://img.shields.io/github/downloads/ComfyPlus/ComfyPlus_Anywhere/latest/total?style=flat&label=downloads%40latest
[github-downloads-link]: https://github.com/ComfyPlus/ComfyPlus_Anywhere/releases

---

**[Setting Up the ComfyPlus\_Anywhere Plugin](docs/setup.md)**

**[Get Started with ComfyPlus\_Anywhere](docs/start.md)**

---

**Key Features**  
Unlock the full potential of AI development with ComfyPlus – Your Ultimate Platform for Creating, Managing, and Running AI Workflows.

* **AI** **Workflow Management**  
  - Seamlessly manage, create, edit, and share your AI workflows. Enabling users to easily build and run complex AI projects.  
  - Create and edit AI workflows with ease.  
  - Share workflows with colleagues and teams.  
  - Simplify complex AI project management.

* **Multiple Access (Local \+ Cloud \+ Lite versions)**  
  - ComfyPlus offers multiple access modes, allowing users to run workflows in different environments:  
  - **Local** Mode: Run Comfy workflows directly on your machines anywhere for free.  
  - **Cloud** Mode: Run ComfyPlus workflows remotely via our cloud for greater flexibility.  
  - **Lite** Version: Experience ComfyPlus with limited features, perfect for getting started and testing basic functionality.  
       
* **Multi-Modal Support, Including GPT, TTS, Text-to-Image, Image-to-Image, 3D, and Traditional Deep Learning Algorithms**  
  - ComfyPlus supports a wide range of AI models, including GPT for text generation, TTS for speech synthesis, Text-to-Image and Image-to-Image for visual creation and manipulation, 3D modeling, and traditional deep learning algorithms, addressing diverse AI use cases by nodes.

* **Model Training and Fine-Tuning (Coming Soon)**  
  - ComfyPlus will soon provide powerful tools for training and fine-tuning AI models, enabling users to optimize pre-existing models for specific tasks and improve performance.

* **Distributed Task Scheduling (Coming Soon)**  
  - With distributed task scheduling, ComfyPlus will allow users to assign tasks across multiple machines, enhancing efficiency and speeding up processing for large-scale AI projects.

* **Subflow Support (Coming Soon)**  
  - Soon, ComfyPlus will support creating modular subflows, allowing you to build reusable workflow components for greater flexibility and efficiency in AI project management.

---

## **[ComfyPlus\_Anywhere Plugin Setup Guide](docs/setup.md)**

Enhance your workflow with the powerful ComfyPlus\_Anywhere plugin. This guide provides two methods for installation: the ZIP method for simplicity and the Git method for efficient updates.

---

### **Method 1: Installing via ZIP**

**1️ Visit the Official Repository**

* Navigate to the plugin repository: **[ComfyPlus\_Anywhere GitHub](https://github.com/ComfyPlus/ComfyPlus_Anywhere).**

**2️ Download the Plugin**

* Click the green \<\> Code button.  
* Select Download ZIP to download the plugin files.

**3️ Install the Plugin**

* Extract the ZIP file and copy the folder into `comfyui/custom_nodes`.

**4️ Restart ComfyUI**

* Relaunch ComfyUI to activate the plugin and enjoy its powerful features\!

![](/images/image112.png)

---

### **Method 2: Installing via Git**

**Prerequisites:**

* **Ensure Git is installed and configured on your system. [Download Git](https://git-scm.com/).**

**1️⃣ Access the Plugin Repository**

* **Open the repository: [ComfyPlus\_Anywhere GitHub](https://github.com/ComfyPlus/ComfyPlus_Anywhere).**  
* **Click the green \<\> Code button.**  
* **Select the HTTPS option and copy the repository URL.**

![](/images/image114.png)


**2️⃣ Clone the Repository**

* Open your **CMD terminal**.

Navigate to your ComfyUI plugin directory using the `cd` command, e.g.,

```bash
cd E://ComfyUI_windows_portable/ComfyUI/custom_nodes
```

**Clone the repository using the following command:**  

```bash
git clone https://github.com/ltdrdata/ComfyPlus_Anywhere.git
```

**3️⃣ Restart ComfyUI**

* Once the cloning is complete, restart **ComfyUI**.  
* Verify the installation by checking the interface or plugin functionality.

---

**Both methods are effective. Choose ZIP for simplicity or Git for ongoing updates. Enjoy the enhanced capabilities of ComfyPlus\_Anywhere\!**

---

## **Run ComfyUI**

### **1️ Open CMD and Navigate to the Project Directory**

Run this command to access the directory where you cloned **ComfyUI**:

```bash
cd ComfyUI
```

### **2️ Install Dependencies**

Ensure everything runs smoothly by installing required libraries:

```bash
pip3 install -r requirements.txt
```

### **3️ Launch the Project**

Run ComfyUI with a single command:

```bash
python3 main.py
```

or 

```bash
python3 ComfyUI.py
```

### **4️ Explore the Documentation**

Need help? The detailed instructions are right in the `README.md`. Check it out:

```bash
cat README.md
```

### **5️ Troubleshooting Made Easy**

🌟 **Permission Issues?** Add `--user` or use `sudo`:

```bash
pip3 install --user -r requirements.txt
```

🌟 **Prefer a Virtual Environment?** Isolate your setup:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

🌟 **Encounter Errors?** Visit our [Issues Page](https://github.com/comfyanonymous/ComfyUI/issues) for quick solutions.

---

[Get Started with ComfyPlus Anywhere in Just a Few Steps\!](docs/start.md)

**\* Please ensure that the setup of ComfyPlus Anywhere has been completed according to the steps outlined above. \***

---

**Running ComfyPlus Anywhere is** simple and straightforward. Follow this guide and experience seamless AI workflows like never before\!

Connecting to an instance is simple:

![](/images/image113.png)

1️⃣ **Click "Connect"**  
Begin the connection process by clicking the **"Connect"** button.

![](/images/image111.png)

2️⃣ **Get Your Token**

* Navigate to the **ComfyPlus Dashboard**.  
* Go to the **Instance Management** section.  
* Find and copy the token for the desired instance.

![](/images/image116.png)

![](/images/image117.png)

3️⃣ **Paste and Connect**

* Paste the token into the input box as shown below.  
* Click **"Connect"** to complete the process\!

![](/images/image118.png)

### **✅ All Set and Ready to Go\!**

Once installed, you can start using **ComfyPlus\_Anywhere** to streamline your AI workflows. Customize and configure to suit your needs\!

Don’t wait—dive into the future of AI workflows now\! 🚀
