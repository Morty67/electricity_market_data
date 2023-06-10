from rest_framework import views, status
from rest_framework.response import Response

from energy_market.models import MarketClosingData
from energy_market.serializers import MarketClosingDataSerializer


class MarketClosingDataView(views.APIView):
    def get(self, request, date):
        try:
            market_data = MarketClosingData.objects.filter(date=date)
            if market_data.exists():
                serializer = MarketClosingDataSerializer(market_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No data available for this date."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
