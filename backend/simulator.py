"""
CARELINK AI - Patient Vitals Simulator
Generates realistic patient vital signs for 10 independent patients
"""

import random
import time
from datetime import datetime

class PatientSimulator:
    """Simulates realistic vital signs for a single patient"""
    
    def __init__(self, patient_id, name, age, condition="normal"):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.condition = condition  # normal, at-risk, critical
        
        # Baseline vitals
        if condition == "normal":
            self.baseline_hr = random.randint(60, 80)
            self.baseline_temp = round(36.5 + random.uniform(-0.5, 0.5), 1)
            self.baseline_spo2 = random.randint(95, 98)
        elif condition == "at-risk":
            self.baseline_hr = random.randint(85, 100)
            self.baseline_temp = round(37.5 + random.uniform(-0.3, 0.3), 1)
            self.baseline_spo2 = random.randint(90, 94)
        else:  # critical
            self.baseline_hr = random.randint(105, 130)
            self.baseline_temp = round(38.5 + random.uniform(-0.2, 0.2), 1)
            self.baseline_spo2 = random.randint(85, 92)
        
        # Current vitals (start with baseline)
        self.heart_rate = self.baseline_hr
        self.temperature = self.baseline_temp
        self.spo2 = self.baseline_spo2
        
        # Trend variables
        self.hr_trend = random.choice([-1, 0, 1])
        self.temp_trend = random.choice([-1, 0, 1])
        self.spo2_trend = random.choice([-1, 0, 1])
        
        # Simulation counter
        self.update_count = 0
    
    def update_vitals(self):
        """Update vitals with realistic variation"""
        self.update_count += 1
        
        # Heart Rate (normal: 60-100, with gradual change)
        self.hr_trend += random.uniform(-0.3, 0.3)
        self.heart_rate = max(50, min(150, self.baseline_hr + self.hr_trend * 10))
        
        # Temperature (normal: 36.5-37.5°C, with gradual change)
        self.temp_trend += random.uniform(-0.1, 0.1)
        self.temperature = round(max(35.0, min(40.0, self.baseline_temp + self.temp_trend * 0.5)), 1)
        
        # SpO2 (normal: >95%, with gradual change)
        self.spo2_trend += random.uniform(-0.2, 0.2)
        self.spo2 = max(75, min(100, int(self.baseline_spo2 + self.spo2_trend * 3)))
        
        # Periodically create emergencies (5% chance every update)
        if random.random() < 0.05 and self.update_count > 20:
            self.trigger_emergency()
    
    def trigger_emergency(self):
        """Simulate an emergency condition"""
        self.condition = "critical"
        self.baseline_hr = random.randint(110, 130)
        self.baseline_temp = round(38.5 + random.uniform(-0.2, 0.3), 1)
        self.baseline_spo2 = random.randint(85, 92)
    
    def get_vitals(self):
        """Return current vitals as dictionary"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "heart_rate": round(self.heart_rate, 1),
            "temperature": self.temperature,
            "spo2": self.spo2,
            "condition": self.condition,
            "timestamp": datetime.now().isoformat()
        }


class PatientsDatabase:
    """Manages 10 simulated patients"""
    
    def __init__(self):
        self.patients = {
            1: PatientSimulator(1, "John Doe", 65, "normal"),
            2: PatientSimulator(2, "Sarah Smith", 58, "normal"),
            3: PatientSimulator(3, "Mike Johnson", 72, "at-risk"),
            4: PatientSimulator(4, "Emily Davis", 51, "normal"),
            5: PatientSimulator(5, "Robert Brown", 68, "normal"),
            6: PatientSimulator(6, "Lisa Wilson", 55, "at-risk"),
            7: PatientSimulator(7, "James Taylor", 75, "normal"),
            8: PatientSimulator(8, "Jennifer Lee", 62, "normal"),
            9: PatientSimulator(9, "David Anderson", 70, "at-risk"),
            10: PatientSimulator(10, "Mary Thomas", 60, "normal"),
        }
    
    def update_all_patients(self):
        """Update vitals for all patients"""
        for patient in self.patients.values():
            patient.update_vitals()
    
    def get_patient(self, patient_id):
        """Get single patient vitals"""
        if patient_id in self.patients:
            return self.patients[patient_id].get_vitals()
        return None
    
    def get_all_patients(self):
        """Get vitals for all patients"""
        return [patient.get_vitals() for patient in self.patients.values()]
    
    def get_patient_list(self):
        """Get list of all patients (for dashboard)"""
        return [
            {
                "patient_id": p.patient_id,
                "name": p.name,
                "age": p.age,
                "condition": p.condition
            }
            for p in self.patients.values()
        ]
