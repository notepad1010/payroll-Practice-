from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from security.models.role import Role,RolePermission,Permission
from security.serializer.role_serializers import RoleSerializer,PermissionSerializer,RolePermissionSerializer


class RoleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        role = Role.objects.all()
        serializer = RoleSerializer(role,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        if not request.user.is_staff:
            return Response({'error','Access Denied!'},status=status.HTTP_403_FORBIDDEN)
        serializer = RoleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Role.objects.get(pk = pk)
        except Role.DoesNotExist:
            return None
        
    def get(self,request,pk):
        # if not request.user.is_staff:
        #     return Response({'error':'Access Denied'},status=status.HTTP_403_FORBIDDEN)
        role = self.get_object(pk)
        if not role:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role)
        return Response(serializer.data)
    
    def put(self,request,pk):
        if not request.user.is_staff:
            return Response({'error':'Access Denied'},status=status.HTTP_403_FORBIDDEN)
        role = self.get_object(pk)
        if not role:
            return Response({'error':'Not Found!'},status=status.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(role,data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def delete(self,request,pk):
        if not request.user.is_staff:
            return Response({'error':'Access Denied'},status=status.HTTP_403_FORBIDDEN)
        role = self.get_object(pk)
        if not role:
            return Response({'error':'Not Found'},status=status.HTTP_404_NOT_FOUND)
        if role.user_role.exists():
            return Response({'error':'Cannot Delete a role that is assigned to user'},status=status.HTTP_400_BAD_REQUEST)
        role.delete()
        return Response({'message':'Role Deleted!'},status=status.HTTP_204_NO_CONTENT)
    
class AssignPermissionToRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Role.objects.get(pk = pk)
        except Role.DoesNotExist:
            return None

    def post(self,request,pk):
        if not request.user.is_staff:
            return Response({'error':'Access Denial'},status=status.HTTP_403_FORBIDDEN)
        role = self.get_object(pk)
        if not role:
            return Response({'error':'Role Not Found!'},status=status.HTTP_404_NOT_FOUND)
        permission_ids = request.data.get('permission_ids',[])

        permissions = Permission.objects.filter(id__in = permission_ids)
        if permissions.count() !=  len(permission_ids):
            return Response({'error': 'One or More permission ID are invalid'},status=status.HTTP_400_BAD_REQUEST)

        RolePermission.objects.filter(role = role).delete()
        RolePermission.objects.bulk_create([RolePermission(role = role,permission = p) for p in permissions])
        return Response(RoleSerializer(role).data)
    
