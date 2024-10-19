"""Exampple module that only contains a sum API endpoint."""

from fastapi import Response

from utils.API_framework import Route
from utils.custom_logging import logger

route = Route()


@route.get("/sum/{numbers:path}")
async def calculate_sum(numbers: str, response: Response):
    """
    Calculate the sum of a list of numbers provided in the URL path.

    Args:
        numbers (str): A string of numbers separated by '/' in the URL path.

    Returns:
        dict: A dictionary containing the sum of the input numbers.

    Raises:
        HTTPException: If an error occurs during the calculation.
    """
    logger.debug("Received request to sum numbers: %s", numbers)

    if not numbers:
        logger.error("Empty input received")
        response.status_code = 400
        return {"detail": "No numbers provided"}

    try:
        # Split the string into a list and convert each item to float
        number_list = [float(num) for num in numbers.split("/") if num]
        if not number_list:
            logger.error("No valid numbers found in input")
            response.status_code = 400
            return {"detail": "No valid numbers provided"}
        result = sum(number_list)
        logger.info("Successfully calculated sum: %s", result)
        return {"sum": result}
    except ValueError as e:
        logger.error("Error parsing numbers: %s", str(e))
        response.status_code = 400
        return {"detail": "Invalid number format in the URL path"}
