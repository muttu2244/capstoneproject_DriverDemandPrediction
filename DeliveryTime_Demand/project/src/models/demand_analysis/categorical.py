"""Category-based demand analysis."""
import pandas as pd
from typing import Dict, Any

class CategoryAnalyzer:
    def analyze(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze category-based demand patterns."""
        return {
            'restaurant_type': self._analyze_restaurant_types(data),
            'food_category': self._analyze_food_categories(data),
            'order_value': self._analyze_order_values(data)
        }
    
    def _analyze_restaurant_types(self, data: pd.DataFrame) -> Dict[str, Any]:
        restaurant_stats = data.groupby('restaurant_type')['order_count'].agg(['mean', 'std']).to_dict()
        return {'type_stats': restaurant_stats}
    
    def _analyze_food_categories(self, data: pd.DataFrame) -> Dict[str, Any]:
        category_stats = data.groupby('food_category')['order_count'].agg(['mean', 'std']).to_dict()
        return {'category_stats': category_stats}
    
    def _analyze_order_values(self, data: pd.DataFrame) -> Dict[str, Any]:
        # Create value ranges
        data['value_range'] = pd.qcut(data['order_value'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        value_stats = data.groupby('value_range')['order_count'].agg(['mean', 'std']).to_dict()
        return {'value_stats': value_stats}