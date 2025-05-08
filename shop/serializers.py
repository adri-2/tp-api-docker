from rest_framework import serializers

from shop.models import Category, Product, Article


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
    
    def validate_name(self,value):
        if Article.objects.filter(name=value).exists():
            raise serializers.ValidationError("Article exists")
        return value
    
    def validate_price(self, data):
        if data < 1:
            raise serializers.ValidationError('Price doit etre > 1')
        return data
    
    def validate_product(self, data):
        if data.active is False:
             raise serializers.ValidationError('Product doit etre active')

        return data



class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleListSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name','description']

    def validate_name(self,value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category exists")
        return value
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data


class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data
    
    