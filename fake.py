import json
import os
import random
from random import choice, randint, randrange
import sys

from django.contrib.auth import get_user_model
from faker import Faker

from blog.models import Category, Post, Tag, Comment
from users.models import Profile

fake = Faker()

User = get_user_model()

# Tùy chỉnh
NUMBER_OF_USERS = 20  # Số lượng người dùng (User)
NUMBER_OF_CATEGORIES = 20  # Số lượng danh mục (Category)
NUMBER_OF_TAGS = 30  # Số lượng thẻ/nhãn (Tag)
NUMBER_OF_POSTS = 50  # Số lượng bài viết (Post)
NUMBER_OF_COMMENTS = 200  # Tổng số lượng bình luận (Comment)
MIN_FOLLOWERS_PER_USER = 2
MAX_FOLLOWERS_PER_USER = 5


class Fake:
    def __init__(self, generate=True, reset=True, delete_users=False):
        if reset:
            if delete_users:
                User.objects.all().filter(is_superuser=False).delete()
            Post.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
        if generate:
            if User.objects.all().count() < 2:
                self.generate_users(NUMBER_OF_USERS)
                self.random_profile()
                self.create_follower(MIN_FOLLOWERS_PER_USER,
                                     MAX_FOLLOWERS_PER_USER)
            self.generate_categories(NUMBER_OF_CATEGORIES)
            self.generate_tags(NUMBER_OF_TAGS)
            self.generate_posts(NUMBER_OF_POSTS)
            self.generate_comments(NUMBER_OF_COMMENTS)

    def generate_users(self, number):
        for _ in range(number):
            mock_user = {
                "username": fake.unique.user_name(),
                "password": "1",
                "email": fake.unique.email()
            }
            user = User.objects.create_user(username=mock_user["username"], password=mock_user["password"],
                                            email=mock_user["email"])
            sys.stdout.write("create a user successful !\n")
            sys.stdout.flush()

    def create_follower(self, min, max):
        all_profiles = Profile.objects.all()
        for profile in all_profiles:
            random_number = randrange(min, max)
            random_follower = Profile.objects.order_by('?')[:random_number]
            for follower in random_follower:
                profile.followers.add(follower)

    def random_profile(self):
        profiles = Profile.objects.all()
        for p in profiles:
            p.bio = fake.sentence(randrange(5, 30))
            p.save()

    def generate_posts(self, n_posts):
        posts = []
        categories = Category.objects.all()
        tags = Tag.objects.all()
        users = User.objects.all().filter(is_superuser=False)
        for i in range(n_posts):
            mock_post = {
                "author": choice(users),
                "title": fake.sentence(randrange(8, 20)),
                "description": fake.sentence(randrange(10, 20)),
                "content": fake.paragraph(150),
                "list_categories": random.sample(list(categories), randrange(1, 3)),
                "list_tags": random.sample(list(tags), randrange(1, 5)),
            }
            post = Post(author=mock_post["author"], title=mock_post["title"], description=mock_post["description"],
                        content=mock_post["content"])
            post.published = True

            post.save()
            post.categories.set(mock_post["list_categories"])
            post.tags.set(mock_post["list_tags"])
            post.save()
            posts.append(post)

        sys.stdout.write(f"create {len(posts)} posts successful !\n")
        sys.stdout.flush()

    def generate_comments(self, n_comments):
        comments = []
        posts = Post.objects.all()
        user = User.objects.all()
        for i in range(0, n_comments):
            mock_comment = {
                "post": choice(posts),
                "user": choice(user),
                "content": fake.sentence(randrange(10, 50))
            }
            comment = Comment(
                post=mock_comment["post"], user=mock_comment["user"], content=mock_comment["content"])
            comments.append(comment)
        Comment.objects.bulk_create(comments)
        sys.stdout.write(f"create {len(comments)} comments successful !\n")
        sys.stdout.flush()

    def generate_tags(self, n_tags=20):
        tags = []

        for _ in range(n_tags):
            tags.append(fake.word().lower())

        for tag in tags:
            c = Tag.objects.get_or_create(name=tag)

        sys.stdout.write(f"create {len(tags)} tags successful !\n")
        sys.stdout.flush()

    def generate_categories(self, n_cat=10):

        categories = []
        category_names = set()

        while len(category_names) < n_cat:
            category_names.add(
                ' '.join(fake.words(nb=randint(2, 3))).capitalize())

        for i, name in enumerate(list(category_names)[:n_cat]):
            description = fake.paragraph(
                nb_sentences=randint(3, 7), variable_nb_sentences=True)

            category_data = dict([
                ("name", name),
                ("description", description)
            ])
            categories.append(category_data)

        for cat in categories:
            c = Category.objects.get_or_create(
                name=cat["name"], description=cat["description"])

        sys.stdout.write(f"create {n_cat} categories successful !\n")
        sys.stdout.flush()
