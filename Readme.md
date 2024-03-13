# Camunda 8 Process Instance Overview

## Introduction
This document explains the concept of a "Process Instance" in Camunda 8, essential for understanding how processes are executed within the engine.

## What is a Process Instance?
A Process Instance represents a single execution of a process. Each time a process is triggered, a new instance is created. This instance follows the defined BPMN model, executing tasks and making decisions as per the process design.

## Lifecycle of a Process Instance
- **Start:** Triggered by an event, API call, or manually.
- **Execution:** Moves through the BPMN elements (tasks, gateways) as defined.
- **End:** Completes once the end event is reached.

## Monitoring Process Instances
Camunda 8's Operate interface allows users to monitor and manage live and historical instances, providing insights into performance and potential issues.

## Use Cases
- **Order Processing:** Each order triggers a new instance, handling the sequence of validation, payment, and shipment.
- **Customer Onboarding:** New customer sign-ups instantiate a process for verification, account setup, and welcome communication.

For further details, refer to [Camunda's process instance documentation](https://docs.camunda.io).

