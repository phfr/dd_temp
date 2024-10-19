"""
Integration tests for the sum API endpoint in the DataDiVR-Backend.

This module contains pytest fixtures and test cases to verify the functionality
of the sum API endpoint, testing various input scenarios and expected responses.
"""

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from routes.sum import route  # Ensure this imports the FastAPI app properly

app = FastAPI()
app.include_router(route)  # Include your route in the FastAPI app


@pytest.mark.asyncio
async def test_calculate_sum_valid_input():
    """
    Test the sum endpoint with valid integer inputs.

    Verifies that the endpoint correctly calculates the sum of multiple integers.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1/2/3/4/5")
        assert response.status_code == 200
        assert response.json() == {"sum": 15.0}


@pytest.mark.asyncio
async def test_calculate_sum_float_input():
    """
    Test the sum endpoint with valid float inputs.

    Verifies that the endpoint correctly calculates the sum of multiple floats.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1.5/2.7/3.3")
        assert response.status_code == 200
        assert response.json()["sum"] == pytest.approx(7.5, rel=1e-5)


@pytest.mark.asyncio
async def test_calculate_sum_single_number():
    """
    Test the sum endpoint with a single number input.

    Verifies that the endpoint correctly handles and returns a single number.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/42")
        assert response.status_code == 200
        assert response.json() == {"sum": 42.0}


@pytest.mark.asyncio
async def test_calculate_sum_invalid_input():
    """
    Test the sum endpoint with invalid input.

    Verifies that the endpoint correctly handles and reports invalid number formats.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1/2/three/4/5")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid number format in the URL path"}


@pytest.mark.asyncio
async def test_calculate_sum_empty_input():
    """
    Test the sum endpoint with empty input.

    Verifies that the endpoint correctly handles and reports when no numbers are provided.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/")
        assert response.status_code == 400
        assert response.json() == {"detail": "No numbers provided"}
