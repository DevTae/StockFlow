from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from ..models.stock_model import market_type, stock_info
from ..serializers.stock_serializer import MarketTypeSerializer, StockInfoSerializer
from ..api_keys import api_key_header, api_keys
from ..errors import RES_ERR_MSG_HEAD_MUST_EXISTS, \
                     RES_ERR_MSG_HEAD_NOT_SUPPORTED, \
                     RES_ERR_MSG_VAL_FORMAT_MISMATCH, \
                     RES_ERR_MSG_VAL_NOT_VALID, \
                     RES_ERR_MSG_VAL_NOT_FOUND
                     
class MarketView(APIView):
    """
    GET /market
    """
    def get(self, request):
        market_list = market_type.objects.all()
        serializer = MarketTypeSerializer(market_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    POST /market/
    {
        "api_key" : xxxxxx,
        "market_name" : "kospi"
    }
    """
    def post(self, request):
        if api_key_header not in request.data:
            return RES_ERR_MSG_HEAD_MUST_EXISTS(api_key_header)
    
        api_key = request.data.pop(api_key_header)
        if api_key not in api_keys:
            return RES_ERR_MSG_VAL_NOT_VALID(api_key_header)

        serializer = MarketTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    PUT /market
    {
        "api_key" : xxxxxx,
        "market_name" : "kospi",
        "market_name_after" : "kosdaq"
    }
    """
    def put(self, request):
        if api_key_header not in request.data:
            return RES_ERR_MSG_HEAD_MUST_EXISTS(api_key_header)
    
        api_key = request.data.pop(api_key_header)
        if api_key not in api_keys:
            return RES_ERR_MSG_VAL_NOT_VALID(api_key_header)
        
        


class StockInfoView(APIView):
    """
    GET /stock?page={page}
    GET /stock?limit={limit}
    """
    def get(self, request):
        max_per_page = 10
        
        # headers
        page_header = 'page'
        limit_header = 'limit'
        order_by = 'stock_code'

        # GET Parameter 를 통하여 Pagination 기능 구현
        if page_header in request.GET:
            page = int(request.GET[page_header])
            if not isinstance(page, int):
                return RES_ERR_MSG_VAL_FORMAT_MISMATCH(page_header)
            
            stock_list = stock_info.objects.order_by(order_by)
            paginator = Paginator(stock_list, per_page=max_per_page)
            
            if page <= 0 or page > paginator.num_pages:
                return RES_ERR_MSG_VAL_NOT_FOUND(page_header)
            stock_list = paginator.get_page(page)

        elif limit_header in request.GET:
            limit = int(request.GET[limit_header])
            if not isinstance(limit, int) or limit > max_per_page:
                return RES_ERR_MSG_VAL_FORMAT_MISMATCH(limit_header)
            
            stock_list = stock_info.objects.order_by(order_by)
            total_size = len(stock_list)
            if limit < total_size:
                stock_list = stock_list[total_size - limit:]

        else:
            return RES_ERR_MSG_HEAD_MUST_EXISTS(page_header)

        serializer = StockInfoSerializer(stock_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """
    POST
    {
        "api_key" : xxxxxx,
        "market_name" : xxxxxx,
        "stock_code" : xxxxxx,
        "stock_name" : xxxxxx
    }
    """
    def post(self, request):
        if api_key_header not in request.data:
            return RES_ERR_MSG_HEAD_MUST_EXISTS(api_key_header)
    
        api_key = request.data.pop(api_key_header)
        if api_key not in api_keys:
            return RES_ERR_MSG_VAL_NOT_VALID(api_key_header)

        market_name_header = 'market_name'
        market_header = 'market'

        # market_name 을 바탕으로 외래키의 주키 찾기
        if market_name_header in request.data.keys():
            try:
                market_name = request.data.pop(market_name_header)
                market_object = market_type.objects.get(market_name=market_name)
                request.data[market_header] = market_object.id
            except market_type.DoesNotExist:
                return RES_ERR_MSG_VAL_NOT_FOUND(market_name_header)
        else:
            return RES_ERR_MSG_HEAD_MUST_EXISTS(market_name_header)

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
