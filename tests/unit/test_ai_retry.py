from ai.retry import backoff_delays

def test_backoff_delays_default():
    delays = backoff_delays()
    assert delays == [0.5, 1.5]
