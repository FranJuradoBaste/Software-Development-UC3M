# 📘 G85.2025.T09.EG1 - UC3MMoney

This repository contains the **first assignment** of the course _Software Development_ (UC3M, 2025). The main objective of this initial exercise is to establish solid foundations for collaborative coding and to set up a consistent development environment that will be used throughout the project.

---

## 🎯 Objectives

This guided exercise aims to:

- Learn good practices of **collective code ownership**, which are essential when working on a project following **agile methodologies**.
- Establish a **coding standard** that is agreed upon and applied by the entire team, ensuring that all developers work in a consistent and coordinated manner.
- Apply the defined coding standard using a **tool integrated into the development environment**.

---

## 📁 Project Structure
```bash
G85.2025.T09.EG1-main/
├── Main.py
├── README.md
├── UC3MMoney/
│   ├── init.py
│   ├── transactionManagementException.py
│   ├── transactionRequest.py
│   └── transaction_manager.py
├── pylintrc
├── requirements.txt
└── test.json
```
---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/youruser/G85.2025.T09.EG1-main.git
cd G85.2025.T09.EG1-main
```
2.	Install the dependencies:
```bash
pip install -r requirements.txt
```
---
🚀 Execution

The entry point of the project is Main.py, which simulates basic transaction operations.

To run it:
```bash
python Main.py
```

You can also import and use the core classes directly from the UC3MMoney package.

---

🧪 Tests

The file test.json contains sample data used to test the system’s behavior.

In this first assignment, testing is mainly manual or functional, executed directly via examples.

---
🧰 Key Modules

transactionRequest.py: Defines the transaction request model.
transaction_manager.py: Handles transaction processing logic.
transactionManagementException.py: Manages custom exceptions.

---

👨‍💻 Authors

[Fran Jurado Basté]
Software Development - UC3M
Academic Year 2024/2025









