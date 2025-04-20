# sorter/utils/job_titles.py

# Defines the available job titles and their associated required skills.
# Structure: Dictionary where keys are job title strings,
#            and values are lists of required skill strings (lowercase recommended).
# Note: This list is representative and skills can vary greatly by company and role level.
job_titles = {
    # --- Software Development ---
    "Software Engineer": ["python", "java", "c#", ".net", "go", "ruby", "sql", "nosql", "algorithms", "data structures", "git", "docker", "testing"],
    "Frontend Developer": ["html", "css", "javascript", "typescript", "react", "angular", "vue", "svelte", "sass", "less", "webpack", "babel", "responsive design", "git", "browser apis"],
    "Backend Developer": ["python", "java", "c#", "node.js", "go", "ruby", "php", "django", "flask", "spring boot", "asp.net", "express.js", "rest api", "graphql", "sql", "nosql", "mongodb", "postgresql", "redis", "rabbitmq", "kafka", "docker", "kubernetes", "aws", "azure", "gcp", "git", "microservices"],
    "Web Developer (Full Stack)": ["html", "css", "javascript", "typescript", "react", "angular", "vue", "node.js", "python", "django", "java", "spring boot", "sql", "mongodb", "rest api", "git", "docker", "cloud basics"],
    "Mobile Developer (Android)": ["java", "kotlin", "android sdk", "android studio", "xml layouts", "jetpack compose", "sqlite", "firebase", "rest api", "git", "mvvm", "mvc"],
    "Mobile Developer (iOS)": ["swift", "objective-c", "ios sdk", "xcode", "uikit", "swiftui", "core data", "realm", "firebase", "rest api", "git", "mvc", "mvvm"],
    "Game Developer": ["c++", "c#", "unity", "unreal engine", "game physics", "graphics programming", "opengl", "directx", "vulkan", "blender", "3d math"],
    "Embedded Systems Engineer": ["c", "c++", "python", "microcontrollers", "rtos", "linux kernel", "device drivers", "hardware debugging", "arm architecture", "iot"],

    # --- Data & AI ---
    "Data Analyst": ["sql", "python", "r", "excel", "tableau", "power bi", "qlik sense", "data visualization", "statistics", "data cleaning", "etl", "reporting", "google analytics"],
    "Data Scientist": ["python", "r", "sql", "pandas", "numpy", "scipy", "scikit-learn", "tensorflow", "pytorch", "keras", "machine learning", "deep learning", "statistics", "probability", "data modeling", "big data", "spark", "hadoop", "jupyter notebooks", "data visualization"],
    "Data Engineer": ["python", "java", "scala", "sql", "nosql", "etl", "elt", "data warehousing", "data modeling", "spark", "hadoop", "kafka", "airflow", "aws", "azure", "gcp", "databricks", "snowflake", "docker", "kubernetes"],
    "Machine Learning Engineer (ML Engineer)": ["python", "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy", "machine learning algorithms", "deep learning", "nlp", "computer vision", "mlops", "docker", "kubernetes", "aws sagemaker", "azure ml", "gcp ai platform", "sql"],
    "AI Engineer": ["python", "deep learning", "machine learning", "nlp", "computer vision", "tensorflow", "pytorch", "hugging face", "transformers", "reinforcement learning", "keras", "opencv", "docker", "cloud platforms (aws/azure/gcp)"],
    "Business Intelligence (BI) Developer": ["sql", "etl", "data warehousing", "power bi", "tableau", "qlik", "ssis", "ssrs", "ssas", "data modeling", "reporting", "dax", "mdx"],

    # --- Infrastructure & Operations ---
    "DevOps Engineer": ["ci/cd", "jenkins", "gitlab ci", "github actions", "docker", "kubernetes", "terraform", "ansible", "chef", "puppet", "aws", "azure", "gcp", "scripting (python, bash, powershell)", "linux", "networking basics", "monitoring (prometheus, grafana, datadog)", "logging (elk stack)"],
    "Cloud Engineer": ["aws", "azure", "gcp", "terraform", "docker", "kubernetes", "iam", "cloud networking", "cloud security", "serverless", "scripting (python, bash)", "linux", "windows server"],
    "Site Reliability Engineer (SRE)": ["python", "go", "linux", "kubernetes", "docker", "monitoring (prometheus, grafana)", "logging (elk)", "automation (ansible, terraform)", "networking", "distributed systems", "incident response", "performance tuning", "cloud platforms"],
    "Systems Administrator": ["linux (centos, ubuntu, red hat)", "windows server", "active directory", "scripting (bash, powershell, python)", "virtualization (vmware, hyper-v)", "networking basics (tcp/ip, dns, dhcp)", "backup and recovery", "monitoring"],
    "Network Engineer": ["cisco ios", "juniper junos", "routing (bgp, ospf, eigrp)", "switching", "firewalls (palo alto, cisco asa, fortinet)", "vpn", "load balancers (f5)", "tcp/ip", "dns", "dhcp", "network monitoring", "wireless networking"],
    "Database Administrator (DBA)": ["sql", "postgresql", "mysql", "oracle", "sql server", "mongodb", "database design", "performance tuning", "backup and recovery", "high availability", "disaster recovery", "scripting (sql, bash, python)"],

    # --- Security ---
    "Cybersecurity Analyst": ["siem (splunk, qradar, arcsight)", "ids/ips", "vulnerability scanning (nessus, qualys)", "endpoint security (edr)", "firewalls", "incident response", "threat intelligence", "network analysis (wireshark)", "basic scripting"],
    "Security Engineer": ["firewalls", "vpn", "ids/ips", "iam", "encryption", "cloud security (aws, azure, gcp)", "endpoint security", "security architecture", "scripting (python, bash)", "penetration testing concepts", "compliance (iso 27001, soc2, pci-dss)"],
    "Penetration Tester (Ethical Hacker)": ["kali linux", "metasploit", "burp suite", "nmap", "owasp top 10", "web application security", "network security", "scripting (python, bash, powershell)", "reverse engineering (optional)", "social engineering"],

    # --- Management, Architecture & Design ---
    "IT Project Manager": ["project management methodologies (agile, scrum, kanban, waterfall)", "jira", "confluence", "ms project", "smartsheet", "risk management", "stakeholder management", "budgeting", "communication", "pmp (certification)", "csm (certification)"],
    "Product Manager": ["product strategy", "product roadmap", "market research", "user stories", "agile methodologies", "jira", "data analysis", "a/b testing", "ui/ux principles", "communication", "stakeholder management"],
    "Scrum Master": ["scrum framework", "agile principles", "jira", "facilitation", "coaching", "conflict resolution", "servant leadership", " impediment removal", "csm/psm (certification)"],
    "Solutions Architect": ["system design", "cloud platforms (aws, azure, gcp)", "microservices architecture", "apis", "database design (sql/nosql)", "networking concepts", "security principles", "high availability", "disaster recovery", "communication", "specific domain knowledge (e.g., data, web, enterprise)"],
    "Enterprise Architect": ["togaf", "zachman framework", "archimate", "business architecture", "application architecture", "data architecture", "infrastructure architecture", "it strategy", "modeling tools", "stakeholder management"],
    "UI/UX Designer": ["user research", "wireframing", "prototyping", "figma", "sketch", "adobe xd", "invision", "user testing", "information architecture", "interaction design", "visual design", "design systems", "accessibility (wcag)"],
    "UX Researcher": ["user interviews", "surveys", "usability testing", "persona development", "journey mapping", "data analysis (qualitative & quantitative)", "heuristic evaluation", "competitive analysis"],

    # --- QA & Testing ---
    "QA Engineer (Manual Tester)": ["test planning", "test case design", "test execution", "bug tracking (jira, bugzilla)", "testing methodologies", "sql basics", "api testing concepts (postman)", "exploratory testing"],
    "Automation Test Engineer": ["selenium", "cypress", "playwright", "appium", "python", "java", "javascript", "test frameworks (pytest, junit, testng, jest)", "bdd (cucumber, behave)", "ci/cd integration", "api automation", "performance testing (jmeter, k6 - optional)", "sql"],

    # --- Specialized Roles ---
    "SAP Consultant": ["sap modules (fi, co, sd, mm, pp, hr, basis, etc.)", "abap (for technical roles)", "sap configuration", "business process knowledge", "integration", "s/4hana"],
    "Salesforce Developer": ["apex", "visualforce", "lightning web components (lwc)", "soql", "sosl", "salesforce platform", "rest/soap api", "integration", "salesforce dx", "git"],
    "Salesforce Administrator": ["salesforce configuration", "workflows", "process builder", "flow", "user management", "reports & dashboards", "data loader", "appexchange", "security model"],

    # Add more specialized roles like Network Security Engineer, Cloud Security Engineer, etc. if needed
}