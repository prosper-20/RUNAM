from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
# class HasPhoneNumberPermission(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.profile.phone_number:
#             return Response
#         # Check if the user has a phone number in their profile
#         return request.user.profile.phone_number is not None
    


# class HasPhoneNumberPermission(BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user.profile.phone_number)


class HasPhoneNumberPermission(BasePermission):
    message = {"You must complete your profile to create, view or accept tasks, click on this link: http://127.0.0.1:8000/users/profile/"}
    def has_permission(self, request, view):
        
        check = bool(request.user.profile.phone_number)
        if check == False:
            raise PermissionDenied(detail=self.message)
        return bool(request.user.profile.phone_number)
    
        



# permissions.py

# from rest_framework.permissions import BasePermission
# from rest_framework import status
# from rest_framework.exceptions import PermissionDenied


# class HasPhoneNumberPermission(BasePermission):
#     message = "User must have a phone number in their profile to create tasks."

#     def has_permission(self, request, view):
#         if request.user.profile.phone_number is None:
#             raise PermissionDenied(detail=self.message)
#         return True
