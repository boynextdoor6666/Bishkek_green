from django.test import TestCase
from django.contrib.auth.models import User
from .models import TreeType, GreenLocation, PlantingRequest, Donation, GalleryImage


class TreeTypeTestCase(TestCase):
    def setUp(self):
        self.tree_type = TreeType.objects.create(
            name="Дуб",
            description="Крупное дерево с широкой кроной.",
        )

    def test_tree_type_creation(self):
        self.assertEqual(self.tree_type.name, "Дуб")
        self.assertEqual(self.tree_type.description, "Крупное дерево с широкой кроной.")


class GreenLocationTestCase(TestCase):
    def setUp(self):
        self.location = GreenLocation.objects.create(
            title="Парк Победы",
            description="Центральный парк города.",
            latitude=42.8746,
            longitude=74.5698,
            address="ул. Победы, 1",
            status="planned",
        )

    def test_green_location_creation(self):
        self.assertEqual(self.location.title, "Парк Победы")
        self.assertEqual(self.location.status, "planned")


class PlantingRequestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.tree_type = TreeType.objects.create(
            name="Береза",
            description="Дерево с белой корой.",
        )
        self.request = PlantingRequest.objects.create(
            user=self.user,
            name="Иван Иванов",
            email="ivan@example.com",
            phone="+996555123456",
            address="ул. Манаса, 10",
            description="Хочу посадить дерево во дворе.",
            preferred_tree_type=self.tree_type,
            status="pending",
        )

    def test_planting_request_creation(self):
        self.assertEqual(self.request.name, "Иван Иванов")
        self.assertEqual(self.request.status, "pending")


class DonationTestCase(TestCase):
    def setUp(self):
        self.donation = Donation.objects.create(
            name="Айгуль",
            email="aigul@example.com",
            donation_type="money",
            amount=1000.00,
            description="Пожертвование на озеленение.",
        )

    def test_donation_creation(self):
        self.assertEqual(self.donation.name, "Айгуль")
        self.assertEqual(self.donation.donation_type, "money")


class GalleryImageTestCase(TestCase):
    def setUp(self):
        self.location = GreenLocation.objects.create(
            title="Парк Победы",
            description="Центральный парк города.",
            latitude=42.8746,
            longitude=74.5698,
            address="ул. Победы, 1",
            status="completed",
        )
        self.image = GalleryImage.objects.create(
            title="Фото парка",
            description="Фото после озеленения.",
            image="park.jpg",
            location=self.location,
        )

    def test_gallery_image_creation(self):
        self.assertEqual(self.image.title, "Фото парка")
        self.assertEqual(self.image.location.title, "Парк Победы")