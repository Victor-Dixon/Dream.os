"""
FastAPI Monitoring Module
V2 Compliant - <100 lines
"""

from prometheus_client import Counter, Histogram

# Metrics
requests_total = Counter('requests_total', 'Total requests')
response_time = Histogram('response_time', 'Response time')

def get_metrics():
    """Get monitoring metrics"""
    pass