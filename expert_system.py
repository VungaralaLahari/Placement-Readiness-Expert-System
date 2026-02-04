import pandas as pd
import numpy as np

class PlacementExpertSystem():

    def __init__(self):
        self.past_data = self.load_past_data()
        self.base_weights = {
            'cgpa': 19,
            'leetcode': 18,
            'cdc_band': 17,
            'github': 9,
            'weekly_problems': 10,
            'certificates': 11,
            'projects': 14,
            'internships': 20,
            'backlogs': 16,
            'mock_interviews': 7
        }

    def load_past_data(self):
        rng = np.random.default_rng(42)
        data = pd.DataFrame({
            'branch': ['MECH','ECE','EEE','IT','CSE','CSM','CSD','CSC']*20,
            'cgpa': rng.normal(7.5, 0.6, 160),
            'leetcode': rng.normal(160, 30, 160),
            'projects': rng.poisson(1.5, 160),
            'weekly_problems': rng.normal(10, 2, 160),
        })
        return data

    def adjust_weights(self, branch, cgpa):
        weights = self.base_weights.copy()

        if branch in ['MECH','ECE','EEE','IT']:
            weights['cgpa'] -= 2
            weights['leetcode'] -= 10
            weights['projects'] += 2
            weights['weekly_problems'] -= 4

        elif branch in ['CSE','CSM','CSD','CSC']:
            weights['cgpa'] += 1
            weights['leetcode'] += 10
            weights['projects'] += 2
            weights['weekly_problems'] += 6

        if cgpa < 7.0:
            weights['cgpa'] += 7
            weights['backlogs'] += 5

        return {k: min(25, v) for k, v in weights.items()}

    def cdc_band_score(self, band):
        band_scores = {'A': 100, 'B': 80, 'C': 65, 'D': 45}
        messages = {'A': 'Excellent', 'B': 'Good', 'C': 'Average', 'D': 'Poor'}
        return band_scores.get(band.upper(), 50), messages.get(band.upper(), 'Invalid')

    def risk_assessment(self, data):
        risk = []
        if data['cdc_band'] in ['C','D']:
            risk.append("Low CDC band limits opportunities")
        if data['backlogs'] > 0:
            risk.append("Backlogs reduce eligibility")
        if data['weekly_problems'] < 4:
            risk.append("Inconsistent coding practice")
        if data['projects'] == 0:
            risk.append("No projects weakens resume")
        return risk

    def smart_score(self, actual, benchmark, weight):
        if actual >= benchmark * 1.1:
            return weight * 110, "Excellent"
        elif actual >= benchmark:
            return weight * 100, "Good"
        else:
            gap = (benchmark - actual) / benchmark
            score = weight * (1 - gap * 0.7)
            return score, "Needs Improvement"

    def personalized_report(self, weak_areas, data):
        plan = []
        for metric, score, weight in weak_areas:
            if metric == 'cgpa':
                plan.append("Improve CGPA with focused subject revision")
            elif metric == 'backlogs':
                plan.append("Clear backlogs immediately to restore eligibility")
            elif metric == 'leetcode':
                plan.append("Increase DSA practice consistency")
            elif metric == 'projects':
                plan.append("Build at least one end-to-end project")
            elif metric == 'weekly_problems':
                plan.append("Solve coding problems weekly without breaks")
            elif metric == 'cdc_band':
                plan.append("Improve CDC band via mocks and assessments")
        return plan

    def analysis_report(self, data):
        branch = data['branch'].upper()
        self.past_data = self.load_past_data()

        branch_data = self.past_data[self.past_data['branch'] == branch]
        if branch_data.empty:
            branch_data = self.past_data[self.past_data['branch'] == 'CSE']

        benchmarks = {
            'cgpa': branch_data['cgpa'].mean(),
            'leetcode': branch_data['leetcode'].mean(),
            'projects': branch_data['projects'].mean(),
            'weekly_problems': branch_data['weekly_problems'].mean()
        }

        weights = self.adjust_weights(branch, data['cgpa'])
        scores = {}
        explanations = {}

        for metric in ['cgpa','leetcode','weekly_problems','projects']:
            scores[metric], explanations[metric] = self.smart_score(
                data[metric], benchmarks[metric], weights[metric]
            )

        cdc_score, cdc_msg = self.cdc_band_score(data['cdc_band'])
        scores['cdc_band'] = weights['cdc_band'] * (cdc_score / 100)
        explanations['cdc_band'] = cdc_msg

        scores['backlogs'] = weights['backlogs'] * 100 if data['backlogs'] == 0 else weights['backlogs'] * (50 / (data['backlogs'] + 1))
        explanations['backlogs'] = "Clear" if data['backlogs'] == 0 else "Pending"

        scores['internships'] = weights['internships'] * 100 if data['internships'] > 0 else 40
        explanations['internships'] = "Done" if data['internships'] > 0 else "Missing"

        github_commits = data.get('github_commits', 0)
        scores['github'] = weights['github'] * min(100, github_commits / 25 * 100)
        explanations['github'] = str(github_commits)

        certs = data.get('certs', 0)
        scores['certificates'] = weights['certificates'] * min(100, certs * 50)
        explanations['certificates'] = str(certs)

        mocks = data.get('mocks', 0)
        scores['mock_interviews'] = weights['mock_interviews'] * min(100, mocks / 10 * 100)
        explanations['mock_interviews'] = str(mocks)

        total_score = sum(scores.values())

        def determine_status(scores, data):
            risk_points = 0

            if data['projects'] == 0:
                risk_points += 2
            if data['backlogs'] > 0:
                risk_points += min(3, data['backlogs'])
            if data['cdc_band'] in ['C','D']:
                risk_points += 2
            if data['weekly_problems'] < 5:
                risk_points += 1
            if data['leetcode'] < 50:
                risk_points += 1

            total = sum(scores.values())

            if risk_points >= 6:
                return "HIGH RISK"
            if total >= 1200 and risk_points <= 2:
                return "READY"
            if total >= 900:
                return "IMPROVE"
            return "HIGH RISK"

        status = determine_status(scores, data)

        weak_areas = [
            (k, v, weights.get(k, 0))
            for k, v in scores.items()
            if v < weights.get(k, 0) * 0.65
        ]

        weak_areas = sorted(weak_areas, key=lambda x: (x[2] - x[1]), reverse=True)[:5]

        return {
            'branch': branch,
            'total_score': total_score,
            'status': status,
            'scores': scores,
            'explanations': explanations,
            'benchmark': benchmarks,
            'weights': weights,
            'weak_areas': weak_areas,
            'risks': self.risk_assessment(data),
            'action_plan': self.personalized_report(weak_areas, data)
        }
