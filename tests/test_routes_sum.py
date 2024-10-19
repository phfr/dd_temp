import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from routes.sum import route  # Ensure this imports the FastAPI app properly

app = FastAPI()
app.include_router(route)  # Include your route in the FastAPI app


@pytest.mark.asyncio
async def test_calculate_sum_valid_input():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1/2/3/4/5")
        assert response.status_code == 200
        assert response.json() == {"sum": 15.0}


@pytest.mark.asyncio
async def test_calculate_sum_float_input():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1.5/2.7/3.3")
        assert response.status_code == 200
        assert response.json()["sum"] == pytest.approx(7.5, rel=1e-5)


@pytest.mark.asyncio
async def test_calculate_sum_single_number():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/42")
        assert response.status_code == 200
        assert response.json() == {"sum": 42.0}


@pytest.mark.asyncio
async def test_calculate_sum_invalid_input():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/1/2/three/4/5")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid number format in the URL path"}


@pytest.mark.asyncio
async def test_calculate_sum_empty_input():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/sum/")
        assert response.status_code == 400
        assert response.json() == {"detail": "No numbers provided"}
