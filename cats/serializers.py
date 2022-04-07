from rest_framework import serializers

from .models import Achievement, Cat, Owner

class AchivementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Achievement
        fields = ('id', 'name')

class CatSerializer(serializers.ModelSerializer):
    achievements = AchivementSerializer(many=True) # Убрали read_only=True
    # Убрали owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner','achievements')
        
        def create(self, validated_data):
            # Уберем список достижений из словаря validated_data и сохраним его
            achievements = validated_data.pop('achievements')

            # Создадим нового котика пока без достижений, данных нам достаточно
            cat = Cat.objects.create(**validated_data)

            # Для каждого достижения из списка достижений
            for achievement in achievements:
                # Создадим новую запись или получим существующий экземпляр из БД
                current_achievement, status = Achievement.objects.get_or_create(
                    **achievement)
                # Поместим ссылку на каждое достижение во вспомогательную таблицу
                # Не забыв указать к какому котику оно относится
                AchievementCat.objects.create(
                    achievement=current_achievement, cat=cat)
            return cat 
        

class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
        
