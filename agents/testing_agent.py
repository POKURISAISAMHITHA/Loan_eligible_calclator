"""
Testing Agent - Automated Quality Assurance
Validates loan decisions, monitors system behavior, and ensures accuracy
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class TestingAgent:
    """
    Automated Testing Agent that validates loan decisions and system behavior.
    
    Responsibilities:
    - Validate loan decision accuracy
    - Check for bias and fairness
    - Monitor agent performance
    - Detect anomalies in decisions
    - Generate test reports
    """
    
    def __init__(self):
        self.name = "Testing Agent"
        self.test_history: List[Dict] = []
        self.anomaly_threshold = 0.15  # 15% deviation triggers alert
        
        # Expected decision patterns for validation
        self.validation_rules = {
            "high_income_low_loan": {
                "condition": lambda app: app["income"] > 100000 and app["loan_amount"] < app["income"] * 2,
                "expected_decision": "APPROVED",
                "confidence_min": 0.85
            },
            "low_income_high_loan": {
                "condition": lambda app: app["income"] < 40000 and app["loan_amount"] > app["income"] * 5,
                "expected_decision": "REJECTED",
                "confidence_min": 0.80
            },
            "poor_repayment_score": {
                "condition": lambda app: app["repayment_score"] < 0.50,
                "expected_decision": "REJECTED",
                "confidence_min": 0.90
            },
            "excellent_repayment_score": {
                "condition": lambda app: app["repayment_score"] > 0.90 and app["existing_loans"] <= 1,
                "expected_decision": "APPROVED",
                "confidence_min": 0.85
            },
            "high_debt_ratio": {
                "condition": lambda app: (app["loan_amount"] / app["income"]) > 6,
                "expected_decision": "REJECTED",
                "confidence_min": 0.75
            }
        }
    
    def analyze(self, application: Dict[str, Any], decision_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a loan decision for accuracy and fairness.
        
        Args:
            application: The loan application data
            decision_result: The decision made by the orchestrator
            
        Returns:
            Dictionary containing test results and validation status
        """
        test_id = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Extract decision details
        final_decision = decision_result.get("final_decision", "UNKNOWN")
        confidence = decision_result.get("confidence_score", 0.0)
        
        # Run validation checks
        validation_results = self._validate_decision(application, final_decision, confidence)
        
        # Check for bias
        bias_check = self._check_bias(application, decision_result)
        
        # Analyze agent performance
        agent_performance = self._analyze_agent_performance(decision_result)
        
        # Detect anomalies
        anomaly_detection = self._detect_anomalies(application, decision_result)
        
        # Calculate overall test score
        test_score = self._calculate_test_score(
            validation_results, 
            bias_check, 
            agent_performance, 
            anomaly_detection
        )
        
        # Generate test report
        test_report = {
            "test_id": test_id,
            "timestamp": datetime.now().isoformat(),
            "application_id": application.get("name", "Unknown"),
            "final_decision": final_decision,
            "confidence_score": confidence,
            "validation": validation_results,
            "bias_check": bias_check,
            "agent_performance": agent_performance,
            "anomaly_detection": anomaly_detection,
            "test_score": test_score,
            "passed": test_score >= 0.70,  # 70% threshold for passing
            "recommendations": self._generate_recommendations(
                validation_results, 
                bias_check, 
                anomaly_detection
            )
        }
        
        # Store in history
        self.test_history.append(test_report)
        
        return test_report
    
    def _validate_decision(self, application: Dict, decision: str, confidence: float) -> Dict:
        """Validate if the decision matches expected patterns"""
        validations = []
        passed_rules = 0
        total_rules = 0
        
        for rule_name, rule in self.validation_rules.items():
            if rule["condition"](application):
                total_rules += 1
                expected = rule["expected_decision"]
                min_confidence = rule["confidence_min"]
                
                decision_match = decision == expected
                confidence_match = confidence >= min_confidence if decision == expected else True
                
                passed = decision_match and confidence_match
                if passed:
                    passed_rules += 1
                
                validations.append({
                    "rule": rule_name,
                    "expected_decision": expected,
                    "actual_decision": decision,
                    "expected_confidence": min_confidence,
                    "actual_confidence": confidence,
                    "passed": passed,
                    "reason": self._get_validation_reason(decision_match, confidence_match)
                })
        
        accuracy = (passed_rules / total_rules * 100) if total_rules > 0 else 100.0
        
        return {
            "passed_rules": passed_rules,
            "total_rules": total_rules,
            "accuracy": accuracy,
            "validations": validations,
            "status": "PASS" if accuracy >= 80 else "FAIL"
        }
    
    def _check_bias(self, application: Dict, decision_result: Dict) -> Dict:
        """Check for potential bias in decision-making"""
        bias_indicators = []
        bias_score = 1.0  # Start with no bias (1.0 = fair)
        
        # Check income bias
        income = application.get("income", 0)
        loan_amount = application.get("loan_amount", 0)
        dti_ratio = loan_amount / income if income > 0 else 0
        
        # Check if decision seems biased against lower income
        if income < 50000 and dti_ratio < 3 and decision_result.get("final_decision") == "REJECTED":
            bias_indicators.append({
                "type": "POTENTIAL_INCOME_BIAS",
                "severity": "MEDIUM",
                "description": "Low income applicant rejected despite reasonable DTI ratio"
            })
            bias_score -= 0.15
        
        # Check employment years bias
        employment_years = application.get("employment_years", 0)
        if employment_years >= 5 and decision_result.get("final_decision") == "REJECTED":
            # Check if rejection is reasonable
            repayment_score = application.get("repayment_score", 0)
            if repayment_score > 0.70:
                bias_indicators.append({
                    "type": "POTENTIAL_EXPERIENCE_BIAS",
                    "severity": "LOW",
                    "description": "Experienced applicant with good repayment rejected"
                })
                bias_score -= 0.10
        
        # Check for consistency in similar applications
        similar_decisions = self._check_consistency(application, decision_result)
        if similar_decisions["inconsistency_detected"]:
            bias_indicators.append({
                "type": "INCONSISTENCY_DETECTED",
                "severity": "HIGH",
                "description": similar_decisions["description"]
            })
            bias_score -= 0.20
        
        # Calculate fairness score (0-100%)
        fairness_score = max(0, bias_score * 100)
        
        return {
            "fairness_score": fairness_score,
            "bias_indicators": bias_indicators,
            "bias_detected": len(bias_indicators) > 0,
            "status": "FAIR" if fairness_score >= 80 else "REVIEW_NEEDED"
        }
    
    def _analyze_agent_performance(self, decision_result: Dict) -> Dict:
        """Analyze performance of individual agents"""
        agent_results = decision_result.get("agent_results", {})
        
        performance_metrics = {
            "agents_analyzed": len(agent_results),
            "agent_scores": {},
            "average_confidence": 0.0,
            "consensus_strength": 0.0
        }
        
        confidences = []
        decisions = []
        
        for agent_name, result in agent_results.items():
            decision = result.get("decision", "UNKNOWN")
            confidence = result.get("confidence", 0.0)
            
            confidences.append(confidence)
            decisions.append(decision)
            
            performance_metrics["agent_scores"][agent_name] = {
                "decision": decision,
                "confidence": confidence,
                "performance": "GOOD" if confidence >= 0.70 else "NEEDS_REVIEW"
            }
        
        if confidences:
            performance_metrics["average_confidence"] = sum(confidences) / len(confidences)
        
        # Calculate consensus (how much agents agree)
        if decisions:
            most_common = max(set(decisions), key=decisions.count)
            consensus = decisions.count(most_common) / len(decisions)
            performance_metrics["consensus_strength"] = consensus
        
        return performance_metrics
    
    def _detect_anomalies(self, application: Dict, decision_result: Dict) -> Dict:
        """Detect anomalies in the decision process"""
        anomalies = []
        
        # Check for extreme confidence with weak reasoning
        confidence = decision_result.get("confidence_score", 0)
        reasoning = decision_result.get("reasoning", "")
        
        if confidence > 0.95 and len(reasoning) < 100:
            anomalies.append({
                "type": "HIGH_CONFIDENCE_WEAK_REASONING",
                "severity": "MEDIUM",
                "description": "Very high confidence but insufficient reasoning provided"
            })
        
        # Check for contradictory agent decisions
        agent_results = decision_result.get("agent_results", {})
        decisions = [r.get("decision") for r in agent_results.values()]
        
        if len(set(decisions)) == len(decisions) and len(decisions) > 3:
            anomalies.append({
                "type": "NO_AGENT_CONSENSUS",
                "severity": "HIGH",
                "description": "All agents provided different decisions"
            })
        
        # Check for unusual application patterns
        income = application.get("income", 0)
        loan_amount = application.get("loan_amount", 0)
        collateral = application.get("collateral_value", 0)
        
        if loan_amount > income * 10 and decision_result.get("final_decision") == "APPROVED":
            anomalies.append({
                "type": "EXTREME_DTI_APPROVED",
                "severity": "HIGH",
                "description": f"Loan amount {loan_amount} is >10x income {income} but approved"
            })
        
        if collateral > 0 and collateral < loan_amount * 0.5 and decision_result.get("final_decision") == "APPROVED":
            anomalies.append({
                "type": "INSUFFICIENT_COLLATERAL",
                "severity": "MEDIUM",
                "description": "Collateral less than 50% of loan amount"
            })
        
        return {
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "risk_level": self._calculate_risk_level(anomalies),
            "requires_review": len(anomalies) > 0
        }
    
    def _check_consistency(self, application: Dict, decision_result: Dict) -> Dict:
        """Check if decision is consistent with similar past applications"""
        # This is a simplified version - in production, would use ML similarity
        inconsistency = False
        description = "No similar cases found for comparison"
        
        # Check recent history for similar cases
        similar_cases = [
            test for test in self.test_history[-20:]  # Last 20 tests
            if self._is_similar_application(application, test)
        ]
        
        if similar_cases:
            current_decision = decision_result.get("final_decision")
            similar_decisions = [case.get("final_decision") for case in similar_cases]
            
            # If most similar cases had different decisions, flag inconsistency
            different_decisions = sum(1 for d in similar_decisions if d != current_decision)
            if different_decisions > len(similar_decisions) / 2:
                inconsistency = True
                description = f"Decision differs from {different_decisions}/{len(similar_cases)} similar cases"
        
        return {
            "inconsistency_detected": inconsistency,
            "description": description,
            "similar_cases_found": len(similar_cases)
        }
    
    def _is_similar_application(self, app1: Dict, app2: Dict) -> bool:
        """Check if two applications are similar (simplified)"""
        # Compare key metrics with 20% tolerance
        tolerance = 0.20
        
        for key in ["income", "loan_amount", "repayment_score"]:
            val1 = app1.get(key, 0)
            val2 = app2.get(key, 0)
            
            if val1 > 0 and val2 > 0:
                diff = abs(val1 - val2) / val1
                if diff > tolerance:
                    return False
        
        return True
    
    def _calculate_test_score(self, validation: Dict, bias: Dict, 
                             performance: Dict, anomalies: Dict) -> float:
        """Calculate overall test score (0-1)"""
        # Weighted scoring
        validation_score = validation.get("accuracy", 0) / 100 * 0.35
        bias_score = bias.get("fairness_score", 0) / 100 * 0.30
        performance_score = performance.get("average_confidence", 0) * 0.20
        anomaly_score = (1 - (anomalies.get("anomalies_detected", 0) * 0.1)) * 0.15
        
        total_score = validation_score + bias_score + performance_score + max(0, anomaly_score)
        return round(total_score, 3)
    
    def _calculate_risk_level(self, anomalies: List[Dict]) -> str:
        """Calculate risk level based on anomalies"""
        if not anomalies:
            return "LOW"
        
        high_severity = sum(1 for a in anomalies if a.get("severity") == "HIGH")
        medium_severity = sum(1 for a in anomalies if a.get("severity") == "MEDIUM")
        
        if high_severity >= 2:
            return "CRITICAL"
        elif high_severity >= 1:
            return "HIGH"
        elif medium_severity >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_validation_reason(self, decision_match: bool, confidence_match: bool) -> str:
        """Get reason for validation result"""
        if decision_match and confidence_match:
            return "Decision and confidence match expected pattern"
        elif not decision_match:
            return "Decision does not match expected pattern"
        else:
            return "Confidence level below expected threshold"
    
    def _generate_recommendations(self, validation: Dict, bias: Dict, anomalies: Dict) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []
        
        # Validation recommendations
        if validation.get("accuracy", 100) < 80:
            recommendations.append(
                "REVIEW: Decision accuracy below 80%. Review validation rules and agent logic."
            )
        
        # Bias recommendations
        if bias.get("fairness_score", 100) < 80:
            recommendations.append(
                "BIAS_ALERT: Potential bias detected. Review decision for fairness and consistency."
            )
        
        # Anomaly recommendations
        for anomaly in anomalies.get("anomalies", []):
            if anomaly.get("severity") == "HIGH":
                recommendations.append(
                    f"URGENT: {anomaly.get('type')} - {anomaly.get('description')}"
                )
        
        # Performance recommendations
        if not recommendations:
            recommendations.append("PASSED: All tests passed. Decision appears valid.")
        
        return recommendations
    
    def get_test_statistics(self) -> Dict:
        """Get overall testing statistics"""
        if not self.test_history:
            return {
                "total_tests": 0,
                "message": "No tests run yet"
            }
        
        total_tests = len(self.test_history)
        passed_tests = sum(1 for test in self.test_history if test.get("passed", False))
        
        avg_test_score = sum(test.get("test_score", 0) for test in self.test_history) / total_tests
        avg_fairness = sum(test.get("bias_check", {}).get("fairness_score", 0) 
                          for test in self.test_history) / total_tests
        
        total_anomalies = sum(test.get("anomaly_detection", {}).get("anomalies_detected", 0) 
                             for test in self.test_history)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "average_test_score": round(avg_test_score, 3),
            "average_fairness_score": round(avg_fairness, 2),
            "total_anomalies_detected": total_anomalies,
            "status": "HEALTHY" if avg_test_score >= 0.80 else "NEEDS_ATTENTION"
        }
    
    def generate_test_report(self) -> str:
        """Generate a formatted test report"""
        stats = self.get_test_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           TESTING AGENT - QUALITY ASSURANCE REPORT           ║
╚══════════════════════════════════════════════════════════════╝

📊 Overall Statistics:
   • Total Tests Run: {stats.get('total_tests', 0)}
   • Passed: {stats.get('passed_tests', 0)}
   • Failed: {stats.get('failed_tests', 0)}
   • Pass Rate: {stats.get('pass_rate', 0):.1f}%

🎯 Performance Metrics:
   • Average Test Score: {stats.get('average_test_score', 0):.3f}
   • Average Fairness Score: {stats.get('average_fairness_score', 0):.2f}%
   • Anomalies Detected: {stats.get('total_anomalies_detected', 0)}

✅ System Status: {stats.get('status', 'UNKNOWN')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report
