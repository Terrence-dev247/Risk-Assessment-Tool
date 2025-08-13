import json
import numpy as np
from pymcdm.methods import TOPSIS
from pymcdm.weights import equal_weights
import re

class RiskAssessor:
    """
    A class to perform automated risk assessment for data science projects
    using a Multi-Criteria Decision-Making (MCDM) method.
    """
    def __init__(self, risk_data_path=r"C:\Users\Tebogo-LT\.vscode\codes\.vscode\Risk folder\risks.json"):
        self.risk_data_path = risk_data_path
        self.risks = self._load_risk_data()
        self.next_risk_id = self._get_next_risk_id()
        self._calculate_severity_all()  # Update severity based on scores

    def _load_risk_data(self):
        try:
            with open(self.risk_data_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: The file '{self.risk_data_path}' was not found.")
            return []
        
        risks_list = []
        for category in data.get("risk_categories", []):
            for risk in category.get("risks", []):
                risk["category_name"] = category.get("category_name")
                risks_list.append(risk)
        return risks_list

    def _get_next_risk_id(self):
        if not self.risks:
            return 1
        max_id = 0
        for risk in self.risks:
            num_match = re.findall(r'\d+', risk.get('risk_id', ''))
            if num_match:
                max_id = max(max_id, int(num_match[-1]))
        return max_id + 1

    def _calculate_severity_all(self):
        """
        Calculate severity based on likelihood * impact:
        Score >= 16: High
        Score >= 8 and <16: Medium
        Score < 8: Low
        """
        for risk in self.risks:
            score = risk["likelihood_score"] * risk["impact_score"]
            if score >= 16:
                risk["severity"] = "High"
            elif score >= 8:
                risk["severity"] = "Medium"
            else:
                risk["severity"] = "Low"

    def add_custom_risk(self, description, likelihood, impact):
        new_risk = {
            "risk_id": f"CUST_{self.next_risk_id}",
            "description": description,
            "likelihood_score": likelihood,
            "impact_score": impact,
            "category_name": "User-Defined"
        }
        score = likelihood * impact
        if score >= 16:
            new_risk["severity"] = "High"
        elif score >= 8:
            new_risk["severity"] = "Medium"
        else:
            new_risk["severity"] = "Low"

        self.risks.append(new_risk)
        self.next_risk_id += 1
        print(f"\nNew risk '{description}' has been added.")

    def _create_decision_matrix(self):
        if not self.risks:
            return np.array([]), np.array([])
        matrix = np.array([
            [risk["likelihood_score"], risk["impact_score"]]
            for risk in self.risks
        ])
        criteria_types = np.array([1, 1])  # Higher scores mean more risk
        return matrix, criteria_types

    def assess_project_risks(self):
        if not self.risks:
            print("No risk data available for assessment.")
            return []
        matrix, criteria_types = self._create_decision_matrix()
        topsis = TOPSIS()  # Uses Euclidean distance by default
        weights = equal_weights(matrix)
        preferences = topsis(matrix, weights, criteria_types)
        ranked_risks = sorted(
            zip(self.risks, preferences),
            key=lambda x: x[1],
            reverse=True
        )
        return ranked_risks


if __name__ == "__main__":
    project_assessor = RiskAssessor()
    
    print("Do you want to add a new risk to the assessment? (yes/no)")
    if input().strip().lower() == 'yes':
        risk_description = input("Enter a description for the new risk: ")
        likelihood = int(input("Enter likelihood score (1-5): "))
        impact = int(input("Enter impact score (1-5): "))
        project_assessor.add_custom_risk(risk_description, likelihood, impact)

    ranked_risks = project_assessor.assess_project_risks()
    
    if ranked_risks:
        print("\n--- Automated Risk Assessment Report ---")
        print("---------------------------------------")
        for i, (risk, score) in enumerate(ranked_risks):
            print(f"Rank {i + 1}:")
            print(f"  Score (TOPSIS Preference): {score:.4f}")
            print(f"  Risk ID: {risk.get('risk_id')}")
            print(f"  Description: {risk.get('description')}")
            print(f"  Category: {risk.get('category_name')}")
            print(f"  Likelihood: {risk.get('likelihood_score')}")
            print(f"  Impact: {risk.get('impact_score')}")
            print(f"  Severity: {risk.get('severity')}")
            print("-" * 30)
    else:
        print("Risk assessment could not be performed.")
