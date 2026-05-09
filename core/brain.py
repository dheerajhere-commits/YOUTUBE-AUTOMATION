import psutil
import json
import sqlite3
import os
from database.db import get_db_connection

class CognitiveBrain:
    def __init__(self):
        """
        The Neural Logic Brain of the system.
        It detects hardware capabilities to scale processing and learns from past video performance.
        """
        self.hardware_profile = self._assess_hardware()

    def _assess_hardware(self):
        """
        Assesses the system hardware to determine concurrency limits.
        Works across Windows 7/10/11 and Linux.
        """
        cpu_count = psutil.cpu_count(logical=True) or 2
        memory_gb = psutil.virtual_memory().total / (1024 ** 3)

        # Calculate dynamic concurrency limit based on resources
        if memory_gb < 4:
            # Low-end PC (e.g., old Windows 7 machine)
            concurrency_limit = 1
            tier = "Low-end"
        elif memory_gb < 8:
            concurrency_limit = max(2, cpu_count // 2)
            tier = "Mid-range"
        else:
            # High-end PC
            concurrency_limit = max(4, cpu_count)
            tier = "High-end"

        print(f"[Brain] Assessed Hardware: {tier} ({cpu_count} Cores, {memory_gb:.1f}GB RAM)")
        print(f"[Brain] Setting concurrent processing limit to {concurrency_limit}")

        return {
            "tier": tier,
            "cpu_count": cpu_count,
            "memory_gb": memory_gb,
            "concurrency_limit": concurrency_limit
        }

    def get_concurrency_limit(self):
        return self.hardware_profile["concurrency_limit"]

    def memorize_success(self, niche: str, strategy: str, score: float):
        """
        Learns from actions. Stores the performance of a niche/strategy pair.
        """
        print(f"[Brain] Memorizing outcome... Niche: {niche}, Score: {score}")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # If the entry exists, update the score (moving average), else insert
            cursor.execute("SELECT score, encounters FROM neural_memory WHERE niche=?", (niche,))
            row = cursor.fetchone()

            if row:
                old_score = row['score']
                encounters = row['encounters']
                new_score = ((old_score * encounters) + score) / (encounters + 1)
                cursor.execute(
                    "UPDATE neural_memory SET score=?, encounters=? WHERE niche=?",
                    (new_score, encounters + 1, niche)
                )
            else:
                cursor.execute(
                    "INSERT INTO neural_memory (niche, strategy, score, encounters) VALUES (?, ?, ?, 1)",
                    (niche, strategy, score)
                )
            conn.commit()

    def evaluate_niche(self, niche: str) -> float:
        """
        Recalls past memory to determine confidence in a niche.
        Returns a confidence multiplier (1.0 = neutral).
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT score FROM neural_memory WHERE niche=?", (niche,))
            row = cursor.fetchone()

            if row:
                score = row['score']
                print(f"[Brain] Recalling past memory for '{niche}'. Historical score: {score:.2f}")
                # Baseline is 5.0, max is 10.0
                return max(0.5, score / 5.0)
            else:
                print(f"[Brain] No prior memory for '{niche}'. Proceeding with caution (baseline).")
                return 1.0
