from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    bank = serializers.CharField(source='bank_name', help_text="bank_name is model property which gives bank name instead of bank id")
    class Meta:
        model = Branch
        # get all the fields and overwrite bank files with serializer field
        fields = '__all__'


class BranchIFSCView(APIView):

    def get(self, request, ifsc):
        try:
            branch = Branch.objects.get(ifsc__iexact=ifsc)
        except ObjectDoesNotExist:
            # HTTP_404_NOT_FOUND status
            raise NotFound('Branch not found for given IFSC code')
        serializer = BranchSerializer(branch)
        return Response(serializer.data)


class BankBranchView(APIView):

    def get(self, request):
        # Response time:  71 ms for 103 records: size 21 KB

        city = request.GET.get("city")
        bank = request.GET.get("bank")
        if not city or not bank:
            response_data = {"detail": "Both City and Bank names are required "
                                       "to get all the branches of the Bank in the City."}
            return Response(response_data, status=HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            branches = Branch.objects.filter(city__iexact=city,
                                         bank__name__iexact=bank).select_related("bank").values("ifsc", "bank__name","branch", "address","city", "district","state")
        except ObjectDoesNotExist:
            raise NotFound('No branch found for provided Bank and City.')

        data = [{
            "ifsc": branch["ifsc"],
            "bank": branch["bank__name"],
            "branch": branch["branch"],
            "address": branch["address"],
            "city": branch["city"],
            "district": branch["district"],
            "state": branch["state"]
        } for branch in branches]
        return Response(data)
