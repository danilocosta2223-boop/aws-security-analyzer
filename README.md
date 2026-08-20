# 🛡️ AWS Security Analyzer

> Ferramenta desenvolvida em Python para auditoria de segurança em ambientes AWS, permitindo identificar riscos, avaliar conformidade e gerar relatórios executivos automatizados em múltiplos formatos.

Projeto desenvolvido para demonstrar conhecimentos em Python, AWS, Cloud Security, automação de auditorias e geração de relatórios executivos.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![AWS](https://img.shields.io/badge/AWS-Boto3-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Objetivo

O **AWS Security Analyzer** foi desenvolvido para automatizar auditorias de segurança em ambientes AWS, identificando vulnerabilidades, desvios de conformidade e riscos operacionais.

A ferramenta gera relatórios executivos e técnicos para apoiar equipes de Cloud, Segurança da Informação e Governança na tomada rápida de decisões e remediação de falhas.

---

## 🏗️ Arquitetura

```text
AWS Account
│
▼
AWS Security Analyzer (Multi-threading / Multi-region)
│
├── IAM Check
├── S3 Check
└── EC2 (Security Groups) Check
│
▼
Risk Engine (Score & Severity Validation)
│
▼
Relatórios Automáticos (JSON | Excel | PDF | HTML)