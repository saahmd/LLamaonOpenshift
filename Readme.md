# AIOps Automation Solution with Ansible Automation Platform & LlamaStack on OpenShift

## 📌 Overview
This project demonstrates an **end-to-end AIOps automation framework** built using:
- **Ansible Automation Platform (AAP)**
- **OpenShift** 

The solution automates detection, analysis, notification, and remediation of node/service failures (e.g., HTTP service downtime).

---

## ⚙️ Workflow

### 1. Alert Generation
- Kafka is preconfigured to **send alerts** when an HTTP service goes down on a node.

### 2. Event Handling with EDA
- Event Driven Ansible (EDA) **picks up the Kafka alert**.
- EDA triggers the **AI Insights Workflow** in Ansible Automation Platform.

### 3. AI Insights Workflow in AAP
The **AI Insights Workflow Template** contains 3 job templates:
1. **Root Cause Analysis (RCA)**  
   - Error is sent to an underlying LLM for analysis.
2. **Playbook Generation Prompt**  
   - After RCA, an LLM-generated prompt is passed to **Lightspeed** to generate a remediation playbook.
3. **Slack Notification**  
   - Error details are sent to Slack to notify the NOC engineer.

---

### 4. Human Interaction via LlamaStack Agent
- Engineer queries the **LlamaStack Agent UI** for:
  - List of recent events.
  - The RCA-generated prompt.  
- Engineer decides whether to reuse or modify the prompt.

---

### 5. Playbook Generation & Validation
- Engineer runs **template ID 19** in AAP.  
- This connects with **Lightspeed** to generate a remediation playbook.  
- The generated playbook is:
  - Displayed on the **LlamaStack UI**.
  - Reviewed by the engineer.  
- If unsatisfactory, a new prompt can be used to regenerate the playbook.

---

### 6. Remediation Workflow in AAP
If approved, the engineer triggers the **Remediation Workflow Template**, which includes:
1. Push the playbook to **Git**.
2. Sync the **AAP project** with Git.
3. Create a job template for the playbook, hosts, and inventories (if not already present).
4. Trigger the job template to **run the playbook**.

---

### 7. Issue Resolution
- The final template in the Remediation Workflow executes the playbook.
- The **HTTP service issue is remediated automatically**.

---


### Steps to Run the Workflow:

## Prerequisites:

1. Llamastack configured on Openshift using the steps mentioned here llama-on-openshift/openshift/openshift-steps.md
2. Ansible Automation Platform configured with steps mentioned here llama-on-openshift/AAP/aap-readme.md

Step 1: Trigger the Workflow 

Here 
I. Run the ❌ Break Apache job template. This inserts an invalid directive in Apache config and restarts the service.

II. Go to Automation Decisions(Event-Driven Ansible) → Rulebook Activations. Confirm EDA(Event-Driven Ansible) picked up the event.

III. Go to Automation Controller → Jobs. Confirm "AI Insights and Lightspeed prompt generation" workflow execution. When the workflow completes you will see a green ✅ Success.

IV. Go to Templates and you should be able to see a new job template called "🧠 Lightspeed Remediation Playbook Generator" generated. 

V. Head over to slack and check the notification you received. Here’s what to look for:

   🛑 HTTPD Error Logs: These logs were automatically collected from the webserver.

   🧠 AI Insights (RCA): Red Hat AI parsed the logs and generated a root cause analysis. These insights help you understand exactly why the failure occurred.

This is AIOps in action! Logs are sent to Slack so the concerned team can take action, a ticket appears with an RCA already included, and a prompt is ready for Lightspeed to generate the fix.

We’ve completed steps 1, 2, and 3 of the architecture and are now moving on to steps 4, 5, and 6.




Step 2 - Remediation Workflow

Login to Openshift Container Platform using the credentials.

Got to Networking-> Routes

Click on the route next to Streamlit. This is your LLamastack UI.

In UI select  Tools, select mcp:aap under MCP Servers and increate max token to atleast 2000

Now you can interact with the AAP MCP server:

Give the following prompts in sequence:


1. List the most recent Event.

The response will be something like this.

   llama-on-openshift/images/llamastack-ui-1.png


2. Next give this prompt: "Return the LLM Prompt generated"

The response will be something like this.

   llama-on-openshift/images/llamastack-ui-2.png

3. Refresh before executing the below prompt as the underlying LLM of LLamastack may hallucinate due to limited context length. 

After refreshing give the below prompt:


Using the prompt generated above ask LLamastack to do this

      Run a Lightspeed job template with ID 19 with extra_vars
      {
      "lightspeed_prompt": "Remove the invalid directive 'InvalidDirectiveHere' from the httpd configuration file. Then restart the httpd service. Execute against node 1 host"
      }
      and then give the generated playbook


The above prompt is same as the one returned from llamastack as depitcted in response 2, except I am adding "Execute agains node 1". Make sure you add this in the prompt since the http service went down on Node 1, so the playbook should be run agains node 1.

4. Finally give this prompt

Run Remediation Workflow  Template  extra_vars is 

{ "lightspeed_playbook": <cleaned_yaml> }


5. Finally run this prompt to fix the issue:

   Run a job template by name Execute HTTPD Remediation