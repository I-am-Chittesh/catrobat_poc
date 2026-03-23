# Catrobat IoT Middleware - Proof of Concept (PoC)

## Overview
This repository contains a lightweight Proof of Concept (PoC) developed in preparation for my Google Summer of Code application with Catrobat. 

The purpose of this code is to demonstrate the core safety routing logic and hallucination-catching middleware for the **Gemini-API Powered Intelligent Care Assistant**. 

## Core Features Demonstrated
* **Deterministic LLM Parsing:** Utilizes Pydantic for strict JSON schema validation, ensuring the Gemini API returns structured data, not open-ended chat text.
* **Safety Circuit Breaker:** Implements regex-based filtering to intercept and block unauthorized medical terminology before it reaches end-users.
* **Confidence Governance:** Automatically routes AI outputs to a Human-in-the-Loop (HITL) review queue if the model's calculated confidence score falls below 85% or if hardware anomalies are flagged.

*Note: This is a standalone architectural snippet created specifically to showcase the backend safety constraints proposed in the GSoC application.*
