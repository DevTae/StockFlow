from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from ..models.stock_model import market_type, stock_info
from ..serializers.stock_serializer import MarketTypeSerializer, StockInfoSerializer


"""
POST /market/
{
    "market_name" : "kospi"
}
다음과 같이 전송한 뒤에, GET 을 사용하면 된다.
"""
class MarketView(APIView):
    def get(self, request):
        market_list = market_type.objects.all()
        serializer = MarketTypeSerializer(market_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MarketTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockInfoView(APIView):
    # /stock?page={page}
    # /stock?limit={limit}
    def get(self, request):
        max_per_page = 10

        # GET Parameter 를 통하여 Pagination 기능 구현
        if 'page' in request.GET:
            page = int(request.GET['page'])
            if not isinstance(page, int):
                return Response({"message": "page 옵션 값이 유효하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            stock_list = stock_info.objects.order_by('stock_code')
            paginator = Paginator(stock_list, per_page=max_per_page)
            print(paginator.num_pages)
            if page <= 0 or page > paginator.num_pages:
                return Response({"message": "page 옵션 값이 유효하지 않습니다."}, status=status.HTTP_204_NO_CONTENT)
            stock_list = paginator.get_page(page)

        elif 'limit' in request.GET:
            limit = int(request.GET['limit'])
            if not isinstance(limit, int) or limit > max_per_page:
                return Response({"message": "limit 옵션 값이 유효하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            stock_list = stock_info.objects.order_by('stock_code')
            total_size = len(stock_list)
            if limit < total_size:
                stock_list = stock_list[total_size - limit:]

        else:
            return Response({"message": "옵션 값이 유효하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StockInfoSerializer(stock_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """
    POST
    {
        "market_name" : xxxxxx,
        "stock_code" : xxxxxx,
        "stock_name" : xxxxxx
    }
    """
    def post(self, request):
        # market_name 을 바탕으로 외래키의 주키 찾기
        if 'market_name' in request.data.keys():
            try:
                market_name = request.data.pop('market_name')
                market_object = market_type.objects.get(market_name=market_name)
                request.data['market'] = market_object.id
            except market_type.DoesNotExist:
                return Response({"message": "market_name 이 유효하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "market_name 이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StockInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StockInfoEachView(APIView):
    def get(self, request, stock_code):
        try:
            stock = stock_info.objects.get(stock_code=stock_code)
        except stock_info.DoesNotExist:
            stock = None
    
        if stock is None:
            return Response(stock, status=status.HTTP_204_NO_CONTENT)
        
        serializer = StockInfoSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
