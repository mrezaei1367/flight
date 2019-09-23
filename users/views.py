from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .serializers import UserProfileSerializer


class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = self.request.user
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            errs = {'errors':
                        [{'status': 400,
                          'detail': str(e),
                          'source': {'pointer': self.request.path}
                          }]}
            return Response(errs, status.HTTP_400_BAD_REQUEST)
