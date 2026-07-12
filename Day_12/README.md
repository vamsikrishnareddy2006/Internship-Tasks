# Day 12 – Technical Case Study & Domain Research

**Project:** DevPulse — Developer Productivity & Code Quality Dashboard
**Track:** Track 3 – Deployment & Full-Stack Integration
**Internship:** Innolift Ventures
**Prepared by:** Vamsi Krishna Reddy Vemireddy
**Institution:** Vel Tech Rangarajan Dr. Sagunthala R&D Institute of Science and Technology

## Overview

Day 12 focuses on a technical case study and domain research report for DevPulse, an application that treats developer activity — commits, pull requests, code reviews, and static-analysis output — as measurable data, using machine learning to surface productivity and code-quality signals through a Flask + Chart.js dashboard.

## Contents of this Report

1. Domain Introduction
2. Industry Problems
3. Existing Solutions Analysis (SonarQube, Pluralsight Flow, Code Climate Quality)
4. Market Research
5. Flask Technology Study
6. Frontend Technology Study (HTML / CSS / JavaScript)
7. Database Study (SQLite)
8. Domain-Specific Technical Study
9. Machine Learning Research
10. System Design (Architecture, Workflow, ER Diagram)
11. Implementation Preview
12. References

## Domain

**Software Engineering Analytics / DevOps Intelligence** — applying data engineering and ML to the software development lifecycle, converting commits, PRs, and build/quality signals into productivity indices and risk flags for developers and engineering managers.

## Core Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Machine Learning:** scikit-learn (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM — compared via weighted F1-score and GridSearchCV)
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Deployment:** Gunicorn + Render

## Key Highlights

- Comparative analysis of existing tools (SonarQube, Pluralsight Flow, Code Climate Quality) and how DevPulse positions itself as a lightweight, self-hosted, ML-assisted alternative that unifies productivity and quality metrics in one dashboard.
- Full system design: layered architecture diagram, 7-step workflow (data capture → storage → request → inference → response → visualization → deployment), and a normalized SQLite schema with an ER diagram (`projects` → `developers` → `activity_records` → `predictions`).
- Machine learning pipeline: feature preprocessing, model comparison via GridSearchCV, model persistence with `joblib`, and a `/predict` Flask API returning class probabilities and confidence scores.
- Implementation preview mockups of the project overview dashboard and the live prediction interface.

## Deliverable

📄 [`DevPulse_Day12_Technical_Case_Study.pdf`](./DevPulse_Day12_Technical_Case_Study.pdf) — full technical case study and domain research report.
