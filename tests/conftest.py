"""
Fixtures for tests for Milestone 3 Game Logic
"""
import pytest
from strands import StrandsGame

@pytest.fixture
def ft_game():
    return StrandsGame("boards/face-time.txt")

@pytest.fixture
def dir_game():
    return StrandsGame("boards/directions.txt")
