"""
Testing Dashboard
Interactive dashboard for viewing test results and system health
"""
import sys
from pathlib import Path
from typing import List, Dict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.testing_agent import TestingAgent
from tests.test_data_generator import TestDataGenerator
from orchestrator import LoanOrchestrator
from models import LoanApplication


class TestingDashboard:
    """Interactive testing dashboard for monitoring system quality"""
    
    def __init__(self):
        self.testing_agent = TestingAgent()
        self.orchestrator = LoanOrchestrator()
        self.data_generator = TestDataGenerator()
        self.test_results: List[Dict] = []
    
    def run_test_suite(self, test_count: int = 20):
        """Run a comprehensive test suite"""
        print(f"\n{'='*70}")
        print(f"🧪 RUNNING TEST SUITE - {test_count} Applications")
        print(f"{'='*70}\n")
        
        # Generate test applications
        print("📊 Generating test data...")
        applications = self.data_generator.generate_batch(
            count=test_count,
            profile_distribution={
                "strong": 0.30,
                "moderate": 0.40,
                "weak": 0.25,
                "edge_case": 0.05
            }
        )
        
        print(f"✓ Generated {len(applications)} test applications\n")
        
        # Process each application
        print("🔄 Processing applications...")
        for i, app_data in enumerate(applications, 1):
            app = LoanApplication(**app_data)
            
            # Process through orchestrator
            result = self.orchestrator.process_application(app)
            
            # Validate with testing agent
            test_report = self.testing_agent.analyze(app_data, result)
            
            self.test_results.append({
                "application": app_data,
                "decision_result": result,
                "test_report": test_report
            })
            
            # Progress indicator
            if i % 5 == 0:
                print(f"   Processed {i}/{test_count} applications...")
        
        print(f"✓ Completed processing\n")
        
        # Display results
        self.display_results()
    
    def display_results(self):
        """Display test results in a formatted dashboard"""
        if not self.test_results:
            print("No test results available. Run test suite first.")
            return
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["test_report"]["passed"])
        failed_tests = total_tests - passed_tests
        
        # Decision distribution
        decisions = [r["decision_result"]["final_decision"] for r in self.test_results]
        approved = decisions.count("APPROVED")
        rejected = decisions.count("REJECTED")
        conditional = decisions.count("CONDITIONAL")
        
        # Average scores
        avg_confidence = sum(r["decision_result"]["confidence_score"] for r in self.test_results) / total_tests
        avg_test_score = sum(r["test_report"]["test_score"] for r in self.test_results) / total_tests
        avg_fairness = sum(r["test_report"]["bias_check"]["fairness_score"] for r in self.test_results) / total_tests
        
        # Anomalies
        total_anomalies = sum(r["test_report"]["anomaly_detection"]["anomalies_detected"] 
                             for r in self.test_results)
        
        # Display dashboard
        print(f"\n{'='*70}")
        print(f"📊 TESTING DASHBOARD - COMPREHENSIVE RESULTS")
        print(f"{'='*70}\n")
        
        # Overview section
        print(f"{'▶ OVERVIEW':<50}")
        print(f"{'─'*70}")
        print(f"  Total Tests Run:          {total_tests}")
        print(f"  Tests Passed:             {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"  Tests Failed:             {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"  Status:                   {'✓ HEALTHY' if passed_tests/total_tests >= 0.80 else '⚠ NEEDS ATTENTION'}")
        print()
        
        # Decision distribution
        print(f"{'▶ DECISION DISTRIBUTION':<50}")
        print(f"{'─'*70}")
        print(f"  Approved:                 {approved} ({approved/total_tests*100:.1f}%)")
        print(f"  Rejected:                 {rejected} ({rejected/total_tests*100:.1f}%)")
        print(f"  Conditional:              {conditional} ({conditional/total_tests*100:.1f}%)")
        print()
        
        # Quality metrics
        print(f"{'▶ QUALITY METRICS':<50}")
        print(f"{'─'*70}")
        print(f"  Average Confidence Score: {avg_confidence:.3f}")
        print(f"  Average Test Score:       {avg_test_score:.3f}")
        print(f"  Average Fairness Score:   {avg_fairness:.1f}%")
        print(f"  Total Anomalies Detected: {total_anomalies}")
        print()
        
        # Failed tests details
        if failed_tests > 0:
            print(f"{'▶ FAILED TESTS DETAILS':<50}")
            print(f"{'─'*70}")
            
            failed_list = [r for r in self.test_results if not r["test_report"]["passed"]]
            for i, failed in enumerate(failed_list[:5], 1):  # Show first 5
                app_name = failed["application"]["name"]
                decision = failed["decision_result"]["final_decision"]
                test_score = failed["test_report"]["test_score"]
                
                print(f"  {i}. {app_name}")
                print(f"     Decision: {decision} | Test Score: {test_score:.3f}")
                
                # Show recommendations
                for rec in failed["test_report"]["recommendations"][:2]:
                    print(f"     → {rec}")
                print()
            
            if failed_tests > 5:
                print(f"  ... and {failed_tests - 5} more failed tests\n")
        
        # Bias and fairness issues
        biased_tests = [r for r in self.test_results 
                       if r["test_report"]["bias_check"]["bias_detected"]]
        
        if biased_tests:
            print(f"{'▶ BIAS & FAIRNESS ALERTS':<50}")
            print(f"{'─'*70}")
            print(f"  Tests with Bias Indicators: {len(biased_tests)}\n")
            
            for i, biased in enumerate(biased_tests[:3], 1):  # Show first 3
                app_name = biased["application"]["name"]
                fairness_score = biased["test_report"]["bias_check"]["fairness_score"]
                indicators = biased["test_report"]["bias_check"]["bias_indicators"]
                
                print(f"  {i}. {app_name} (Fairness: {fairness_score:.1f}%)")
                for indicator in indicators:
                    print(f"     [{indicator['severity']}] {indicator['type']}")
                print()
        
        # High-risk anomalies
        high_risk_tests = [r for r in self.test_results 
                          if r["test_report"]["anomaly_detection"]["risk_level"] in ["HIGH", "CRITICAL"]]
        
        if high_risk_tests:
            print(f"{'▶ HIGH-RISK ANOMALIES':<50}")
            print(f"{'─'*70}")
            print(f"  High-Risk Tests: {len(high_risk_tests)}\n")
            
            for i, risky in enumerate(high_risk_tests[:3], 1):
                app_name = risky["application"]["name"]
                risk_level = risky["test_report"]["anomaly_detection"]["risk_level"]
                anomalies = risky["test_report"]["anomaly_detection"]["anomalies"]
                
                print(f"  {i}. {app_name} (Risk: {risk_level})")
                for anomaly in anomalies:
                    print(f"     [{anomaly['severity']}] {anomaly['type']}")
                    print(f"     {anomaly['description']}")
                print()
        
        print(f"{'='*70}\n")
    
    def run_fairness_test(self):
        """Run fairness and bias testing"""
        print(f"\n{'='*70}")
        print(f"⚖️  FAIRNESS & BIAS TESTING")
        print(f"{'='*70}\n")
        
        print("Generating similar application pairs...")
        applications = self.data_generator.generate_fairness_test_batch()
        
        print(f"Processing {len(applications)} applications...\n")
        
        fairness_results = []
        
        for app_data in applications:
            app = LoanApplication(**app_data)
            result = self.orchestrator.process_application(app)
            test_report = self.testing_agent.analyze(app_data, result)
            
            fairness_results.append({
                "application": app_data,
                "decision": result["final_decision"],
                "fairness_score": test_report["bias_check"]["fairness_score"],
                "bias_indicators": test_report["bias_check"]["bias_indicators"]
            })
        
        # Analyze consistency
        print(f"{'▶ CONSISTENCY ANALYSIS':<50}")
        print(f"{'─'*70}")
        
        # Group similar applications
        for i in range(0, len(fairness_results), 2):
            if i + 1 < len(fairness_results):
                app1 = fairness_results[i]
                app2 = fairness_results[i + 1]
                
                print(f"\n  Pair {i//2 + 1}:")
                print(f"    App 1: {app1['decision']} (Fairness: {app1['fairness_score']:.1f}%)")
                print(f"    App 2: {app2['decision']} (Fairness: {app2['fairness_score']:.1f}%)")
                
                if app1['decision'] != app2['decision']:
                    print(f"    ⚠️  INCONSISTENCY DETECTED - Similar apps, different decisions!")
                else:
                    print(f"    ✓ Consistent decisions")
        
        # Overall fairness score
        avg_fairness = sum(r['fairness_score'] for r in fairness_results) / len(fairness_results)
        total_bias = sum(len(r['bias_indicators']) for r in fairness_results)
        
        print(f"\n{'▶ OVERALL FAIRNESS METRICS':<50}")
        print(f"{'─'*70}")
        print(f"  Average Fairness Score:    {avg_fairness:.1f}%")
        print(f"  Total Bias Indicators:     {total_bias}")
        print(f"  Status:                    {'✓ FAIR' if avg_fairness >= 85 else '⚠ REVIEW NEEDED'}")
        print(f"\n{'='*70}\n")
    
    def run_stress_test(self, count: int = 50):
        """Run stress test with many applications"""
        print(f"\n{'='*70}")
        print(f"💪 STRESS TESTING - {count} Applications")
        print(f"{'='*70}\n")
        
        import time
        
        applications = self.data_generator.generate_stress_test_batch(count)
        
        start_time = time.time()
        success_count = 0
        error_count = 0
        
        print("Processing applications...")
        for i, app_data in enumerate(applications, 1):
            try:
                app = LoanApplication(**app_data)
                result = self.orchestrator.process_application(app)
                success_count += 1
                
                if i % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = i / elapsed
                    print(f"  Processed {i}/{count} ({rate:.1f} apps/sec)")
            
            except Exception as e:
                error_count += 1
                print(f"  ERROR on application {i}: {str(e)}")
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / count
        throughput = count / total_time
        
        print(f"\n{'▶ STRESS TEST RESULTS':<50}")
        print(f"{'─'*70}")
        print(f"  Total Applications:        {count}")
        print(f"  Successful:                {success_count}")
        print(f"  Errors:                    {error_count}")
        print(f"  Total Time:                {total_time:.2f} seconds")
        print(f"  Average Time/App:          {avg_time:.3f} seconds")
        print(f"  Throughput:                {throughput:.1f} applications/second")
        print(f"  Status:                    {'✓ PASSED' if error_count == 0 else '⚠ ERRORS DETECTED'}")
        print(f"\n{'='*70}\n")
    
    def export_results(self, filename: str = "test_results.json"):
        """Export test results to file"""
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"✓ Exported {len(self.test_results)} test results to {filename}")
    
    def interactive_menu(self):
        """Interactive menu for the testing dashboard"""
        while True:
            print(f"\n{'='*70}")
            print(f"🧪 TESTING DASHBOARD - INTERACTIVE MENU")
            print(f"{'='*70}")
            print("\n1. Run Standard Test Suite (20 applications)")
            print("2. Run Large Test Suite (50 applications)")
            print("3. Run Fairness & Bias Testing")
            print("4. Run Stress Test (100 applications)")
            print("5. Display Current Results")
            print("6. Export Results to JSON")
            print("7. Clear Results")
            print("8. Exit")
            print(f"\n{'─'*70}")
            
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == "1":
                self.run_test_suite(test_count=20)
            elif choice == "2":
                self.run_test_suite(test_count=50)
            elif choice == "3":
                self.run_fairness_test()
            elif choice == "4":
                self.run_stress_test(count=100)
            elif choice == "5":
                self.display_results()
            elif choice == "6":
                filename = input("Enter filename (default: test_results.json): ").strip()
                if not filename:
                    filename = "test_results.json"
                self.export_results(filename)
            elif choice == "7":
                self.test_results = []
                self.testing_agent = TestingAgent()  # Reset
                print("✓ Results cleared")
            elif choice == "8":
                print("\n👋 Exiting Testing Dashboard\n")
                break
            else:
                print("Invalid option. Please select 1-8.")


def main():
    """Main function for running the testing dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Loan Approval System Testing Dashboard")
    parser.add_argument("--mode", choices=["standard", "fairness", "stress", "interactive"],
                       default="interactive", help="Testing mode")
    parser.add_argument("--count", type=int, default=20, help="Number of test applications")
    parser.add_argument("--export", type=str, help="Export results to file")
    
    args = parser.parse_args()
    
    dashboard = TestingDashboard()
    
    if args.mode == "interactive":
        dashboard.interactive_menu()
    elif args.mode == "standard":
        dashboard.run_test_suite(test_count=args.count)
        if args.export:
            dashboard.export_results(args.export)
    elif args.mode == "fairness":
        dashboard.run_fairness_test()
    elif args.mode == "stress":
        dashboard.run_stress_test(count=args.count)


if __name__ == "__main__":
    main()
