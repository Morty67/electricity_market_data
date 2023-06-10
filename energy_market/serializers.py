from rest_framework import serializers

from energy_market.models import MarketClosingData


class MarketClosingDataSerializer(serializers.ModelSerializer):
    hour = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    volume = serializers.DecimalField(max_digits=10, decimal_places=1)

    class Meta:
        model = MarketClosingData
        fields = ["date", "hour", "price", "volume"]

    def get_hour(self, obj):
        return f"{obj.hour}:00"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["price (грн/МВт.год)"] = representation.pop("price")
        representation["volume (МВт.год)"] = representation.pop("volume")
        return representation
