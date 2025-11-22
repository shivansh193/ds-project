from prometheus_client import Counter, Histogram, Gauge

# Metrics definitions
BOUNTIES_CREATED = Counter('decom_bounties_created_total', 'Total number of bounties created')
BOUNTIES_COMPLETED = Counter('decom_bounties_completed_total', 'Total number of bounties completed')
ACTIVE_WORKERS = Gauge('decom_active_workers', 'Number of currently active workers')
BID_PRICE = Histogram('decom_bid_price', 'Distribution of bid prices')
VERIFICATION_TIME = Histogram('decom_verification_seconds', 'Time taken to verify results')

def inc_bounties_created():
    BOUNTIES_CREATED.inc()

def inc_bounties_completed():
    BOUNTIES_COMPLETED.inc()

def set_active_workers(count: int):
    ACTIVE_WORKERS.set(count)

def observe_bid_price(amount: float):
    BID_PRICE.observe(amount)
