This project is an automated risk assessment tool for data science projects. It addresses the high failure rate of these projects by providing a structured, data-driven method for identifying and prioritizing potential risks.
The core of the tool is a Python script that uses the TOPSIS algorithm, a multi-criteria decision-making method. This algorithm evaluates and ranks a comprehensive list of risks based on two key factors:
 * Likelihood Score: How likely is the risk to occur?
 * Impact Score: How severe would the consequences be if the risk occurred?
The project's key components are:
 * A Python Script: This is the main application that loads risk data, performs the TOPSIS calculation, and generates a ranked report of the most critical risks.
 * A JSON Data File: This file serves as the project's database, containing a list of pre-defined risks categorized by area. It can be easily expanded or modified to fit specific project needs.
By using this tool, a project manager can move beyond subjective risk estimation and focus on mitigating the most critical threats to a project's success.
