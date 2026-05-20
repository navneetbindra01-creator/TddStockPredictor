"""Behave environment hooks."""
import sys
import os

# Allow imports from project root (pages/, src/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
