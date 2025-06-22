import os
import requests
from typing import Dict, List, Optional, Any
from backend.analyzer import analyze_spending_patterns, calculate_disposable_income
from backend.decision_engine import can_afford_trip, can_afford_purchase
from backend.insights import generate_spending_insights
from backend.prompts import *

class FinanceAdvisor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            'x-api-key': self.api_key,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
    
    def _make_request(self, messages: List[Dict], model: str = "claude-3-sonnet-20240229") -> str:
        payload = {
            "model": model,
            "max_tokens": 1500,
            "messages": messages
        }
        response = requests.post(f"{self.base_url}/messages", headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
        return response.json()['content'][0]['text']
    
    def can_afford_trip(self, trip_cost: float, destination: str, user_data: Dict) -> Dict:
        return can_afford_trip(trip_cost, destination, user_data, self)
    
    def can_afford_purchase(self, item: str, cost: float, category: str, user_data: Dict) -> Dict:
        return can_afford_purchase(item, cost, category, user_data, self)
    
    def get_spending_insights(self, transactions: List[Dict]) -> List[str]:
        return generate_spending_insights(transactions, self)
    
    def analyze_user_finances(self, user_data: Dict) -> Dict:
        """Complete financial health analysis"""
        spending_stats = analyze_spending_patterns(user_data['transactions'])
        disposable = calculate_disposable_income(
            user_data['monthly_salary'], 
            spending_stats['fixed_expenses'],
            spending_stats['variable_avg']
        )
        insights = self.get_spending_insights(user_data['transactions'])
        
        return {
            'spending_stats': spending_stats,
            'disposable_income': disposable,
            'insights': insights,
            'financial_health_score': self._calculate_health_score(user_data, spending_stats)
        }