TRIP_AFFORDABILITY_PROMPT = """
User wants to take a ${trip_cost} trip to {destination}.

Financial Profile:
- Monthly salary: ${monthly_salary}
- Average monthly expenses: ${avg_expenses}
- Current savings: ${current_savings}
- Emergency fund: ${emergency_fund}
- Recent spending trends: {spending_trends}
- Financial goals: {goals}

Analyze:
1. Can they afford this trip without financial stress?
2. What's the opportunity cost?
3. How would this impact their emergency fund/goals?
4. Alternative options (cheaper trip, delay, payment plan)?
5. What would they need to cut back on?

Be realistic and specific about the financial impact.
"""

PURCHASE_DECISION_PROMPT = """
User wants to buy: {item} for ${cost}

Current situation:
- Monthly disposable income: ${disposable}
- This month's discretionary spending: ${spent_this_month}
- Category budget ({category}): ${category_budget}
- Recent similar purchases: {recent_purchases}

Should they buy this? Consider:
- Budget impact
- Necessity vs want
- Alternative options
- Timing considerations
"""