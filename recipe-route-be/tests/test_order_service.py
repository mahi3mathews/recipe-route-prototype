import unittest
from unittest.mock import MagicMock
from service.order_service import OrderService
from enums.order_type import OrderType
from enums.order_status import OrderStatus
from enums.payment_status import PaymentStatus
from flask_pymongo import ObjectId


class TestOrderService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.order_service = OrderService()

    def setUp(self):
        # Initialize the OrderService with mock objects for dependencies
        self.order_service._OrderService__repo = MagicMock()
        self.order_service._OrderService__cart_service = MagicMock()
        self.order_service._OrderService__store_service = MagicMock()

    def test_add_user_order_success(self):
        # Mock cart_service.get_user_cart_items response
        self.order_service._OrderService__cart_service.get_user_cart_items.return_value = {
            "user_id": "64cbd701d9b42f2182a72c17",
            "cartList": {
                "item1": {"total_price": "10.00", "qty": 2},
                "item2": {"total_price": "5.00", "qty": 3},
            },
            "store_id": "64cbf9709fc3f317f81a0f86",
        }

        # Mock cart_service.update_cart_order response
        self.order_service._OrderService__cart_service.update_cart_order.return_value = {
            "code": 200,
        }
        # Mock store_service.update_store_inventory_order response
        self.order_service._OrderService__store_service.update_store_inventory_order.return_value = None

        # Call the add_user_order method
        result = self.order_service.add_user_order("user123", "payment123", OrderType.PICKUP)

        # Check if the order was successfully added
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["response"]["message"], "Successfully placed an order.")

    def test_add_user_order_cart_update_failed(self):
        # Mock cart_service.get_user_cart_items response
        self.order_service._OrderService__cart_service.get_user_cart_items.return_value = {
            "user_id": "64cbf9709fc3f317f81a0f86",
            "cartList": {
                "item1": {"total_price": "10.00", "qty": 2},
                "item2": {"total_price": "5.00", "qty": 3},
            },
            "store_id": "64cbd701d9b42f2182a72c17",
        }

        # Mock cart_service.update_cart_order response
        self.order_service._OrderService__cart_service.update_cart_order.return_value = {
            "code": 500,
        }

        # Call the add_user_order method
        result = self.order_service.add_user_order("user123", "payment123", OrderType.PICKUP)

        # Check if the order placement failed due to cart update failure
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["response"]["message"], "Successfully placed an order, but failed to update cart.")

    # Add more test cases for other scenarios

    def test_get_user_orders(self):
        # Mock order_repository.get_user_orders response
        self.order_service._OrderService__repo.get_user_orders.return_value = [
            {
                "_id": "64cbd701d9b42f2182a72c17",
                "user_id": "64cbd701d9b42f2182a72c17",
                "payment_id": "payment123",
                "order_items": {
                    "item1": {"total_price": "10.00", "qty": 2},
                    "item2": {"total_price": "5.00", "qty": 3},
                },
                "total_price": "15.00",
                "payment_status": PaymentStatus.PAID.value,
                "status": OrderStatus.WAITING.value,
                "order_type": OrderType.PICKUP.value,
                "store_id": "64cbf9709fc3f317f81a0f86",

            },
            # Add more order items...
        ]

        # Mock store_service.get_all_stores response
        self.order_service._OrderService__store_service.get_all_stores.return_value = [
            {
                "_id": ObjectId( "64b31bc89662c42a02c39972"),
                "store_name": "MariyaStore",
                "business_email": "mariya_store@gmail.com",
                "business_phonenumber": "01234567891",
                "address": {
                    "street": "19 Astion Street",
                    "city": "Coventry",
                    "post_code": "CV2 4HA",
                    "country": "UK"
                },
                "FSA_id": "",
                "user_id": "64b31bc89662c42a02c39970",
                "created_on": {
                    "$date": "2023-07-15T23:20:56.286Z"
                },
                "updated_on": {
                    "$date": "2023-07-15T23:20:56.286Z"
                },
                "store_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEBLAEsAAD/4QBWRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAITAAMAAAABAAEAAAAAAAAAAAEsAAAAAQAAASwAAAAB/+0ALFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAAAPHAFaAAMbJUccAQAAAgAEAP/hDIFodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvADw/eHBhY2tldCBiZWdpbj0n77u/JyBpZD0nVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkJz8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0nYWRvYmU6bnM6bWV0YS8nIHg6eG1wdGs9J0ltYWdlOjpFeGlmVG9vbCAxMC4xMCc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczp0aWZmPSdodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyc+CiAgPHRpZmY6UmVzb2x1dGlvblVuaXQ+MjwvdGlmZjpSZXNvbHV0aW9uVW5pdD4KICA8dGlmZjpYUmVzb2x1dGlvbj4zMDAvMTwvdGlmZjpYUmVzb2x1dGlvbj4KICA8dGlmZjpZUmVzb2x1dGlvbj4zMDAvMTwvdGlmZjpZUmVzb2x1dGlvbj4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6eG1wTU09J2h0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8nPgogIDx4bXBNTTpEb2N1bWVudElEPmFkb2JlOmRvY2lkOnN0b2NrOjcyODNmNDM5LWU4NTAtNDEwZi04MTEyLTU0MWQ0MTc3MDg4OTwveG1wTU06RG9jdW1lbnRJRD4KICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOjFmZWU5OTJkLWU4MjItNDUxZC05ODUzLWRmYjJmYTM1MTVhZjwveG1wTU06SW5zdGFuY2VJRD4KIDwvcmRmOkRlc2NyaXB0aW9uPgo8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSd3Jz8+/9sAQwAFAwQEBAMFBAQEBQUFBgcMCAcHBwcPCwsJDBEPEhIRDxERExYcFxMUGhURERghGBodHR8fHxMXIiQiHiQcHh8e/9sAQwEFBQUHBgcOCAgOHhQRFB4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4e/8AAEQgBaAJYAwEiAAIRAQMRAf/EAB0AAQADAAMBAQEAAAAAAAAAAAAGBwgDBAUBAgn/xABTEAABAwMBBQMIBAgKCAUFAAAAAQIDBAURBgcSEyExCEFRFBUiMmFxgZFCobHBFjNSYnKC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"
            },
        ]

        # Call the get_user_orders method
        result = self.order_service.get_user_orders("64cbd701d9b42f2182a72c17", is_raw_data=False)

        # Check if the orders are correctly formatted in the response
        self.assertEqual(result["code"], 200)
        self.assertEqual(result["response"]["message"], "Successfully fetched all orders of user")
        self.assertIsInstance(result["response"]["data"], list)
        self.assertEqual(len(result["response"]["data"]), 1)
        # Add more assertions as needed


if __name__ == "__main__":
    unittest.main()
