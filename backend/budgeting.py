from typing import Dict, List
from datetime import datetime, timedelta

def create_realistic_budget(salary: float, spending_history: List[Dict], goals: Dict) -> Dict:
    """Create budget based on actual spending patterns, not idealistic percentages"""
    
    # Analyze current spending
    categories = {}
    for transaction in spending_history:
        cat = transaction.get('category', 'other')
        categories[cat] = categories.get(cat, 0) + transaction['amount']
    
    # Average monthly amounts
    months = len(set(t['date'][:7] for t in spending_history))  # YYYY-MM format
    monthly_categories = {cat: total/months for cat, total in categories.items()}
    
    # Create realistic budget (not 50/30/20 rule, but based on actual behavior)
    essential_categories = ['rent', 'utilities', 'groceries', 'insurance', 'debt_payments']
    essential_total = sum(monthly_categories.get(cat, 0) for cat in essential_categories)
    
    discretionary_total = salary - essential_total
    savings_capacity = max(0, discretionary_total * 0.3)  # 30% of discretionary income
    
    return {
        'monthly_salary': salary,
        'essential_expenses': essential_total,
        'discretionary_budget': discretionary_total - savings_capacity,
        'savings_target': savings_capacity,
        'category_budgets': monthly_categories,
        'goals_timeline': calculate_goals_timeline(goals, savings_capacity)
    }

def track_budget_performance(budget: Dict, actual_spending: List[Dict]) -> Dict:
    """Compare actual vs budgeted spending"""
    
    current_month_spending = {}
    current_month = datetime.now().strftime('%Y-%m')
    
    for transaction in actual_spending:
        if transaction['date'].startswith(current_month):
            cat = transaction.get('category', 'other')
            current_month_spending[cat] = current_month_spending.get(cat, 0) + transaction['amount']
    
    performance = {}
    for category, budgeted in budget['category_budgets'].items():
        actual = current_month_spending.get(category, 0)
        performance[category] = {
            'budgeted': budgeted,
            'actual': actual,
            'difference': budgeted - actual,
            'percentage_used': (actual / budgeted * 100) if budgeted > 0 else 0,
            'status': 'over' if actual > budgeted else 'under'
        }
    
    return performance

def suggest_budget_adjustments(performance: Dict, user_goals: Dict) -> List[str]:
    """Suggest realistic budget changes based on actual behavior"""
    suggestions = []
    
    # Find categories consistently over budget
    over_budget = [cat for cat, data in performance.items() 
                   if data['status'] == 'over' and data['percentage_used'] > 120]
    
    if over_budget:
        suggestions.append(f"You're consistently overspending on: {', '.join(over_budget)}")
        suggestions.append("Consider increasing these budgets or finding specific ways to reduce spending")
    
    # Find categories with room to optimize
    under_budget = [cat for cat, data in performance.items() 
                    if data['status'] == 'under' and data['percentage_used'] < 80]
    
    if under_budget:
        suggestions.append(f"You have room in: {', '.join(under_budget)}")
        suggestions.append("Consider reallocating this money to savings or debt payments")
    
    return suggestions

def calculate_goals_timeline(goals: Dict, monthly_savings_capacity: float) -> Dict:
    """Calculate realistic timelines for financial goals"""
    timelines = {}
    
    for goal_name, target_amount in goals.items():
        if monthly_savings_capacity > 0:
            months_needed = target_amount / monthly_savings_capacity
            timelines[goal_name] = {
                'target_amount': target_amount,
                'monthly_savings_needed': monthly_savings_capacity,
                'months_to_goal': round(months_needed, 1),
                'target_date': (datetime.now() + timedelta(days=months_needed * 30)).strftime('%Y-%m')
            }
        else:
            timelines[goal_name] = {
                'target_amount': target_amount,
                'status': 'Need to reduce expenses first to create savings capacity'
            }
    
    return timelines