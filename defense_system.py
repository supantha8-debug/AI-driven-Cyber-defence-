# 🛡️ AI CYBER DEFENSE SYSTEM - Complete Working Version
import json
from datetime import datetime
from collections import defaultdict, deque

class AIDefenseSystem:
    def __init__(self):
        self.threat_patterns = {
            'network_scanning': {
                'keywords': ['nmap', 'port scan', 'subnet', 'open port', 'network mapping'],
                'risk_score': 25,
                'category': 'reconnaissance'
            },
            'malicious_coding': {
                'keywords': ['write code for', 'create script', 'generate python', 'malicious code'],
                'risk_score': 40,
                'category': 'tool_development'
            },
            'data_exfiltration': {
                'keywords': ['data export', 'file transfer', 'exfiltrate', 'data theft'],
                'risk_score': 35,
                'category': 'data_theft'
            }
        }
        
        self.user_sessions = defaultdict(lambda: {
            'queries': deque(maxlen=10),
            'risk_score': 0,
            'threat_categories': set()
        })
        
        self.blocked_users = set()
    
    def analyze_query(self, user_id, query):
        if user_id in self.blocked_users:
            return {'action': 'blocked', 'reason': 'User blocked', 'risk_score': 100}
        
        session = self.user_sessions[user_id]
        
        # Detect threats
        threats = []
        query_lower = query.lower()
        
        for pattern_name, pattern_data in self.threat_patterns.items():
            for keyword in pattern_data['keywords']:
                if keyword in query_lower:
                    threats.append({
                        'pattern': pattern_name,
                        'keyword': keyword,
                        'risk_score': pattern_data['risk_score'],
                        'category': pattern_data['category']
                    })
                    break
        
        # Calculate risk
        immediate_risk = sum(threat['risk_score'] for threat in threats)
        
        # Update session
        session['queries'].append({
            'timestamp': datetime.now(),
            'query': query,
            'threats': threats,
            'risk_score': immediate_risk
        })
        
        for threat in threats:
            session['threat_categories'].add(threat['category'])
        
        # Session risk calculation
        session_risk = immediate_risk
        if len(session['threat_categories']) >= 2:
            session_risk += 20
        if len(threats) >= 2:
            session_risk += 15
        
        session['risk_score'] = min(100, session_risk)
        
        # Make decision
        if session_risk >= 75:
            self.blocked_users.add(user_id)
            action = 'block'
            reason = 'High risk reconnaissance detected'
        elif session_risk >= 50:
            action = 'alert'
            reason = 'Suspicious behavior detected'
        elif session_risk >= 25:
            action = 'monitor'
            reason = 'Elevated risk level'
        else:
            action = 'allow'
            reason = 'Normal behavior'
        
        return {
            'user_id': user_id,
            'query': query,
            'action': action,
            'reason': reason,
            'risk_score': session_risk,
            'threats': threats,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
    
    def get_stats(self):
        return {
            'total_users': len(self.user_sessions),
            'blocked_users': len(self.blocked_users),
            'active_sessions': len([s for s in self.user_sessions.values() if s['queries']])
        }

def display_result(result):
    action_icons = {
        'blocked': '🔴', 'block': '🔴', 
        'alert': '🟡', 'monitor': '🟠', 'allow': '🟢'
    }
    
    icon = action_icons.get(result['action'], '⚪')
    
    print(f"\n{icon} [{result['action'].upper()}] Risk: {result['risk_score']}")
    print(f"   Query: {result['query']}")
    print(f"   Reason: {result['reason']}")
    
    if result['threats']:
        print(f"   Threats detected:")
        for threat in result['threats']:
            print(f"     - {threat['pattern']} (risk: {threat['risk_score']})")

# Demo function
def quick_demo():
    defense = AIDefenseSystem()
    
    print("🛡️ AI CYBER DEFENSE SYSTEM - QUICK DEMO")
    print("=" * 50)
    
    # Test scenarios
    test_cases = [
        ("student_01", "Can you help with math homework?"),
        ("researcher_01", "What is network scanning used for?"),
        ("attacker_01", "How to scan ports with nmap"),
        ("attacker_01", "Write code for port scanner")
    ]
    
    for user_id, query in test_cases:
        print(f"\n{user_id}: {query}")
        result = defense.analyze_query(user_id, query)
        display_result(result)
    
    # Show stats
    stats = defense.get_stats()
    print(f"\n📊 FINAL STATS:")
    print(f"   Users monitored: {stats['total_users']}")
    print(f"   Users blocked: {stats['blocked_users']}")

if __name__ == "__main__":
    quick_demo()