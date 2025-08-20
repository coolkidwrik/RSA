import psutil
from typing import Dict

def get_system_info() -> Dict[str, str]:
    """Get system information for health checks"""
    return {
        "cpu_percent": f"{psutil.cpu_percent()}%",
        "memory_percent": f"{psutil.virtual_memory().percent}%",
        "available_memory": f"{psutil.virtual_memory().available // 1024 // 1024} MB"
    }

def format_large_number(number: int, max_digits: int = 50) -> str:
    """Format large numbers for display"""
    num_str = str(number)
    if len(num_str) <= max_digits:
        return num_str
    return f"{num_str[:max_digits//2]}...{num_str[-max_digits//2:]}"

def calculate_key_strength(bit_length: int) -> str:
    """Calculate relative strength of RSA key"""
    if bit_length < 1024:
        return "Weak (Educational only)"
    elif bit_length < 2048:
        return "Moderate (Not recommended for production)"
    elif bit_length < 3072:
        return "Strong"
    else:
        return "Very Strong"

def estimate_prime_generation_time(bit_length: int) -> float:
    """Estimate time needed for prime generation based on bit length"""
    # Rough estimates based on typical performance
    base_time = 0.1  # seconds for 512-bit
    complexity_factor = (bit_length / 512) ** 2
    return base_time * complexity_factor