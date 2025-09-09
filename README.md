# 🔍 Automated API Discovery and Fingerprinting

This repository contains Python automation for **discovering, extracting, and fingerprinting APIs** across **Postman** and **SwaggerHub**.  
It supports **dynamic doc scraping (Postman)**, **API pagination (SwaggerHub)**, and structured **JSON → CSV pipelines** with dataset enrichment for analysis.

---

## 📌 Features
- 🚀 Automated scraping of **Postman API docs** (Selenium for dynamic pages)  
- 📂 Export and parse **Postman collections** into structured CSV  
- 📊 Fetch and paginate through **SwaggerHub’s 700k+ APIs**  
- 🔧 Enrich datasets with **server & contact metadata**  
- 📑 Modular scripts with a unified **orchestrator**  

---

## 📂 Repository Structure

```text
api-discovery-fingerprinting/
│
├── postman/
│   ├── postman_discover_docs.py        # Selenium automation (dynamic docs)
│   ├── postman_export_collections.py   # Export Postman collections JSON
│   └── postman_parse_collections.py    # Parse JSON → CSV
│
├── swaggerhub/
│   ├── swaggerhub_fetch.py             # Fetch/paginate APIs
│   └── swaggerhub_enrich.py            # Add servers/contacts metadata
│
├── common/
│   ├── json_utils.py                   # Shared helper functions
│   └── config_base.py                  # Config/constants
│
├── scripts/
│   └── orchestrate_all.py              # Pipeline runner
│
├── samples/
│   └── responses.txt                   # Example API response output
│
├── docs/                               #  PDFs / PPTs
├── outputs/                            # Generated CSV/JSON (gitignored)
├── README.md
└── .gitignore

---
💡 Key Takeaways
Automating API discovery saves hundreds of hours of manual work.
Selenium enables extraction from JavaScript-heavy pages (Postman).
Structured CSV datasets enable cybersecurity & interoperability research.

---

## 🧑‍💻 Author

**Phranavh Sivaraman**  
Master of Cyber Security – API Security, Automation & OSINT Research  

- 📍 Melbourne, Australia  
- 🔗 [LinkedIn](https://www.linkedin.com/in/phranavhsivaraman/)  
- 💻 [GitHub](https://github.com/Phranavh28)  
- 📧 phranavh@gmail.com
