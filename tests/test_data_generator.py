"""
Test Data Generator
Generates diverse test data for comprehensive testing
"""
import random
from typing import List, Dict, Any
from datetime import datetime


class TestDataGenerator:
    """Generate diverse loan application test data"""
    
    def __init__(self, seed: int = None):
        """Initialize generator with optional seed for reproducibility"""
        if seed:
            random.seed(seed)
        
        self.company_names = [
            "Tech Corp", "Finance Inc", "Retail Solutions", "Manufacturing Co",
            "Healthcare Systems", "Education Services", "Construction Ltd",
            "Restaurant Group", "Software Innovations", "Consulting Partners",
            "Energy Solutions", "Transportation Services", "Media Network",
            "Biotech Research", "Legal Associates", "Startup Ventures"
        ]
        
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
            "Linda", "William", "Elizabeth", "David", "Barbara", "Richard",
            "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
        ]
    
    def generate_application(self, profile_type: str = "random") -> Dict[str, Any]:
        """
        Generate a single loan application
        
        Args:
            profile_type: Type of applicant profile
                - "strong": High approval probability
                - "weak": High rejection probability
                - "moderate": Medium approval probability
                - "random": Random profile
                - "edge_case": Edge case testing
        
        Returns:
            Dictionary with loan application data
        """
        if profile_type == "strong":
            return self._generate_strong_profile()
        elif profile_type == "weak":
            return self._generate_weak_profile()
        elif profile_type == "moderate":
            return self._generate_moderate_profile()
        elif profile_type == "edge_case":
            return self._generate_edge_case_profile()
        else:
            return self._generate_random_profile()
    
    def generate_batch(self, count: int = 10, 
                      profile_distribution: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Generate a batch of loan applications
        
        Args:
            count: Number of applications to generate
            profile_distribution: Distribution of profile types
                Example: {"strong": 0.3, "moderate": 0.5, "weak": 0.2}
        
        Returns:
            List of loan application dictionaries
        """
        if profile_distribution is None:
            # Default distribution
            profile_distribution = {
                "strong": 0.25,
                "moderate": 0.45,
                "weak": 0.25,
                "edge_case": 0.05
            }
        
        # Normalize distribution
        total = sum(profile_distribution.values())
        normalized = {k: v/total for k, v in profile_distribution.items()}
        
        applications = []
        for _ in range(count):
            # Choose profile type based on distribution
            rand = random.random()
            cumulative = 0.0
            profile_type = "random"
            
            for ptype, prob in normalized.items():
                cumulative += prob
                if rand <= cumulative:
                    profile_type = ptype
                    break
            
            applications.append(self.generate_application(profile_type))
        
        return applications
    
    def _generate_strong_profile(self) -> Dict[str, Any]:
        """Generate a strong applicant profile (likely approval)"""
        return {
            "name": self._generate_name(),
            "income": random.uniform(90000, 180000),
            "loan_amount": random.uniform(100000, 300000),
            "existing_loans": random.randint(0, 2),
            "repayment_score": random.uniform(0.85, 0.98),
            "employment_years": random.uniform(5.0, 20.0),
            "company_name": random.choice(self.company_names),
            "collateral_value": random.uniform(200000, 500000)
        }
    
    def _generate_weak_profile(self) -> Dict[str, Any]:
        """Generate a weak applicant profile (likely rejection)"""
        income = random.uniform(25000, 45000)
        return {
            "name": self._generate_name(),
            "income": income,
            "loan_amount": random.uniform(income * 4, income * 8),  # High DTI
            "existing_loans": random.randint(3, 6),
            "repayment_score": random.uniform(0.30, 0.55),
            "employment_years": random.uniform(0.5, 2.5),
            "company_name": random.choice(self.company_names),
            "collateral_value": random.uniform(30000, 80000)
        }
    
    def _generate_moderate_profile(self) -> Dict[str, Any]:
        """Generate a moderate applicant profile (conditional/mixed)"""
        income = random.uniform(50000, 85000)
        return {
            "name": self._generate_name(),
            "income": income,
            "loan_amount": random.uniform(income * 2, income * 3.5),
            "existing_loans": random.randint(1, 3),
            "repayment_score": random.uniform(0.65, 0.80),
            "employment_years": random.uniform(2.5, 7.0),
            "company_name": random.choice(self.company_names),
            "collateral_value": random.uniform(100000, 250000)
        }
    
    def _generate_random_profile(self) -> Dict[str, Any]:
        """Generate a completely random profile"""
        income = random.uniform(25000, 200000)
        return {
            "name": self._generate_name(),
            "income": income,
            "loan_amount": random.uniform(50000, 500000),
            "existing_loans": random.randint(0, 6),
            "repayment_score": random.uniform(0.30, 0.98),
            "employment_years": random.uniform(0.5, 25.0),
            "company_name": random.choice(self.company_names),
            "collateral_value": random.uniform(0, 600000)
        }
    
    def _generate_edge_case_profile(self) -> Dict[str, Any]:
        """Generate edge case profiles for testing boundaries"""
        edge_type = random.choice([
            "zero_income",
            "extreme_dti",
            "perfect_score",
            "zero_collateral",
            "maximum_loans",
            "minimal_employment"
        ])
        
        if edge_type == "zero_income":
            return {
                "name": self._generate_name(),
                "income": 0.0,
                "loan_amount": 100000.0,
                "existing_loans": 0,
                "repayment_score": 0.80,
                "employment_years": 1.0,
                "company_name": random.choice(self.company_names),
                "collateral_value": 150000.0
            }
        
        elif edge_type == "extreme_dti":
            income = random.uniform(30000, 50000)
            return {
                "name": self._generate_name(),
                "income": income,
                "loan_amount": income * random.uniform(10, 20),  # Extreme DTI
                "existing_loans": random.randint(2, 4),
                "repayment_score": random.uniform(0.60, 0.75),
                "employment_years": random.uniform(2.0, 5.0),
                "company_name": random.choice(self.company_names),
                "collateral_value": random.uniform(50000, 100000)
            }
        
        elif edge_type == "perfect_score":
            return {
                "name": self._generate_name(),
                "income": 200000.0,
                "loan_amount": 150000.0,
                "existing_loans": 0,
                "repayment_score": 1.0,  # Perfect score
                "employment_years": 15.0,
                "company_name": random.choice(self.company_names),
                "collateral_value": 500000.0
            }
        
        elif edge_type == "zero_collateral":
            return {
                "name": self._generate_name(),
                "income": random.uniform(60000, 90000),
                "loan_amount": random.uniform(150000, 250000),
                "existing_loans": random.randint(1, 2),
                "repayment_score": random.uniform(0.70, 0.85),
                "employment_years": random.uniform(3.0, 8.0),
                "company_name": random.choice(self.company_names),
                "collateral_value": 0.0  # No collateral
            }
        
        elif edge_type == "maximum_loans":
            return {
                "name": self._generate_name(),
                "income": random.uniform(70000, 100000),
                "loan_amount": random.uniform(100000, 200000),
                "existing_loans": 10,  # Many existing loans
                "repayment_score": random.uniform(0.60, 0.75),
                "employment_years": random.uniform(5.0, 10.0),
                "company_name": random.choice(self.company_names),
                "collateral_value": random.uniform(150000, 250000)
            }
        
        else:  # minimal_employment
            return {
                "name": self._generate_name(),
                "income": random.uniform(40000, 70000),
                "loan_amount": random.uniform(100000, 180000),
                "existing_loans": random.randint(1, 3),
                "repayment_score": random.uniform(0.65, 0.80),
                "employment_years": 0.1,  # Just started
                "company_name": random.choice(self.company_names),
                "collateral_value": random.uniform(120000, 200000)
            }
    
    def _generate_name(self) -> str:
        """Generate a random name"""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        return f"{first} {last}"
    
    def generate_stress_test_batch(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate a large batch for stress testing"""
        return self.generate_batch(
            count=count,
            profile_distribution={
                "strong": 0.30,
                "moderate": 0.40,
                "weak": 0.25,
                "edge_case": 0.05
            }
        )
    
    def generate_fairness_test_batch(self) -> List[Dict[str, Any]]:
        """Generate applications to test for bias and fairness"""
        # Create pairs of similar applications to test consistency
        applications = []
        
        for _ in range(5):
            # Generate base profile
            base_income = random.uniform(50000, 100000)
            base_loan = base_income * random.uniform(2.0, 3.5)
            base_repayment = random.uniform(0.70, 0.85)
            
            # Create two nearly identical applications
            for i in range(2):
                applications.append({
                    "name": self._generate_name(),
                    "income": base_income * random.uniform(0.95, 1.05),  # Within 5%
                    "loan_amount": base_loan * random.uniform(0.95, 1.05),
                    "existing_loans": random.randint(1, 3),
                    "repayment_score": base_repayment * random.uniform(0.97, 1.03),
                    "employment_years": random.uniform(3.0, 7.0),
                    "company_name": random.choice(self.company_names),
                    "collateral_value": base_loan * random.uniform(1.1, 1.4)
                })
        
        return applications
    
    def save_to_file(self, applications: List[Dict[str, Any]], filename: str):
        """Save generated applications to JSON file"""
        import json
        
        with open(filename, 'w') as f:
            json.dump(applications, f, indent=2)
        
        print(f"Saved {len(applications)} applications to {filename}")
    
    def load_from_file(self, filename: str) -> List[Dict[str, Any]]:
        """Load applications from JSON file"""
        import json
        
        with open(filename, 'r') as f:
            applications = json.load(f)
        
        print(f"Loaded {len(applications)} applications from {filename}")
        return applications


# CLI interface for generating test data
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate test data for loan application system")
    parser.add_argument("--count", type=int, default=10, help="Number of applications to generate")
    parser.add_argument("--type", choices=["random", "strong", "weak", "moderate", "edge_case", "stress", "fairness"],
                       default="random", help="Type of test data")
    parser.add_argument("--output", type=str, help="Output file (JSON)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    generator = TestDataGenerator(seed=args.seed)
    
    if args.type == "stress":
        applications = generator.generate_stress_test_batch(args.count)
    elif args.type == "fairness":
        applications = generator.generate_fairness_test_batch()
    else:
        applications = generator.generate_batch(count=args.count)
    
    if args.output:
        generator.save_to_file(applications, args.output)
    else:
        import json
        print(json.dumps(applications, indent=2))
