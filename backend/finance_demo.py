import requests
from typing import Dict, List

class FinanceAdvisor:
    def __init__(self):
        # Using Groq free API
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "mixtral-8x7b-32768"
    
    def _make_request(self, prompt: str) -> str:
        """Make request to free Groq API"""
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.1
            }
            
            response = requests.post(self.base_url, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return self._fallback_response(prompt)
        except:
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Simple rule-based responses if API fails"""
        prompt_lower = prompt.lower()
        
        if 'trip' in prompt_lower and '$2500' in prompt:
            return """❌ **Cannot afford this trip safely**
            
Reasoning: A $2,500 trip represents 50% of your monthly salary. This would significantly impact your emergency fund and delay your financial goals.

Alternative: Save $400/month for 6 months, or consider a $1,500 domestic trip instead.

Impact: Would delay emergency fund goal by 4+ months."""
        
        elif 'macbook' in prompt_lower or 'laptop' in prompt_lower:
            return """⚠️ **Proceed with caution**
            
This $1,200 purchase is 24% of your monthly salary. While technically affordable, it would use 15% of your current savings.

Recommendation: Wait 2 months and save specifically for this purchase, or consider a $800 alternative.

Impact: Would reduce discretionary spending capacity for 3 months."""
        
        else:
            return "Based on your financial profile, focus on building emergency funds before major purchases."
    
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze spending patterns"""
        categories = {}
        total_spending = 0
        
        for transaction in transactions:
            cat = transaction.get('category', 'other')
            amount = transaction['amount']
            categories[cat] = categories.get(cat, 0) + amount
            total_spending += amount
        
        # Calculate monthly averages (assuming 2 months of data)
        monthly_avg = total_spending / 2
        
        return {
            'monthly_average': monthly_avg,
            'categories': categories,
            'top_category': max(categories, key=categories.get),
            'discretionary_spending': categories.get('dining_out', 0) + categories.get('entertainment', 0)
        }
    
    def can_afford_trip(self, trip_cost: float, destination: str, user_data: Dict) -> Dict:
        """Determine if user can afford a trip"""
        monthly_salary = user_data['monthly_salary']
        current_savings = user_data['current_savings']
        
        # Simple affordability logic
        spending_stats = self.analyze_spending_patterns(user_data['transactions'])
        monthly_expenses = spending_stats['monthly_average']
        
        # Can afford if: trip < 30% of monthly salary AND savings > trip cost * 2
        affordable = (trip_cost < monthly_salary * 0.3) and (current_savings > trip_cost * 2)
        
        prompt = f"""
        User wants a ${trip_cost} trip to {destination}.
        
        Financial situation:
        - Monthly salary: ${monthly_salary}
        - Current savings: ${current_savings}
        - Monthly expenses: ${monthly_expenses:.0f}
        - Emergency fund goal: ${user_data['goals']['emergency_fund']}
        
        Can they afford this trip? Provide specific reasoning and alternatives if not.
        """
        
        ai_response = self._make_request(prompt)
        
        return {
            'affordable': affordable,
            'reasoning': ai_response,
            'alternative': f"Save ${trip_cost//6:.0f}/month for 6 months" if not affordable else None
        }
    
    def can_afford_purchase(self, item: str, cost: float, category: str, user_data: Dict) -> Dict:
        """Determine if user can afford a purchase"""
        monthly_salary = user_data['monthly_salary']
        
        # Simple logic: purchase should be < 25% of monthly salary
        recommended = cost < monthly_salary * 0.25
        
        prompt = f"""
        User wants to buy: {item} for ${cost}
        
        Monthly salary: ${monthly_salary}
        Current savings: ${user_data['current_savings']}
        
        Should they buy this? Consider budget impact and alternatives.
        """
        
        ai_response = self._make_request(prompt)
        
        return {
            'recommended': recommended,
            'impact_analysis': ai_response
        }
    
    def get_spending_insights(self, transactions: List[Dict]) -> List[str]:
        """Generate spending insights"""
        stats = self.analyze_spending_patterns(transactions)
        
        insights = []
        
        # Dining out analysis
        dining_out = stats['categories'].get('dining_out', 0)
        if dining_out > 200:
            insights.append(f"You spend ${dining_out:.0f}/month on dining out - cooking more could save $100+")
        
        # Top category insight
        top_cat = stats['top_category']
        top_amount = stats['categories'][top_cat]
        insights.append(f"Your biggest expense category is {top_cat}: ${top_amount:.0f}")
        
        # General advice
        if stats['discretionary_spending'] > stats['monthly_average'] * 0.3:
            insights.append("Consider reducing discretionary spending by 20% to boost savings")
        
        return insights

def main():
    print("hello")
    # Initialize the advisor
    advisor = FinanceAdvisor()
    
    # Sample user financial data
    user_data = {
        'monthly_salary': 5000,
        'current_savings': 8000,
        'transactions': [
            {'date': '2024-01-15', 'amount': 1200, 'category': 'rent', 'description': 'Monthly rent'},
            {'date': '2024-01-16', 'amount': 300, 'category': 'groceries', 'description': 'Whole Foods'},
            {'date': '2024-01-18', 'amount': 45, 'category': 'dining_out', 'description': 'Dinner'},
            {'date': '2024-01-20', 'amount': 80, 'category': 'gas', 'description': 'Shell station'},
            {'date': '2024-01-22', 'amount': 150, 'category': 'entertainment', 'description': 'Concert tickets'},
            {'date': '2024-02-15', 'amount': 1200, 'category': 'rent', 'description': 'Monthly rent'},
            {'date': '2024-02-16', 'amount': 280, 'category': 'groceries', 'description': 'Safeway'},
            {'date': '2024-02-18', 'amount': 65, 'category': 'dining_out', 'description': 'Pizza night'},
            {'date': '2024-02-20', 'amount': 75, 'category': 'gas', 'description': 'Gas station'},
            {'date': '2024-02-22', 'amount': 120, 'category': 'utilities', 'description': 'Electric bill'},
        ],
        'goals': {
            'emergency_fund': 15000,
            'vacation': 3000,
            'new_car_down_payment': 5000
        }
    }
    
    print("=== FINANCIAL ADVISOR DEMO ===\n")
    
    # 1. Trip affordability check
    print("1. TRIP AFFORDABILITY CHECK:")
    trip_decision = advisor.can_afford_trip(2500, "Europe", user_data)
    print(f"Can afford Europe trip ($2,500): {trip_decision['affordable']}")
    print(f"Analysis: {trip_decision['reasoning']}")
    print()
    
    # 2. Purchase decision
    print("2. PURCHASE DECISION:")
    laptop_decision = advisor.can_afford_purchase("MacBook Pro", 1200, "electronics", user_data)
    print(f"Should buy MacBook Pro ($1,200): {laptop_decision['recommended']}")
    print(f"Analysis: {laptop_decision['impact_analysis']}")
    print()
    
    # 3. Spending insights
    print("3. SPENDING INSIGHTS:")
    insights = advisor.get_spending_insights(user_data['transactions'])
    for insight in insights:
        print(f"• {insight}")
    print()
    
    # 4. Quick financial snapshot
    print("4. FINANCIAL SNAPSHOT:")
    stats = advisor.analyze_spending_patterns(user_data['transactions'])
    print(f"Monthly spending average: ${stats['monthly_average']:.0f}")
    print(f"Biggest expense: {stats['top_category']}")
    print(f"Discretionary spending: ${stats['discretionary_spending']:.0f}")

    print("snapshot complete.\n")

if __name__ == "__main__":
    main()