from django.shortcuts import render
from rest_framework import generics, views, status
from .serializers import *
from .models import Employee
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.apps import apps


class OneEmployeeAPIView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        try:
            obj_subject = Employee.objects.get(pk=kwargs.get('pk'))
        except:
            return Response({'error': 'Object does not exists'}, status=400)

        if not obj_subject.is_active:
            return Response({'error': 'Object does not exists'}, status=400)

        obj_serial = {}

        if obj_subject.id_leader:
            try:
                obj_leader = Employee.objects.get(pk=obj_subject.id_leader)

                if not obj_leader.is_active:
                    raise Exception

                obj_serial = EmployeeSerializer(obj_leader).data
            except:
                pass

        return Response({
            "employee": EmployeeSerializer(obj_subject).data,
            "leader": obj_serial
        }, status=200)



class CreateEmployeeAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = CreateEmployeeSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "id": serializer.data.get('id'),
            "token": serializer.data.get('token')
        }, status=status.HTTP_201_CREATED)

    # def post(self, request, *args, **kwargs):
    #
    #     is_leader_field = request.data.get('is_leader', None)
    #
    #     if is_leader_field:
    #         id_leader_field = request.data.get('id_leader', None)
    #
    #         if id_leader_field:
    #             return Response({"error": "if field 'is_leader' equals 'True', field 'id_leader' cannot be filled"})


class UpdateStatusAPIView(views.APIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UpdateStatusSerializer

    def put(self, request, *args, **kwargs):
        id_obj = request.data.get('id', None)

        if not id_obj:
            return Response({'error': 'Method PUT not allowed'}, status=400)

        try:
            instance = Employee.objects.get(pk=id_obj)
        except:
            return Response({'error': 'Object does not exists'}, status=400)

        last_activity = 'active' if instance.is_active else 'not active'

        serializer = UpdateStatusSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_activity = 'active' if serializer.data.get('is_active') else 'not active'

        return Response({
            "id": instance.id,
            "last_activity": last_activity,
            "activity": new_activity
        }, status=200)

class ChangeLeaderAPIView(views.APIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = LeaderEmployeeSerializer

    def put(self, request, *args, **kwargs):

        id_employee = request.data.get('id', None)

        if not id_employee:
            return Response({'error': 'Method PUT not allowed'}, status=400)

        id_leader = request.data.get('id_leader', None)

        if not id_leader:
            return Response({'error': 'Method PUT not allowed'}, status=400)

        if id_leader == id_employee:
            return Response({"error": "id_employee and id_leader must not be equal"}, status=400)


        try:
            obj_subject = Employee.objects.get(pk=id_employee)
        except:
            return Response({"error": "Object employee does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        if not obj_subject.is_active:
            return Response({"error": "Object employee does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj_leader = Employee.objects.get(pk=id_leader)
        except:
            return Response({"error": "Object leader does not exists"}, status=400)

        if not obj_leader.is_active:
            return Response({"error": "Object leader does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LeaderEmployeeSerializer(data=request.data, instance=obj_subject)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "id": serializer.data.get('id'),
            "id_leader": serializer.data.get('id_leader'),
            "status": "Success"
        }, status=200)


class LoginAPIView(views.APIView):
    queryset = Employee.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        # user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)











        

