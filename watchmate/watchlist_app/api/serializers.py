from rest_framework import serializers
from watchlist_app.models import WatchList , StreamPlatform ,Review

"""
serializers.Serializer
"""

# def name_len(value):
#     """
#     validator
#     - Individual fields on a serializer can include validators,
#        by declaring them on the field instance
#     """
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is to short")
#
# class MovieSerializers(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_len])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         instance pointing towards old data
#         validated_data pointing towards new data
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#     # def validate_name(self, value):
#     #     """
#     #     def validate_<field_name>(self, value): # that why its validate name field
#     #     Field level validation
#     #     """
#     #     if len(value)<2:
#     #         raise serializers.ValidationError("Name is to short")
#     #     return value
#
#     def validate(self, data):
#         """
#         object level validation
#         """
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description should be different")
#         else:
#              return data


"""
serializers.ModelSerializer
"""
class ReviewSerializers(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        #fields = "__all__"  # it includes all fields
        exclude = ("watchlist",)

class WatchListSerializers(serializers.ModelSerializer):
    """
    The ModelSerializer class is the same as a regular Serializer class, except that:
    It will automatically generate a set of fields for you, based on the model.
    It will automatically generate validators for the serializer, such as unique_together validators.
    It includes simple default implementations of .create() and .update().
    """
    #len_name = serializers.SerializerMethodField()

    #reviews = ReviewSerializers(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = "__all__" #  it includes all fields
        #fields = ['id','name','description']  # it includes user define field
        #exclude = ['active'] # It exculded mention field

class StreamPlatformSerializers(serializers.ModelSerializer):
    # Nested serializer
    # Here the variabale name is must same as we define in django model relationship
    # It return all fields
    watchlist = WatchListSerializers(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True) It return title only
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) It return PK
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='track-detail'
    # )    In return the link just assign view name correctly

    class Meta:
        model = StreamPlatform
        fields = "__all__"

    # def get_len_name(self,object):
    #     """
    #     syntax get_<field_name>
    #     adding custome field in data using serializer without define in model.py
    #     No, adding a custom field like len_name = serializers.SerializerMethodField()
    #     does NOT affect your database or the Django admin section.
    #     """
    #     length = len(object.name)
    #     return length
    #
    # def validate_name(self, value):
    #     """
    #     def validate_<field_name>(self, value): # that why its validate name field
    #     Field level validation
    #     """
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is to short")
    #     return value
    #
    # def validate(self, data):
    #     """
    #     object level validation
    #     """
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description should be different")
    #     else:
    #          return data


