# tests/test_day_35.py
def test_event_listener_pattern():
    messages = []
    def handler(msg):
        messages.append(msg)
    
    # Simulate event
    def trigger_event():
        handler("Event triggered!")
    
    trigger_event()
    assert messages == ["Event triggered!"]