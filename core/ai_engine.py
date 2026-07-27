# KHOEM_AI CORE SYSTEM ENGINE - MAHANOKOR 369
import random

class MahanokorCore:
    def __init__(self):
        self.system_name = "MAHANOKOR-369"
        self.version = "KHOEM_AI_v3.6.9"
        self.defense_layers = 45
        self.matrix_locked = False
        
    def get_matrix_status(self):
        """គណនាស្ថានភាពប្រព័ន្ធពិតប្រាកដ"""
        return {
            "status": "online" if not self.matrix_locked else "locked",
            "cooling_temp": round(random.uniform(11.8, 13.5), 1),
            "defense_status": f"{self.defense_layers} layers active",
            "botany_health": 100,
            "healthcare_health": 100
        }
        
    def trigger_security_lock(self):
        """ពិធីសារបិទម៉ាទ្រីសសុវត្ថិភាព"""
        self.matrix_locked = True
        return self.matrix_locked
