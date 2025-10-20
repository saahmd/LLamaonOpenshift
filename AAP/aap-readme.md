As mentioned this demo is based out on a catalog item available on RHDP

So first step go to RHDP and order this catalog item https://catalog.demo.redhat.com/catalog?search=ai+driven&item=babylon-catalog-prod%2Fsandboxes-gpte.ai-driven-ansible-automation.prod
Order the catalog item with default values

Once the catalog item is ready head over to the lab

1) Login to Ansible Automation Platform using the credentials.

2) Go to Automation Execution → Project

3) Click Create Project. Fill in the details:

    Parameter	    Value
    Name            MyProject

    Organization    Default

    Source Control Type     Git

    Source Control URL      https://github.com/saahmd/LLamaonOpenshift.git

4) Go to Automation Execution → Project and check the status of MyProject. It should be Success.


5) Go to Automation Execution → Templates.

3)  Create "Get Lightspeed Prompt" Template

    I. Click Create Job Template. Fill in the details:

            Parameter	    Value
            Name            Get Lightspeed Prompt

            Inventory       Demo Inventory

            Project         MyProject

            Playbook        playbooks/aap_create_job_template.yml 

            Credentials     AAP
    
    II. Click "Create job Template" button below.


4)  Create "Send Report to Slack" Template

    I. Click Create Job Template. Fill in the details:

            Parameter	            Value
            Name                    Send Report to Slack

            Inventory               Demo Inventory

            Project                 MyProject

            Playbook                playbooks/send_report_slack.yml 

            Credentials             AAP

            Extra variables         slack_token: "<YOUR SLACK TOKEN>"

    II. Click "Create job Template" button below.


5) Next, Go to Automation Execution → Templates. Click Create template → Create     Workflow job template.

4) Fill in the details:
    
    Parameter	    Value
    Name            AI Insights and Lightspeed prompt generation

    Organization    Default

5) Click Create workflow job template.

6) You’ll see the empty workflow visualizer.

7) Click Add Step button and fill in the below details:


    Parameter	            Value

    Node type               Job Template

    Job Template            ⚙️ Apache Service Status Check

    Convergence             Any

    Node alias              (You can leave this blank)


8) Click Next, then Finish.

9) Visual after first node:

        llama-on-openshift/images/ai-insights-workflow1.png


10) Add RHEL AI: Analyze Incident step:

    I. Click on the three dots (⋮ kebab menu) next to the ⚙️ Apache Service Status Check node.

    II. Click on ⊕ Add step and link to insert the next node into the workflow.

            Parameter	    Value

            Node type       Job Template

            Job Template    🤖 RHEL AI: Analyze Incident

            Status          Run on success

            Convergence     Any

            Node alias      (You can leave this blank)


    III. Click Next, then Finish.

    Workflow with two nodes:

        llama-on-openshift/images/ai-insights-workflow2.png

11) Add "Get Lightspeed Prompt" Template

    I. Click on the three dots (⋮ kebab menu) next to the 🤖 RHEL AI: Analyze Incident node.

    II. Click on ⊕ Add step and link to insert the next node into the workflow.

        Parameter	    Value
        
        Node type       Job Template

        Job Template    Get Lightspeed Prompt

        Status          Run on success

        Convergence     Any
    
        Node alias      (You can leave this blank)

    III. Click Next, then Finish.

Workflow with three nodes:

    llama-on-openshift/images/ai-insights-workflow3.png


12) Add "Send Report to Slack" Template

    I. Click on the three dots (⋮ kebab menu) next to the 🤖 RHEL AI: Analyze Incident node.

    II. Click on ⊕ Add step and link to insert the next node into the workflow.

        Parameter	    Value
        
        Node type       Job Template

        Job Template    Send Report to Slack

        Status          Run on success

        Convergence     Any
    
        Node alias      (You can leave this blank)

    III. Click Next, then Finish.



    Final workflow visual:

        llama-on-openshift/images/ai-insights-final-workflow.png


17) Click Save to finalize.


### Create Remediation Workflow 

1) Log in to the web UI for Ansible Automation Platform if you are not already logged in.

2) In the left navigation menu, click on Automation Execution → Templates.

3) Click Create template → Create workflow job template.

4) Fill in the details:
    Parameter	    Value
    Name            Remediation Workflow

5) Select Prompt on Launch Checkbox.

6) Click "Save workflow job template".

6) You’ll see the empty workflow visualizer.

7) Click on the blue Add step. 

    I. Fill out the following values

        Parameter	    Value
        Node type       Job Template

        Job Template    🧾 Commit Fix to Gitea

        Convergence     Any

        Node alias      (You can leave this blank)


    II. Click on the blue Next. Review and click the blue Finish button

    Your workflow will now look like this:

        llama-on-openshift/images/remediation-1.png


8) Add "Project Sync" Node

    I. Click on the three dots (kebab menu) next to the 🧾 Commit Fix to Gitea

    II. Click on ⊕ Add step and link. Fill out the following values

        Parameter	    Value
        Node type       Project Sync

        Job Template    Lightspeed-Playbooks

        Status          Run on success

        Convergence     Any

        Node alias      (You can leave this blank)

    III. Click on the blue Next.

    IV. Review and click the blue Finish button.

        Your workflow will now look like this:

            llama-on-openshift/images/remediation-2.png

11) Add "⚙️ Build HTTPD Remediation Template" Node

    I. Click on the three dots (kebab menu) next to the 🧾 Commit Fix to Gitea

    II. Click on ⊕ Add step and link. Fill out the following values

        Parameter	    Value
        Node type       Job Template

        Job Template    ⚙️ Build HTTPD Remediation Template

        Status          Run on success

        Convergence     Any

        Node alias      (You can leave this blank)

    III. Click on the blue Next.

    IV. Review and click the blue Finish button.

    Your workflow will now look like this:
    
        llama-on-openshift/images/remediation-3.png