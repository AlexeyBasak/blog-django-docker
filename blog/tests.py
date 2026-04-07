from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Category
from blog.forms import PostForm

User = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Python'
        )
    
    def test_category_creation(self):
        """Проверка создания категории"""
        self.assertEqual(self.category.name, 'Python')
        self.assertTrue(self.category.slug)
        self.assertEqual(str(self.category), 'Python')
    
    def test_slug_auto_generation(self):
        """Проверка авто-генерации slug"""
        category = Category.objects.create(name='Django Framework')
        self.assertEqual(category.slug, 'django-framework')
    
    def test_unique_slug(self):
        """Проверка уникальности slug"""
        with self.assertRaises(Exception):
            Category.objects.create(name='Python')  # Уже существует


class PostModelTest(TestCase):
    """Тесты для модели Post"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержимое теста',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_post_creation(self):
        """Проверка создания поста"""
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertTrue(self.post.slug)  # Slug существует
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(str(self.post), 'Тестовый пост')
    
    def test_slug_auto_generation(self):
        """Проверка авто-генерации slug"""
        post = Post.objects.create(
            title='Ещё один пост',
            content='Тест',
            author=self.user
        )
        self.assertTrue(post.slug)  # Slug существует
        self.assertNotEqual(post.slug, '')  # Не пустой
    
    def test_status_choices(self):
        """Проверка статусов поста"""
        self.assertEqual(self.post.status, 'published')
        self.post.status = 'draft'
        self.post.save()
        self.assertEqual(self.post.status, 'draft')
    
    def test_published_only(self):
        """Проверка фильтрации опубликованных"""
        draft_post = Post.objects.create(
            title='Черновик',
            content='Не опубликован',
            author=self.user,
            status='draft'
        )
        published_posts = Post.objects.filter(status='published')
        self.assertIn(self.post, published_posts)
        self.assertNotIn(draft_post, published_posts)


class PostListViewTest(TestCase):
    """Тесты для списка постов"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test')
        
        # Создаём тестовые посты
        Post.objects.create(
            title='Опубликованный пост',
            content='Контент',
            author=self.user,
            status='published'
        )
        Post.objects.create(
            title='Черновик',
            content='Контент',
            author=self.user,
            status='draft'
        )
    
    def test_post_list_status_code(self):
        """Проверка статуса страницы"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_list_template(self):
        """Проверка использования шаблона"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')
    
    def test_only_published_posts(self):
        """Проверка что видны только опубликованные"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, 'Опубликованный пост')
        self.assertNotContains(response, 'Черновик')
    
    def test_post_count(self):
        """Проверка количества постов"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(len(response.context['posts']), 1)


class PostDetailViewTest(TestCase):
    """Тесты для детального просмотра поста"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Тестовый пост',
            slug='test-post',
            content='Контент поста',
            author=self.user,
            status='published'
        )
    
    def test_post_detail_status_code(self):
        """Проверка статуса страницы"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_template(self):
        """Проверка использования шаблона"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_not_found(self):
        """Проверка 404 для несуществующего поста"""
        response = self.client.get(reverse('blog:post_detail', args=['non-existent']))
        self.assertEqual(response.status_code, 404)
    
    def test_draft_not_accessible(self):
        """Проверка что черновики не видны"""
        self.post.status = 'draft'
        self.post.save()
        response = self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 404)


class PostCreateViewTest(TestCase):
    """Тесты для создания поста"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test')
    
    def test_create_login_required(self):
        """Проверка что нужен вход"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect на login
    
    def test_create_post_success(self):
        """Проверка успешного создания"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'Новый пост',
            'content': 'Содержимое нового поста',
            'category': self.category.id,
            'status': 'published'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Post.objects.filter(title='Новый пост').exists())
    
    def test_create_post_author(self):
        """Проверка что автор = текущий пользователь"""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('blog:post_create'), {
            'title': 'Пост автора',
            'content': 'Контент',
            'status': 'published'
        })
        post = Post.objects.get(title='Пост автора')
        self.assertEqual(post.author, self.user)


class PostDeleteViewTest(TestCase):
    """Тесты для удаления поста"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Удалить меня',
            slug='delete-me',
            content='Контент',
            author=self.user,
            status='published'
        )
    
    def test_delete_login_required(self):
        """Проверка что нужен вход"""
        response = self.client.get(reverse('blog:post_delete', args=[self.post.slug]))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_success(self):
        """Проверка успешного удаления"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('blog:post_delete', args=[self.post.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(slug='delete-me').exists())
    
    def test_delete_only_author(self):
        """Проверка что только автор может удалить"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('blog:post_delete', args=[self.post.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(slug='delete-me').exists())  # Не удалён



class PostFormTest(TestCase):
    """Тесты для формы поста"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_form_valid(self):
        """Проверка валидной формы"""
        form = PostForm(data={
            'title': 'Тестовый заголовок',
            'content': 'Тестовое содержимое',
            'status': 'published'
        })
        self.assertTrue(form.is_valid())
    
    def test_form_required_fields(self):
        """Проверка обязательных полей"""
        form = PostForm(data={
            'title': '',  # Пустой
            'content': 'Контент',
            'status': 'published'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_save(self):
        """Проверка сохранения формы"""
        form = PostForm(data={
            'title': 'Сохранить тест',
            'content': 'Контент для сохранения',
            'status': 'draft'
        })
        post = form.save(commit=False)
        post.author = self.user
        post.save()
        self.assertEqual(Post.objects.filter(title='Сохранить тест').count(), 1)