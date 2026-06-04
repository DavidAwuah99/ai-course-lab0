"""
environment_test.py
Lab 0 - Environment Verification Script
Verify that all required packages are installed and accessible.
"""

import sys
import platform
import os

def verify_environment():
    """Verify Python environment and package installations."""
    
    results = []
    
    # Check Python version
    python_version = sys.version.split()[0]
    results.append(f"✅ Python Version: {python_version}")
    
    # Check operating system
    results.append(f"✅ OS: {platform.system()} {platform.release()}")
    
    # Required packages with versions
    required_packages = {
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn'
    }
    
    for package_name, display_name in required_packages.items():
        try:
            module = __import__(package_name)
            version = getattr(module, '__version__', 'unknown')
            results.append(f"✅ {display_name}: {version}")
        except ImportError:
            results.append(f"❌ {display_name}: NOT INSTALLED")
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    in_conda = 'CONDA_PREFIX' in os.environ
    
    if in_venv:
        results.append(f"✅ Virtual Environment: Active ({sys.prefix})")
    elif in_conda:
        results.append(f"✅ Conda Environment: Active ({os.environ['CONDA_PREFIX']})")
    else:
        results.append("⚠️  Virtual Environment: Not active")
    
    return "\n".join(results)

if __name__ == "__main__":
    print("=" * 50)
    print("LAB 0: ENVIRONMENT VERIFICATION")
    print("=" * 50)
    print(verify_environment())
    print("=" * 50)
